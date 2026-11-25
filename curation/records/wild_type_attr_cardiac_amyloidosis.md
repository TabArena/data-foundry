---
unique_name: wild_type_attr_cardiac_amyloidosis
name: Cardiac amyloidosis in heart-failure patients from claims codes (Huda et al. 2021, IQVIA validation cohort)
checked_by:
- Andrej
data_foundry_status:
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
decision_markers:
- Selection Bias
tags:
- Clinical Study
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Varying Delay'
- 'Features: Read Later'
- Many features
original_source: Other
year: '2021'
collection_period: Oct 2015 - Apr 2019
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.nature.com/articles/s41467-021-22876-9
- https://www.nature.com/articles/s41467-024-45879-8
- https://doi.org/10.1186/s12911-026-03654-3
- https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-021-22876-9/MediaObjects/41467_2021_22876_MOESM4_ESM.zip
v2_path: datasets/_dev/tabarena-v0pt2/wild_type_attr_cardiac_amyloidosis/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

**AI summary:**

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

CC (2026-11-25, Andrej): accepted for adding (asked in chat to build it); issue 2 c, built from the IQVIA validation file with any cardiac amyloidosis code as the label, issue 1 A applied to its flags.

**Assessment (AI, 2026-11-25):** collection period set from the paper's Methods, "Dataset curation": the IQVIA extract used "a date range (observation window) of 1 January 2008 to 30 April 2019" (read from PMC8113237); the screening's `Unknown` is replaced. The collection facts stand (`Samples: Over Time`, `Time: Lost`: the release holds one undated code list per patient).

**Assessment (AI, 2026-11-25):** built from the IQVIA validation file (issue 2 c), not the 2,142-patient derivation file the Screening block describes; the split is repeated 3-fold cross-validation on random patients (leaf L-PLACE.random: one source, no site column).

**Assessment (AI, 2026-11-25):** what sets this case apart from stroke_prediction and the other SEL-7 retirements: the label is a clinician's amyloidosis code set after a biopsy or scintigraphy, not a self-reported past diagnosis; Huda et al. name the screening decision; the model was validated at another health system (ROC AUC 0.80 at Northwestern); the paper shows antecedent codes years before the diagnosis; and the signal survives removing the diagnosis-era codes (0.816 after the narrow cut). Review issue 3 asks the curator to confirm.

**Assessment (AI, 2026-11-25):** review panel (full): ship after changes, made (code-first manifestation flags and heart-transplant status dropped; the source's case exclusions, intracranial haemorrhage included, applied to both classes: 13,454 patients, LightGBM 0.827; flags categorical; ROC AUC declared as the paper's metric); disputed: none left open; for the curator: issues 3-8 (SEL-7 facts, LEAK-10 work-up codes, USE-5 label, rename, LEAK-31 label-free selection, the transplant group flag). Priority 3: gap 0, use case + (named screening decision, external validation), source + (Nat Commun with released rows), shape + (13,454 patients, 1,695 flags), risk - (undated lifetime codes, a noisy label).

## Review

**Outcome:** added. Huda et al. 2021's IQVIA validation file (issue 2 c): heart-failure patients, label an amyloidosis code E85.4 or E85.82 (any cardiac amyloidosis, not only wild-type ATTR), ICD-10 presence flags built with Huda's map and 2% case rule, repeated 3-fold cross-validation on random patients (one source, no site column). The AI recommends shipping it with the panel's changes, which are made: the code-first manifestation codes and heart-transplant status dropped, and the source's case exclusions, intracranial haemorrhage included, applied to both classes (13,454 patients, ROC AUC 0.826 for LightGBM). Value: a real signal, above 0.80 after every cut against 0.548 for the number of codes alone. Quality: the label is a noisy mix of amyloid types (issue 5). Six questions are yours, first whether an undated past diagnosis can be this screening task (issue 3).

**Main points:** Keep it as a screening task with the distinguishing facts written (issue 3); which work-up codes go (issue 4, reopened); keep the source's broad label (issue 5); rename it (issue 6); the label-free 2% rule (issue 7); the transplant group flag (issue 8).

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

   **Andrej (2026-11-25, discuss):** Reply (c): Build this record from the validation file instead.

   **Resolved (2026-11-25, Andrej):** c: the record is built from Huda's IQVIA validation file (15,394 heart-failure patients, raw ICD-10 code lists); the label is an amyloidosis code (E85.82 or E85.4), every E85 code is removed from the features, the flags are built with Huda's ICD map and 2% case-prevalence rule, and issue 1's two leak flags go. The derivation file's score is reported beside it at /add-dataset.

   [^a2]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target away; out: a part, a consequence or another encoding of the target.

   [^a1]: **PROV-6** (Must): different versions or cuts of one underlying dataset are duplicates too when neither adds a distinct task: a swapped target, another slice of the same cohort, added or dropped rows or columns.

   [^split36]: **SPLIT-36** (Should): a definition's split is decided by walking the split decision tree; a forced leaf is for the curator to look at.

3. **Keep an undated past diagnosis as a screening task, with the facts that set it apart from stroke_prediction written down?**

   * **Problem:**
     - The label is an amyloidosis code in the same undated claims history as the features, and 52% of cases carry the companion code I43, so the history runs past the diagnosis[^sel7].
     - stroke_prediction, cdc_diabetes_health_indicators and south_africa_coronary_heart_disease were retired for an undated past diagnosis predicted from the same record.
   * **Background:** what may set this case apart: the label is a clinician's code set after a biopsy or scintigraphy, the source names a screening decision, the source's wild-type model held ROC AUC 0.80 at another health system (Northwestern; a model trained on the derivation cohort, not on this label), the paper shows antecedent codes years before the diagnosis, and the signal survives removing the diagnosis-era codes (0.816 after the narrow cut of issue 4).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, the facts written in the record (implemented) | an Assessment line names them; the task card says features and label share one undated record | the source's screening task; the timing problem is handled as a leak, by drops | a precedent the next undated diagnosis will cite |
     | B | Retire like stroke_prediction | `No Good Target / Scientific Discovery` | consistent with three retirements | loses the one screening dataset with a named actor and an externally validated source model |
     | C | Amend the rule | a clause on clinician-coded labels | one rule for every such case | a rule change for one dataset |

   * **Recommendation:** A; the advocate, the critic and the mediator agree the rule is not triggered on its text, and with the facts written down, the next undated diagnosis can be judged against them instead of against this outcome alone. **Decision:** A, B or C?

   [^sel7]: **SEL-7** (Must): a label the respondent already knows, asked in the same interview as the features (a past diagnosis), is predicted by nobody; a screening task needs positives found by an independent measurement.

4. **Which codes written during the work-up go? (issue 1, reopened as you asked)**

   * **Problem:**
     - The cardiomyopathy codes are lifetime flags: hypertrophic cardiomyopathy came before the diagnosis as a misdiagnosis (the paper), the restrictive, other and unspecified cardiomyopathy codes are written by the work-up, and end-stage and acute-on-chronic heart failure follow the disease[^leak10w].
     - Late values are kept only when they weaken the signal, and this family raises it[^leak11].
   * **Experiments:** ROC AUC (higher is better), 9 shipped splits, on the 13,454 patients after the changes made; 3 x 3-fold; a random extra column moves the mean by up to 0.0007, so smaller differences are noise.

     | Cut | LightGBM | Logistic regression |
     |---|---|---|
     | A: keep the family (implemented) | 0.8256 | 0.8074 |
     | narrow: drop `cardiomyopathy`, restrictive, other and unspecified cardiomyopathy, end-stage and acute-on-chronic heart failure; keep hypertrophic and dilated | 0.8155 | 0.7963 |
     | narrow plus cardiomegaly and abnormal heart imaging | 0.8151 | 0.7962 |
     | B: the whole family | 0.8168 | 0.7985 |
     | B2: the family and the heart-failure subtypes | 0.8051 | 0.7868 |

   * **Consistency:** distribution_transformers_at_cauca_department dropped values that changed after the outcome, with no allowance for the gain they gave.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the family (implemented) | as now | your first call; the paper's features | a late value that raises the score; needs a rule amendment |
     | B | Narrow cut | the flags named in the table | keeps the antecedent hypertrophic flags; costs about as much as dropping the whole family | our own list |
     | C | Narrow cut plus cardiomegaly and abnormal heart imaging | two more flags | also the imaging findings | those can come from the first heart-failure work-up too |
     | D | Drop the whole family | every cardiomyopathy flag | simplest | drops the antecedent |

   * **Recommendation:** B; the advocate and the critic both moved to it. **Decision:** A, B, C or D?

   **Notes for the AI:** On B, C or D: drop the flags in `_clean` after the 2% rule, name them in a note with the score, re-run `dataset check` on the cluster.

   [^leak10w]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target away; out: a column recorded after the outcome, a part, a consequence or another encoding of the target.
   [^leak11]: **LEAK-11** (Should): a value measured after the outcome that weakens the signal stays, with a note.

5. **Keep the source's broad label?**

   * **Problem:**
     - In the raw file every case holds E85.4 (organ-limited amyloidosis) and only 516 hold E85.82 (wild-type ATTR); 47% of cases carry no code linking the amyloid to the heart[^use5].
     - Before E85.82 existed (October 2017), E85.4 was the code used for ATTR cardiomyopathy, so its presence without I43 is no proof of non-cardiac amyloid.
   * **Experiments:** ROC AUC (higher is better), LightGBM, 9 shipped splits (3 x 3-fold), after the changes made; each row rebuilds the dataset with that label.

     | Label | Patients / cases | LightGBM |
     |---|---|---|
     | E85.4 or E85.82 (implemented) | 13,454 / 6,899 | 0.8256 |
     | E85.82, or E85.4 with I43 | 10,513 / 3,958 | 0.9092 |
     | E85.82 only | 7,053 / 498 | 0.9523 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the paper's Cohort 3 label (implemented) | a note with the code shares | the source's label | a noisy mix of amyloid types |
     | B | E85.82, or E85.4 with I43 | cases without a heart link dropped | closer to cardiac amyloid | selects the fully coded cases, the opposite of the undiagnosed patients the model scores; its +0.08 comes from that selection |
     | C | E85.82 only | 498 cases | wild-type ATTR exactly | the code exists from October 2017 only; about 166 positives per test fold |

   * **Recommendation:** A: the source's label, and the definition already notes the code shares; B's gain comes from keeping only the fully coded cases. **Decision:** A, B or C?

   [^use5]: **USE-5** (Must): predict what the actor would act on, at the resolution they act on it; check how the source built its label before accepting it.

6. **Rename the dataset?**

   * **Problem:**
     - The name says wild-type ATTR, but the label is any amyloidosis code and only 516 cases hold the wild-type code.
     - The name is the dataset's key in the record, the folder and the review pages.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `wild_type_attr_cardiac_amyloidosis` (implemented) | nothing | no key changes | the name misstates the label |
     | B | `cardiac_amyloidosis_iqvia_claims` | record, folder and notes renamed | says what the data is | one rename across files |

   * **Recommendation:** B (or a name you prefer). **Decision:** A or B?

   **Notes for the AI:** On B: rename the record file and `unique_name`, the folder and the class, `v2_path`, the CHANGELOG line and the split-tree example; re-run `sync-notebooks --check` and the record tests.

7. **Choose the flags without labels?**

   * **Problem:**
     - Huda's 2% rule keeps a flag when 2% of the cases have it, chosen on all cases, test folds included; on this file it is our own step, as Huda's validation notebook reused the trained model's flags[^leak31].
     - A rule without labels (2% of all patients) scores the same.
   * **Experiments:** LightGBM, ROC AUC (higher is better), 9 shipped splits (3 x 3-fold), after the changes made.

     | Rule | Flags | LightGBM |
     |---|---|---|
     | 2% of the cases (implemented) | 1,695 | 0.8256 |
     | 2% of all patients | 1,641 | 0.8256 |

   * **Consistency:** home_credit_default_risk and qsar_bioconcentration dropped a selection by the label that our own pipeline made; B follows them[^prec7].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Huda's rule on the cases (implemented) | as issue 2 c named it | the source's rule | uses every label |
     | B | 2% of all patients | label-free selection | no label used; same score; as the precedents | departs from Huda's rule |

   * **Recommendation:** B: the same score without using a label, as in the precedents. **Decision:** A or B?

   [^leak31]: **LEAK-31** (Should): supervised feature selection on the full labelled set: measure it; keep with a note when small, remove it when we can.
   [^prec7]: home_credit_default_risk (Lennart, 2026-10-19): the notebook's importance-based selection is not applied. qsar_bioconcentration (Lennart, 2026-10-26): the authors' 9 selected Dragon descriptors are dropped.

8. **Drop the transplant-status group flag?**

   * **Problem:**
     - `transplanted_organ_and_tissue_status` is the parent of the dropped heart-transplant code and still encodes it (3.1% of cases against 1.4% of controls)[^leak10b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep it (implemented) | as now | other transplants are antecedents | partly encodes the dropped code |
     | B | Drop it | one flag fewer | the dropped code cannot come back through its parent; ROC AUC 0.8258 against 0.8256 (LightGBM, 9 splits), within noise | other transplants go with it |

   * **Recommendation:** B: it closes the route back to a dropped leak code at no cost in score. **Decision:** A or B?

   [^leak10b]: **LEAK-10** (Must): a feature never gives the target away, also not through another encoding of a dropped value.

**Review panel:** ship after changes (mediator). Claims: 31 tested, 26 hold, 3 refuted (the metric's origin, the exclusion list's cohort, a duplicate count; reworded), 2 loosely worded. Blind review: include with changes and rename. Task gamer: mildly gameable (+0.008 from the J99 code, +0.016 from decoding the controls' exclusion codes), both fixed. Agreed: the drops, the exclusions on both classes, the split. Disputed: none left open; six questions go to you as issues 3-8.

<details><summary>Mediator</summary>

**Mediator: wild_type_attr_cardiac_amyloidosis**

Decisive experiment: a cluster run. Script
(a script in the run folder), results in `decisive2.json`
and `decisive2.log` next to it. Shipped 3 x 3 splits: shipped rows were matched to patients by flag pattern and
label, and variants that drop rows use the same folds with those rows removed. LightGBM (400 trees, 0.05, 31 leaves,
colsample 0.3) and L2 logistic regression (C 0.05). ROC AUC. Each variant recomputes the 2% rule on its own cases. The
shipped score reproduces (0.8376, the claim auditor's figure on the same splits).

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL-7 not triggered on its text (the label is a clinician's code set after a diagnostic test, not a
  self-report), but the distinguishing facts must be written (consistency with stroke_prediction and SAheart);
  USE-1 holds (approximate fit); USE-5 holds with a note (the source's Cohort 3 label, noisy) after the CAA/ICH
  cases go; LEAK-10 triggered, fixed: J99 and Z94.1 dropped by an amyloid code-first rule; LEAK-10 triggered by the
  work-up codes: the narrow cut recommended (issue 1); LEAK-13 triggered (case-only exclusions), fixed by applying
  them to both classes; PROV-6 holds (the derivation file is not shipped); SPLIT-36 forced leaf, holds.
Value: TP-2, a real signal: 0.816 (narrow cut + fixes) against 0.548 for the code count.
Quality: CLEAN-14 flags to categorical; MET-5 roc_auc is the source's metric; LEAK-31 label-free 2% rule (curator).
Weighed: size + (13,454 rows after the fixes), source + (Nat Commun, external validation), label noise -,
  matched sample -.
For the curator: issue 1 (narrow cut, A, B or B2); issue 2 (keep the Cohort 3 label or tighten it); issue 3
  (label-free 2% rule); issue 4 (Z94 group flag); issue 5 (forced leaf); a consistency check on SEL-7.
```

**Results (ROC AUC, 9 shipped splits)**

N = the agreed changes that need no decision, combined (rows and features below).

| Variant | Rows | Cases | Flags | LightGBM (sd; min-max) | LogReg |
|---|---|---|---|---|---|
| A shipped | 15,394 | 7,697 | 1,733 | 0.8376 (0.0035; 0.830-0.842) | 0.8131 |
| N0: A without J99 and Z94.1 | 15,394 | 7,697 | 1,731 | 0.8294 | 0.8087 |
| N1: N0 + control-only exclusions applied to both classes | 14,573 | 7,697 | 1,731 | 0.8296 | 0.8085 |
| **N: N1 + I60-I62 patients dropped from both classes** | 13,454 | 6,899 | 1,695 | **0.8256** (0.0026) | 0.8074 |
| N without the Z94 group flag | 13,454 | 6,899 | 1,694 | 0.8258 | 0.8070 |
| **N + narrow cut** | 13,454 | 6,899 | 1,688 | **0.8155** (0.0015) | 0.7963 |
| N + narrow cut + cardiomegaly and R93.1 | 13,454 | 6,899 | 1,686 | 0.8151 | 0.7962 |
| N + B (cardiomyopathy family) | 13,454 | 6,899 | 1,687 | 0.8168 | 0.7985 |
| N + B2 (B + I50 subtype flags) | 13,454 | 6,899 | 1,672 | 0.8051 | 0.7868 |
| N + label T1 (E85.82, or E85.4 with I43) | 10,513 | 3,958 | 1,594 | 0.9092 | 0.8985 |
| N + label T0 (E85.82 only) | 7,053 | 498 | 1,766 | 0.9523 | 0.9383 |
| N + label-free 2% rule | 13,454 | 6,899 | 1,641 | 0.8256 | 0.8071 |
| N + narrow cut + label-free 2% rule | 13,454 | 6,899 | 1,634 | 0.8140 | 0.7961 |
| N + narrow cut + T1 | 10,513 | 3,958 | 1,586 | 0.8951 | 0.8833 |
| N with every "classified elsewhere" flag dropped (broad rule, not recommended) | 13,454 | 6,899 | 1,683 | 0.8252 | 0.8073 |

Noise band: about 0.0007 (task gamer, random columns). The control-only exclusion removes 821 controls and no case.
The ICH exclusion removes 798 cases and 363 controls.

**Changes to make now (no decision needed)**

**Row and feature changes**

1\. **Drop amyloid code-first manifestation flags (LEAK-10, Must).** Rule for the definition: drop every flag all of
   whose codes are ICD-10-CM manifestation codes whose "code first" note names amyloidosis (E85.-): I43, J99, L99,
   K77, N29, G63, M14.8. Today this adds only `respiratory_disorders_in_diseases_classified_elsewhere` (J99: 180 cases,
   11 controls) to the I43 flag already dropped. The others are under 2% now, but G63
   (`polyneuropathy_in_diseases_classified_elsewhere`) passes once the label changes (T0), so write the rule, not the
   name. The code list comes from the ICD-10-CM tabular notes as I know them; check it against the CMS tabular when
   implementing. Do not use the broad name rule ("classified elsewhere" in the name): it drops anaemia in CKD,
   dementia and infection-agent flags whose notes do not name amyloidosis, and scores the same (0.8252).
2\. **Drop `heart_transplant_status` (Z94.1) (LEAK-10, Must).** 2.0% of cases and 0.2% of controls. The transplant
   follows the diagnosis or makes it. Items 1 and 2 together cost 0.008 (0.8376 to 0.8294).
3\. **Apply the source's case exclusions to both classes (LEAK-13, Must; the remedy ladder's repair from the
   source).** Drop every patient, case or control, whose code list holds N18.6, D47.2, E88.09, I68.0, C90.*, C85.88,
   C83.30, C83.39, C85.10, Z49.02, T85.691A (the codes with no case and at least 10 controls, plus I68.0: 821
   controls) or I60.*, I61.*, I62.* (intracranial haemorrhage: 798 cases, 363 controls). Then 13,454 patients remain
   (6,899 cases, 6,555 controls). The 2% rule then runs on the remaining cases. Cost: 0.004, all of it from the ICH
   step. The definition's current reason to keep the rows ("dropping those controls leaves the score unchanged") is
   no reason to keep them (LEAK-10's clause: a "removing it changes no score" test alone is no reason to keep).
4\. **Type the flags categorical (CLEAN-14, Should).** These are yes/no presence flags of named diagnoses (zillow
   precedent). This changes the dtype only, not the values.

**Identity and declarations**

5\. **Rename (USE-5 note).** `unique_name` and the record's `name` say wild-type ATTR, but every case holds E85.4 and
   only 516 hold E85.82. Proposed name: `cardiac_amyloidosis_iqvia_claims` (the curator may choose another). The
   folder, the record file, the class name and CHANGELOG follow.
6\. **Metric origin (MET-5, Should).** `roc_auc` is the source's metric. The paper selects its model "as evaluated by
   the AUROC" (Methods) and ranks the NMEDW models by AUROC only. Declare it as the source's metric with that quote.
   The score does not change.

**Wording only**

7. `fit_reason` and `predicted`: name the label noise. Every case holds E85.4 and 516 also hold E85.82; E85.9 is in
   35%, E85.3 (AA) in 10% and E85.1 (hereditary) in 9%; 47% of cases carry neither I43 nor E85.82. Also name the
   CAA/ICH exclusion.
8. `task_summary` (`known` or `row`): features and label come from one undated claims record. The history is ICD-10
   only (no ICD-9 code in any list), so it runs from about October 2015 to April 2019, not 2008 to 2019. Fix
   `collection_period` and the time basis to match.
9. The exclusion bullet: the full list (blood cancer, AL, ESRD, CAA, ICH) is the paper's NMEDW (Cohort 5)
   definition. For Cohort 3 the Methods say "blood cancers and other non-ATTR-CM-related amyloidosis terms". The ICH
   and CAA exclusion follows from that clause. Rewrite the bullet as the new rule of item 3, with its counts.
10. Duplicates: one group of 4 identical rows with both labels, not "2 patients".
11. "22,220 of 22,222 codes": one of the two unmapped values is the `-1` placeholder (1,293 patients); the real
    unmapped code is N35.81.
12. Median codes: 112 against 102 once the E85 codes go.
13. T63 anomaly: the bulk likely comes from the ICD-9 to ICD-10 conversion (989.5 maps to every T63 code).
14. Group basis: the drop from 0.93 to 0.80 is the wild-type model's, not a model trained on this label. Say so.
15. The 2% bullet: Huda applied the rule to the derivation's wild-type cases, and the validation notebook reused that
    feature list. On this file the rule is our adaptation. The "Potential leak, kept on purpose" figures follow
    issue 3.
16. `_decisions` table: the rows "cases excluded by the source" become "excluded from both classes", with the counts
    of item 3.
17. Record: the `## Review` Outcome line and the Screening `Split:` line still describe the 2,142-patient derivation
    file. Write an Assessment line for the validation file (15,394 patients, then 13,454 after the fixes, same leaf).
    Add the SEL-7 distinguishing facts (consistency, below).

**Issues for the curator (ranked)**

**1. Work-up and disease-course codes (issue 1, reopened): narrow cut, A, B or B2? (P4, LEAK-10 Must)**

* **Problem:** the flags are lifetime presence, and 52% of cases carry I43, so for at least half the cases the
  history runs past the diagnosis. `cardiomyopathy` (I42 parent) is the top single flag (51.9% against 26.5%).
* **Settled facts:** LEAK-11 cannot keep the family, because it raises the score. LEAK-10's clause on late values
  that cannot be located row by row says they go "when they may carry a gain" (distribution_transformers). Here the
  gain is +0.010. So A as implemented departs from a Must; keeping it needs an amendment, not an exception. The
  narrow cut must drop the `cardiomyopathy` parent, because I42.5, I42.8 and I42.9 set it; keeping the parent keeps
  the leak.
* **Options (on top of N):**

  | | Option | LightGBM | LogReg | Pro | Con |
  |---|---|---|---|---|---|
  | narrow | drop `cardiomyopathy`, I42.5/.8/.9 (`other_restrictive_cardiomyopathy`, `other_cardiomyopathies`, `cardiomyopathy__unspecified`), `end_stage_heart_failure`, the 4 acute-on-chronic HF flags; keep HCM and dilated | 0.8155 | 0.7963 | drops the codes the work-up and the disease course write, keeps HCM, which the paper says came before the diagnosis | our own list; the remaining flags still cover the whole history |
  | narrow+ | narrow, plus `cardiomegaly` and R93.1 | 0.8151 | 0.7962 | drops imaging findings too | cardiomegaly is often coded at the HF diagnosis (49% of cases against 33% of controls); costs 0.0004 more |
  | B | the whole cardiomyopathy family | 0.8168 | 0.7985 | a simple rule | drops HCM, a real antecedent; keeps acute-on-chronic and end-stage HF |
  | B2 | B plus every I50-only subtype flag | 0.8051 | 0.7868 | the harshest cut | drops the HF type (HFpEF), which is known before referral |
  | A | keep all (the curator's 2026-11-25 call) | 0.8256 | 0.8074 | the paper's features | needs an amendment of LEAK-10 for coded histories |

* **Advocate:** moved from A to the narrow cut. Would leave cardiomegaly and R93.1 out of the default.
* **Critic:** narrow cut, with the parent dropped; A only with an amendment.
* **Recommendation:** narrow. It costs 0.010, which is about B's cost, and it keeps the antecedent HCM flags that B
  drops. **Decision:** narrow, narrow+, B, B2 or A (with an amendment)?

**2. The label: keep the source's Cohort 3 label, or tighten it? (P3, USE-5 Must)**

* **Problem:** every case holds E85.4 ("organ-limited"). 47% have no code that ties the amyloid to the heart.
* **Options (on top of N):**

  | | Option | Rows / cases | LightGBM | Pro | Con |
  |---|---|---|---|---|---|
  | keep | E85.4 or E85.82 (Cohort 3) | 13,454 / 6,899 | 0.8256 | the source's label; covers ATTR-CM coded under the general term before E85.82 existed (October 2017) | noisy: AA, hereditary and unspecified amyloid among the positives |
  | T1 | E85.82, or E85.4 with I43; the other cases dropped | 10,513 / 3,958 | 0.9092 (narrow cut: 0.8951) | the positives have a heart link | selects the positives by I43, the post-diagnosis companion code the features drop, so it keeps the cases whose diagnosis is fully coded, the opposite of the undiagnosed patients the use case scores; +0.08 fits that; our own redefinition |
  | T0 | E85.82 only | 7,053 / 498 | 0.9523 | the specific wild-type code | the code exists only from October 2017; 505 of the 516 are the derivation's curated cases; about 166 positives per test fold; near the ceiling |

* **Recommendation:** keep, with the note of change 7. The CAA/ICH positives, the part that was clearly another
  quantity, go with change 3. A label without I43 is not proof of non-cardiac amyloid, because E85.4 was the code
  for ATTR-CM before E85.82. **Decision:** keep, T1 or T0?

**3. The 2% rule: Huda's rule on all cases, or label-free? (P4, LEAK-31 Should)**

* **Problem:** the case-based rule uses every label, test folds included. On this file it is our own step (the
  validation notebook reused the derivation's feature list). The curator named "Huda's 2% rule" in issue 2 c.
* **Options:** Huda's rule on this file's cases: 0.8256, 1,695 flags. Label-free rule, a flag in at least 2% of all
  patients: 0.8256, 1,641 flags. With the narrow cut: 0.8155 against 0.8140.
* **Settled:** LEAK-31 is the rule, not LEAK-29, because it is the specific rule for selecting columns. The
  label-free rule also drops J99 on its own (1.2% of patients).
* **Recommendation:** label-free (home_credit, qsar_bioconcentration, numerai). It costs nothing, and the column set
  no longer depends on the test folds' labels. **Decision:** Huda's rule or label-free?

**4. The Z94 group flag `transplanted_organ_and_tissue_status` (P4, LEAK-10)**

* With Z94.1 gone, the parent still encodes it for most cases (3.1% against 1.4%, mostly heart). Drop: 0.8258;
  keep: 0.8256 (within noise).
* **Recommendation:** drop it, by the same parent-and-child reasoning as issue 1. **Decision:** drop or keep?

**5. Forced leaf L-PLACE.random, reached for the first time (SPLIT-36, Should)**

* The use case is another health system, and the file has no site column. The other branch (later patients) is
  forced random too. The grouped alternative scores the same (0.837).
* **Recommendation:** confirm. **Decision:** confirm the leaf?

**Disputed points, settled**

| Point | Advocate | Critic | Settled by | Outcome |
|---|---|---|---|---|
| Is SEL-7 triggered? | no: an independent diagnostic code, not self-report | yes, by the stroke_prediction analogy | SEL-7's text ("found by an independent measurement such as a lab test") | not triggered. The timing problem is LEAK-10's and is fixed by drops. Both sides agree the distinguishing facts go in the record (consistency, below) |
| Issue 1: weighing call or Must? | weighing call (opening); narrow default (rebuttal) | Must: A needs an amendment | LEAK-10's late-values clause (gain +0.010), LEAK-11 not available | Must: A needs an amendment. Which cut is the curator's call (issue 1) |
| Must the narrow cut drop the `cardiomyopathy` parent? | first kept it | drop it | I42.5/.8/.9 set the parent (task gamer exploit 3 logic) | drop it; measured that way |
| Cardiomegaly and R93.1 | keep them out of the default | measure as an add-on | measured: 0.0004 | an option within issue 1, not the default |
| ICH exclusion: USE-5 or LEAK-13 | LEAK-13 | USE-5 | same remedy | apply to both classes (change 3); the note cites the Cohort 3 clause |
| 2% rule: LEAK-29 or LEAK-31 | LEAK-31 | LEAK-31 after the rebuttal | LEAK-31 narrows LEAK-6/LEAK-28 for column selection | LEAK-31, Should; curator (issue 3) |

**The task gamer's exploits, mapped**

| # | Exploit | Rule | Definition's note | New or known | Measured against the note |
|---|---|---|---|---|---|
| 1 | J99 manifestation flag, +0.0081 on 9 of 9 splits | LEAK-10 (Must) | none. The lifetime note names only the I42 family; J99 is another encoding of the target, like I43 | **new** | fixed by change 1 (−0.008 together with Z94.1) |
| 2 | Controls by construction (797 to 821 controls with codes no case may carry); +0.016 if decoded | LEAK-13 (Must); LEAK-10 clause on "changes no score" | known: a "Note" (marker AUC 0.551, LightGBM 0.837 with and without) | **known, but the conclusion is wrong**: the size matches (N0 0.8294 against N1 0.8296), but the note keeps the rows on that test, which LEAK-10 rules out, and the decodable ceiling (+0.016) is not in the note | fixed by change 3 |
| 3 | Hierarchy residuals (parent flag without an in-kit child), +0.0013 | LEAK-13 (it decodes the same exclusion codes) and the parent-child rule of issues 1 and 4 | none | new, near noise | removed with change 3 and the parent drops; no separate change. Shipping one hierarchy level only would be our own redesign; not recommended |
| — | Timing block (7 cardiomyopathy flags, pericardial effusion, transplant), +0.0073 | LEAK-10 / USE-3 | known: "Potential leak, kept on purpose" (lifetime presence, `cardiomyopathy`) | known; the size matches the note's issue 1 figures (0.008) | issue 1 |
| — | I43 restored (+0.057) | LEAK-10 | known, already dropped | known | none |

**Agreed facts**

* The table rebuilds bit for bit from the public Source Data (blind reviewer: all 1,733 prevalences, 15,390 of 15,394
  rows hash-match). The label is Huda's notebook rule: E85.4 or E85.82 in the code list.
* There are 7,697 cases and 7,697 controls. Every case holds E85.4 and 516 also hold E85.82; no control holds an E85
  code. 597 patients are also in the derivation file, which is not shipped.
* The flags are undated lifetime presence. No release has per-code dates, so no cut at the prediction point can be
  rebuilt. I43 is in 52.4% of cases.
* J99 (180 against 11) and Z94.1 (2.0% against 0.2%) are consequence or companion codes.
* 821 controls and no case carry the case-only exclusion codes. 798 cases (10.4%) and 363 controls carry I60-I62,
  with a CAA profile (lobar ICH 238 against 17). The shipped model scores the ICH cases at 0.915 and the others at
  0.828.
* The signal is broad: 0.805 to 0.816 after the harshest cuts, against 0.548 for the code count alone. The split is
  right for the file: train against test AUC 0.50, no exploitable pairs or near copies.
* `roc_auc` is the right metric. The paper selects its model by AUROC.

**Consistency**

* **Followed:** distribution_transformers_at_cauca_department (narrow cut, issue 1); home_credit,
  qsar_bioconcentration, numerai (label-free rule, issue 3); hepatitis_c_prediction and gallstone_disease (LEAK-13,
  class-specific recording harmonised: change 3); zillow (CLEAN-14); forest_fires (MET-5); the Selection Bias set
  (matched sample, marker kept); pheochromocytoma_paraganglioma_metastasis (same forced leaf).
* **Departure the record must name (SEL-7):** stroke_prediction, cdc_diabetes_health_indicators and SAheart were
  retired as look-backs. What sets this case apart: the label is a clinician's code set after biopsy or scintigraphy
  (the independent measurement SEL-7 asks for); the source names a screening decision; the model was validated
  externally (0.80 at Northwestern); the paper's figure shows non-cardiac antecedents years before the diagnosis; the
  signal survives the removal of the diagnosis-era codes (0.816 with the narrow cut). Proposed consistency check
  for the curator:

  > **Consistency check (AI, 2026-11-25):** keeping this coded-history task differs from stroke_prediction and SAheart
  > (an undated past diagnosis, retired). What sets it apart? (a) a label from a diagnostic test, a screening decision
  > named by the source, external validation, and a signal that survives the diagnosis-era drops, recorded in the
  > record; (b) treat it like stroke_prediction (`No`); (c) change SEL-7 (an amendment).
  > Recommendation: (a).
* **SAheart's LEAK-11 keep** does not carry over, because the family raises the score here.
* **The curator's own issue 1 A (2026-11-25)** was given with "reopen this as a discussion point". The narrow-cut
  recommendation reopens it with new facts (LEAK-11 not available, +0.010), so it does not override that call.

</details>

<details><summary>Claim audit</summary>

**Claim audit: wild_type_attr_cardiac_amyloidosis**

Evidence: `panel/claim-auditor_facts.txt` (raw-file counts, login-node pandas), `panel/claim-auditor_frame_checks.json` + `.log` (a cluster run), `panel/claim-auditor_src/` (the notebooks, the derivation file, the paper's text). Scripts: (a script in the run folder). The builder's `variants.json` was read, not rerun, except the shipped score, which I reproduced on the shipped splits.

**Summary:** 31 claims tested. 26 hold, 3 refuted (all minor: the metric's origin, a citation, a duplicate count), 2 partly hold (wording). Nothing changes the task, the split or the label.

**Claims**

| # | Claim | Where | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Metric: `Metric.fallback`, "several metrics reported ... at no threshold set by a decision" | `metric` reason; record Screening "Metric" line | Read the paper's Methods and the notebooks | **Refuted (origin only)** | Methods: "The Random Forest model, which had the best diagnostic performance (as evaluated by the AUROC curve), was carried forward". Results: the RF "had the highest AUROC of 0.93 (vs. 0.91 LR, 0.90 XGBoost) ... Thus, the Random Forest ML model was carried forward". Table 4 ranks the NMEDW models by AUROC only. So the paper selects its model by ROC AUC, and that makes ROC AUC its one deliberate metric. The reason says "Looked at: Results and Tables 2-5", but it misses this Methods sentence. GridSearchCV in `Model Training.ipynb` keeps the default (accuracy) for the tuning, but the paper names AUROC as the criterion it selects by. | MET-5, MET-1 |
| 2 | ROC AUC can be computed on every fold and means here what it meant in the source | MET-2 (implied) | Dummy and random predictions through `declared_metric()` on all 9 shipped folds; positives per fold | Holds | Each test fold has 5,131-5,132 rows, of which 2,565-2,566 are positives. A constant 0.5 scores 0.500 and random scores 0.491-0.516. The metric needs no inputs. The target is the source's Cohort 3 label (`cohort_flag`) at the source's 1:1 balance. The splits cover every row once per repeat, and train and test never overlap. | MET-2 |
| 3 | Label = code list holds E85.82 or E85.4, "the rule of Huda's `Model Validation.ipynb`" | comments | Read the notebook | Holds | `cohort_flag = np.where(codes=='E8582','1', np.where(codes=='E854','1','0'))` | LEAK-10 |
| 4 | 7,697 cases and 7,697 controls | comments | Counted | Holds | 7,697 / 7,697 | - |
| 5 | Every case holds E85.4, 516 also E85.82, no control holds any E85 code | comments; `predicted` | Counted E85* by class | Holds, but incomplete | E854 is in 7,697 cases. E8582 is in 516, every one of which also holds E854. No control has an E85 code. The claim leaves out that cases also carry E85.9 (2,701, 35%), E85.8 (1,197), E85.3 secondary systemic (AA) amyloidosis (783, 10%), E85.1 hereditary neuropathic (716, 9%) and E85.89 (507). See finding U1. | - |
| 6 | Every E85 code is removed before the features are built | comments; `known` | Searched the column names for "amyloid" | Holds | No column contains "amyloid". The prefix filter runs before the melt. | LEAK-10 |
| 7 | "its companion cardiomyopathy code removed" (I43) | `known`; comments | Read I43's three names in `icd_map.csv` | Holds | I43 → short_desc and major "Cardiomyopathy in diseases classified elsewhere", sub_chapter "Other Forms Of Heart Disease". Both cleaned names are the dropped leak flags, so I43 gives no feature. | LEAK-10 |
| 8 | 22,220 of 22,222 distinct codes are in the map; the two that are not give no flag | comments | Counted | Holds | The two missing codes are `-1` (a placeholder, not a code) and `N3581`. | - |
| 9 | Three names per code, cleaned as in the source; names that clean to the same string share one flag | comments | Read `preprocess` in `Model Validation.ipynb` | Holds | The notebook does `.str.lower().str[:100].replace("[^A-Za-z0-9]","_",regex=True)` and pivots on the cleaned name. | - |
| 10 | "A flag is kept when at least 2% of the cases carry it, Huda's rule"; "with the source's map and 2% rule" | comments; `changes` | Minimum case share in the frame; source code | Partly holds (wording) | The frame's minimum case share is 0.02001. Huda, however, applied the 2% rule to the wild-type ATTR-CM derivation cases ("present in at least 2% of wild-type ATTR-CM patients"). The validation notebook does not re-select: it keeps the trained model's feature list (`feature_importance.csv`). Applying the rule to the Cohort 3 cases is our adaptation of Huda's rule. | PROV (wording) |
| 11 | `cardiomyopathy_in_diseases_classified_elsewhere` is in 52.4% of cases and 1.4% of controls; `other_forms_of_heart_disease` is in every patient | comments | Counted I43; I50 is in every patient | Holds | I43: 52.45% / 1.44%. All patients carry an I50 code, which lies in I30-I52. | LEAK-10 |
| 12 | Dropping the source's two leak flags follows `Model Training.ipynb` `potential_target_leaks` | comments | Read the notebook | Holds | `potential_target_leaks = ['cardiomyopathy_in_diseases_classified_elsewhere','other_forms_of_heart_disease']`. In the validation notebook the drop line is commented out, but the feature list there already excludes both flags. | - |
| 13 | The case-only exclusions quote Methods: cases without "blood cancer, light chain amyloidosis, end-stage renal disease, cerebral amyloid angiopathy, or intracranial hemorrhage", "the definitions of Cohorts 3 and 4" | comments | Searched the paper's text | **Refuted (citation)** | That sentence defines the **NMEDW cohort (Cohort 5)** ("The NMEDW dataset was queried ... Cases were patients with an organ-limited amyloidosis code (E85.4) plus a HF diagnosis code but not blood cancer, ..."). For Cohorts 3-5 the Methods say only "we excluded blood cancers ... and other non-ATTR-CM-related amyloidosis terms". The data show the Cohort 5 list was in effect applied to Cohort 3 too, except intracranial haemorrhage, so the substance stands and only the attribution is wrong. | - |
| 14 | 785 controls (10.2%) and no case carry N18.6 (498), D47.2 (136), E88.09 (161), C90 (73), I68.0 (2) | comments; Decision table | Counted | Holds | Exactly these numbers; 0 cases. | SEL |
| 15 | Intracranial haemorrhage was not excluded (10.4% of cases, 4.7% of controls) | comments | I60-I62 by class | Holds | 10.37% / 4.72% | - |
| 16 | Those exclusion markers are the whole case-only selection | implied by 14 | Every code with 0 cases and ≥10 controls | Holds, nearly | 13 codes. Besides the listed ones: lymphoma codes C85.88 (20), C83.30 (17), C83.39 (15), C85.10 (14), myeloma C90.0x (counted under C90), and dialysis-access codes Z49.02 (13) and T85.691A (11). They overlap the listed controls and stay far under the 2% case rule. "Blood cancer" was excluded only in part: cases hold C91 leukaemia 1.0%, D46 MDS 1.2%, C85 0.4%. | SEL |
| 17 | The marker alone scores ROC AUC 0.551; LightGBM 0.837 with and without those controls | comments | Read `variants.json` (builder, cluster) | Holds | marker 0.5510; A 0.8372 vs C (14,609 rows) 0.8366 | - |
| 18 | Dropped 7 flags that hold the same patients as another (e.g. `essential__primary__hypertension` / `essential_hypertension`) | comments | Identical columns left in the frame; example names | Holds | 0 identical columns left. `essential__primary__hypertension` is kept and `essential_hypertension` is gone. The 1,740 flags (after the 2% rule and the leak drop) become 1,733, so 7 went. | - |
| 19 | Dropped `patient_id` | comments | Frame columns | Holds | 1,733 int8 0/1 features + target | - |
| 20 | `exposure_to_...` flags are ICD-10 external-cause codes, not an amount at risk | comments | Names | Holds | 3 flags: `exposure_to_animate/inanimate_mechanical_forces`, `exposure_to_other_specified_factors__initial_encounter` (W, X codes). The bundle warning `task_feature_looks_like_exposure` is a false positive. | MET-15 |
| 21 | "2 patients repeat another's flags exactly (1 with the other label)" | comments | Hashed the feature rows of the frame | **Refuted (count)** | One group of **4 identical rows** (3 repeats), and the group holds both labels. The conclusion (keep them) is unaffected. | DUP |
| 22 | Every patient has a heart-failure code (I50) | comments; `row` | Counted | Holds | 0 patients without I50. The source notebook's HF filter therefore drops no one. | - |
| 23 | Median number of codes 114 in cases, 102 in controls | comments | Counted | Partly holds | Raw code lists with the E85 codes: matches. Without the E85 codes: 112 vs 102. Kept flags: 191 vs 175. | - |
| 24 | Paper Table 1: 7,296 + 7,296 for Cohort 3; the file holds 7,697 each | comments (Anomaly) | Paper's Table 1 | Holds | Table 1: "Cardiac amyloid + HF (n = 7296)" | - |
| 25 | 110 patients (56 cases, 54 controls) carry up to 152 T63 codes, equally common in both classes | comments (Anomaly) | Counted | Holds | 110, 56 cases, max 152, median 152; 0.73% / 0.70% | - |
| 26 | `cardiomyopathy` (I42) is in 51.9% of cases and 26.5% of controls | comments | Flag shares in the frame | Holds | 51.89% / 26.50% | LEAK-10 (issue 1) |
| 27 | Transductive 2% rule moves nothing: 0.837 / 0.838 / 0.839 | comments | `variants.json`; shipped-split rerun | Holds | 0.8372 / 0.8379 / 0.8392. On the shipped splits with the shipped 1,733 flags: LightGBM 0.8376 (0.830-0.842), LR 0.8131. | LEAK-27 |
| 28 | 597 of the validation patients (505 cases, 92 controls) are rows of the derivation file with the same label | comments | Joined on `patient_id` | Holds | 597; 505/92; 100% agreement. All 505 derivation wild-type cases hold E85.82 here, so 505 of the 516 E85.82 cases are derivation cases. | PROV-6 |
| 29 | Patients aged ≥50, IQVIA 1 Jan 2008 - 30 Apr 2019; 1:1 propensity matching on age, sex, history length, visit count | `row`; comments; time_basis; record `collection_period` | Paper text | Holds | "patients in all five cohorts were only included if they were 50 years or older"; "observation window of 1 January 2008 to 30 April 2019"; "Patients in the first four cohorts were matched on age, sex, duration of medical history ... number of healthcare visits". E85.82 has been an ICD-10-CM code since FY2018 (Oct 2017), so its presence before April 2019 is consistent. | - |
| 30 | Fit reason: 0.7% prevalence at Northwestern; the source model fell from 0.93 (IQVIA holdout) to 0.80 at Northwestern | `fit_reason`; group_basis | Tables 1, 2, 4 | Holds | 261 / 39,654 = 0.66%; Table 2 0.93; Table 4 "ATTRwt-CM RF model 39,654 0.80". | - |
| 31 | No site/region column; one source; undated code lists (`Time: Lost`) | time_basis, group_basis, record tags | Raw file columns | Holds | The file has two columns: `patient_id` and `codes`. (Table 1 shows that a "location of final visit" region existed upstream but was not released.) | SPLIT-36 |

**Refuted and untested, ranked**

None of these bears on validity: the label, the split and the features stand. In rank order:

1\. **Metric origin (claim 1), MET-5 Should.** The metric stays `roc_auc`, but its origin is the paper, not a fallback. The paper selects its model "as evaluated by the AUROC" (Methods) and ranks the RF over LR and XGBoost by AUROC (Results, Supplementary Table 2). It also compares the NMEDW models only by AUROC (Table 4). *Mildest remedy:* declare it as the source's metric with that reference (the "deliberate choice" case of MET-5, as forest_fires and open_soil_spectral_library were handled), and correct the record's Screening "Metric" line. The scores do not change.
2\. **Exclusion-list citation (claim 13).** The quoted exclusion list is the NMEDW (Cohort 5) definition. For Cohort 3 the Methods say "excluded blood cancers ... and other non-ATTR-CM-related amyloidosis terms". *Remedy:* reword the bullet: "the Methods' case exclusions (stated in full for the NMEDW cohort; for Cohorts 3-5, 'blood cancers and other non-ATTR-CM-related amyloidosis terms'); in this file 785 controls ...". Optionally add that the blood-cancer exclusion was partial (cases hold leukaemia, MDS and lymphoma codes; only myeloma is absent).
3\. **Duplicate count (claim 21).** One group of 4 identical patients (3 repeats) with both labels, not "2 patients". *Remedy:* correct the numbers in the note.
4\. **Wording (claims 10, 23).** "Huda's 2% rule" is Huda's rule applied by us to the Cohort 3 cases; Huda's validation run reused the derivation feature list. The median 114/102 counts the E85 codes. *Remedy:* "Huda's 2% rule, applied to this file's cases" and "median 112 vs 102 codes after the E85 codes go".

Untested: none.

**Unwritten claims attacked**

- **U1, what the label means (informational).** The `predicted` text gives the label as "E85.4 ... or E85.82" and calls the class "cardiac amyloidosis". The cases also hold E85.3 secondary systemic (AA) amyloidosis (10%) and E85.1 hereditary neuropathic (9%), although the paper says it excluded "other non-ATTR-CM-related amyloidosis terms". E85.9 unspecified is in 35% of cases. Every E85 code is removed, so nothing leaks. The label is "organ-limited amyloidosis code in a heart-failure patient", a noisy proxy that mixes ATTR, some AA and unspecified amyloidosis. The record's "broader label" option already flags this; a curator may want the shares stated in the label bullet.
- **Features known at the prediction point:** the lifetime-flag leak (I42 `cardiomyopathy` and the rest) is the open issue 1 and is measured (B: 0.829 vs 0.837). I did not relitigate it.
- **Copies across the split:** there are no repeated patient ids. The single group of 4 identical rows is negligible. The 597 patients shared with the derivation file matter only if both files ship.
- **Split fits the use case:** forced random; the time and group bases say so and quote the source's transfer drop. Holds as written.

Sources (web): E85.82 effective FY2018: [CMS ICD-10-CM tabular addenda 2018](https://www.cms.gov/files/document/icd10-cm-tabular-addenda-2018-pdf.pdf), [HHS index addenda 2018](https://www.hhs.gov/guidance/sites/default/files/hhs-guidance-documents/icd10cm_index_addenda_2018.pdf).

</details>

<details><summary>Column audit</summary>

**Column audit: wild_type_attr_cardiac_amyloidosis**

The prediction point is a heart-failure patient's claims history before anyone tests them for amyloid. The flags record whether a code ever appears over the patient's whole history, and the codes carry no dates, so no code can be placed before or after the diagnosis. Each code family below is therefore judged by what it means clinically: an antecedent, a companion code written with the diagnosis, a code from the work-up, or a code from the disease course after diagnosis. All 1,733 flags were audited as code families: each flag mapped back to the codes behind it, with its case and control shares and its single-flag AUC (0.5 + (case share − control share)/2).

Scripts and outputs are in `panel/column-auditor/`:
- `column-auditor_all_flags.csv`: every one of the 23,853 candidate flags, with its codes, shares and AUC.
- `column-auditor_code_shares.csv`: shares for each raw code.
- `column-auditor_variants.json`: the cluster run's results (LightGBM / L2 logistic regression, 3 x 3-fold, seed 4267).

**Files**
All 7 files in the Source Data zip are accounted for. Two are read; the derivation CSV, both notebooks and `package-readme.txt` are left out with a reason given in `curation_comments`. No finding.

**Column table (grouped)**

| Family (example columns) | Meaning | Known at prediction? | dtype / cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| I43 `cardiomyopathy_in_diseases_classified_elsewhere` (dropped) | companion code written with E85 ("code first amyloidosis") | no | — | dropped, correct: 52.4% / 1.4% | LEAK-10 |
| J99 `respiratory_disorders_in_diseases_classified_elsewhere` | manifestation code that requires its underlying disease to be coded first (here pulmonary amyloidosis) | no: written with the E85 diagnosis | int8 0/1 | **leak**: 180 cases / 11 controls (2.3% / 0.1%), likelihood ratio 16 | LEAK-10 (Must) |
| Other "in diseases classified elsewhere" codes (L99 121/0, K77 56/3, I52 13/3, N29, N33) | same companion mechanism | no | not kept (each under the 2% rule) | fine as shipped; they would enter if the 2% rule changed | LEAK-10 |
| Heart transplant: `heart_transplant_status` (2.0% / 0.2%), `transplanted_organ_and_tissue_status` (3.1% / 1.4%, sub-chapter Z94) | the patient had a transplant (Z94.1); aftercare, rejection and LVAD codes are all under 2% | no for most: a transplant follows the diagnosis or is the event that makes it (amyloid found in the removed heart) | int8 | **leak (consequence)**: drop `heart_transplant_status`; the Z94 group flag is mixed, so it is a question | LEAK-10, USE-3 |
| I42 cardiomyopathy: `cardiomyopathy`, `cardiomyopathy__unspecified`, `other_restrictive_cardiomyopathy`, `other_cardiomyopathies`, `dilated_cardiomyopathy` | cardiomyopathy codes; I42.5/I42.8/I42.9 are the codes the work-up writes | mixed | int8 | question (issue 1, reopened): 51.9% / 26.5%, top single flag, AUC 0.627 | LEAK-10 / USE-3 |
| I42.1/I42.2 hypertrophic cardiomyopathy (`other_hypertrophic_cardiomyopathy` 486/71, `obstructive_...` 205/50) | HCM | mostly yes: the paper says HCM "preceded the ATTR-CM diagnosis" as an initial misdiagnosis | int8 | fine (antecedent) | USE-3 |
| I50 HF subtypes (HFpEF I50.3x 58.5% / 38.1%, combined I50.4x 34.7% / 15.7%, acute-on-chronic, `end_stage_heart_failure` 1.6% / 0.2%) | heart-failure type and stage | partly: the HF type comes before the diagnosis, but acute-on-chronic and end-stage codes follow the disease course | int8 | question, tied to issue 1 (B2 measured) | USE-3 |
| Antecedent red flags: carpal tunnel G56.0 (17.3% / 6.8%, bilateral LR 3.2), trigger finger / tenosynovitis M65, lumbar spinal stenosis M48.06, tendon rupture M66 | the paper's own "harbingers", years before diagnosis | yes | int8 | fine | — |
| Cardiac phenotype: atrial flutter, AV block / bundle-branch block I44–I45 (36.6% / 24.8%), pericardial effusion I31.3 (10.5% / 2.4%), pleural effusion, ascites, cardiomegaly I51.7 | the paper's cardiac predictors | mostly yes (they can also come from the work-up) | int8 | fine | — |
| Work-up findings: R93.1 abnormal cardiac imaging (6.6% / 2.8%), R77 plasma proteins (3.5% / 1.8%), R74 enzymes such as troponin (23% / 13%), R94.31 ECG | test results; R93.1 and R77 fit an echo, MRI or scintigraphy and a light-chain screen | partly no | int8 | weak, kept; already covered by the "lifetime presence" note | USE-3 |
| Intracranial haemorrhage I60–I62, cerebral oedema / compression G93.5–6 (35 flags) | brain bleeds; lobar (cortical) ICH I61.1 238 / 17, LR 14 | yes in time, but see problem 3 | int8 | **question on the target** (problem 3) | TGT / selection |
| Negatives: type 2 diabetes (45% / 55%), COPD, CABG Z95.1, obesity, smoking | comorbidity | yes | int8 | fine (real epidemiology, matched sample) | — |
| Everything else (about 1,600 flags: symptoms, Z encounter codes, injuries, other chronic disease) | coded history | yes, apart from the whole-history caveat | int8 | fine | — |
| `cardiac_amyloidosis` (target) | E85.4 or E85.82 | — | category No/Yes | see problem 3 | — |

**Name cleaning and duplicates**
- **Merges among kept flags: 11, all harmless.** Each joins the same name in title case (sub-chapter) and sentence case (major group), e.g. `abnormal_tumor_markers` and `body_mass_index__bmi_`.
- **Merges where truncation at 100 characters joins different names:** these exist (e.g. a "with macular edema" and a "without macular edema" diabetic-retinopathy code share one flag), but none of those flags passes the 2% rule. The 5 kept flags of length 100 each come from one name. No finding.
- **Exact duplicate columns: confirmed 7 pairs.** They match the 7 the definition drops; the lowest name in sorted order stays.
  - `essential__primary__hypertension` = `essential_hypertension`
  - `do_not_resuscitate` = `do_not_resuscitate_status`
  - `malignant_neoplasm_of_breast` = `malignant_neoplasms_of_breast`
  - `accidental_exposure_to_other_specified_factors` = `exposure_to_other_specified_factors`
  - 2 pairs of eye and respiratory "intraop and postproc" complication flags
  - **`iliac_crest_spur__unspecified_hip` = `psoas_tendinitis__unspecified_hip`** (505 / 508 patients, two different diagnoses)
- **Near-duplicates: 23 pairs with Jaccard ≥ 0.98, 65 with ≥ 0.95.** These come from the hierarchy (a description against its category, e.g. `ascites` / `other_ascites`). Fine for trees; no action.
- **The ICD-9 conversion explains several oddities.** The paper states "all ICD-9 codes were converted to ICD-10 codes". One ICD-9 code that maps to many ICD-10 codes explains the identical hip pair (ICD-9 726.5 becomes M76.1x and M76.2x), the hyperesthesia / hypoesthesia near-pair, and very likely the anomaly note's T63 "venomous animals" bulk (ICD-9 989.5 maps to every T63 code). The note could name this mechanism. It is balanced between classes, so no change is needed.
- **The "-1" code.** 1,293 patients (668 cases, 625 controls) carry the code `-1`, a missing-value placeholder. It is one of the "two codes not in the map" in the comment (the other is N35.81). It gives no flag, so the data is fine, but the wording "22,220 of the 22,222 distinct codes" counts the placeholder as a code. Wording fix only.
- **dtype probe: 0 flagged.** Every feature holds only 0 and 1, and no patient has zero kept flags.

**Experiments (a cluster run)**

| Variant | rows | flags | LightGBM | LogReg |
|---|---|---|---|---|
| A shipped | 15,394 | 1,740* | 0.837 | 0.814 |
| G − companion (J99 etc.) − transplant flags | 15,394 | 1,737 | 0.829 | 0.810 |
| H − 35 ICH / cerebral-oedema flags | 15,394 | 1,730 | 0.829 | 0.805 |
| I − cases with I60–I62 (the paper's case definition) | 14,596 | 1,703 | 0.834 | 0.814 |
| I2 − all patients with I60–I62 | 14,233 | 1,703 | 0.834 | 0.816 |
| B − cardiomyopathy family (builder's run) | 15,394 | 1,733 | 0.829 | 0.806 |
| B2 − CM family − I50 subtypes (builder's run) | 15,394 | 1,718 | 0.818 | 0.795 |

Shipped LightGBM scored on subgroups: **ICH cases against all controls 0.915; the other cases against all controls 0.828.**

*Before the 7 duplicate flags are dropped; the builder's variants likewise.

**Problems, ranked**

1\. **J99 is a companion code, kept (LEAK-10, Must).** `respiratory_disorders_in_diseases_classified_elsewhere` is a manifestation code: ICD-10-CM requires the underlying disease (here amyloidosis) to be coded first, the same mechanism as the dropped I43. It is 1 in 180 cases and 11 controls (2.3% / 0.1%, LR 16). It passes the 2% rule by 0.3 points, so it is a near-pure leaf for a tree model.
   - Remedy (mildest): add it to the dropped flags beside the source's two. Better still, state a rule: drop every "in diseases classified elsewhere" manifestation flag whose code-first note names amyloidosis. Today only J99 passes 2%.
   - The score cost is measured together with problem 2: 0.837 → 0.829.
2\. **Heart transplant status is a consequence of the diagnosis (LEAK-10 / USE-3, Must).** `heart_transplant_status` (Z94.1) is 2.0% of cases and 0.2% of controls. In amyloid cardiomyopathy a transplant follows the diagnosis or is the event that makes it. The undiagnosed patient the use case scores has none.
   - Remedy: drop `heart_transplant_status`.
   - `transplanted_organ_and_tissue_status` (the Z94 group: 3.1% / 1.4%, mostly heart) is mixed; dropping it too is the cleaner cut, but it is the curator's call.
3\. **Intracranial haemorrhage marks a case subgroup that may not be cardiac amyloidosis (target validity; a question for the curator).** The paper's case definition for Cohorts 3–5 excludes "cerebral amyloid angiopathy, or intracranial hemorrhage", but the file's cases hold 798 with I60–I62 (10.4% against 4.7% of controls). This is already noted in `curation_comments`. New evidence:
   - The profile is that of cerebral amyloid angiopathy, for which E85.4 is the underlying code: lobar (cortical) ICH 238 / 17 (LR 14), cerebral oedema 283 / 53 (LR 5.3), compression of brain, neglect, aphasia.
   - **484 of the 798 ICH cases carry no I42 or I43 code at all.** 2,359 cases (30.6%) have no cardiomyopathy code of any kind.
   - The shipped model scores those cases at 0.915 against 0.828 for the rest, so the subgroup inflates the score.
   - The ICH flags rank among the top case markers by ratio. Dropping them costs 0.008. Applying the paper's exclusion costs 0.003 (0.834), whether only the cases are dropped or both classes; both classes avoids creating a new case-only marker.
   - The paper's 7,296 cases against the file's 7,697 (401 more) fit an exclusion that was not applied to the file, but do not prove it.
   - Options: (a) keep, and state that the label includes probable CAA cases; (b) drop patients with I60–I62 from both classes, the paper's definition made symmetric (0.834).
   - Mildest remedy that follows the source: (b).
4\. **The cardiomyopathy and HF-subtype families (issue 1, settled as A; reopened on purpose).** New evidence for the discussion:
   - The family is not uniform. HCM (I42.1/I42.2, 7.6% / 1.3%) is an antecedent per the paper ("initial misdiagnoses ... preceded the ATTR-CM diagnosis").
   - Restrictive / other / unspecified (I42.5/I42.8/I42.9) are the codes the work-up writes.
   - End-stage HF (I50.84, 1.6% / 0.2%) and acute-on-chronic HF codes follow the disease course.
   - A narrower cut keeps I42.1/I42.2, drops I42.5/I42.8/I42.9 and `end_stage_heart_failure`, and would sit between A (0.837) and B (0.829). It was not run.
   - Not relitigated; for the issue's table.
5\. **The flags are typed numeric (CLEAN-14, Should).** `_feature_types` returns `FeatureTypes()` with the comment "kept numeric". CLEAN-14 says a 0/1 column whose meaning says it is a yes/no flag is categorical (zillow's presence flags are the precedent). These are presence flags of named diagnoses.
   - Remedy: type all 1,733 categorical, or give the reason for numeric in the definition.
6\. **Minor wording.**
   - The "22,220 of 22,222 codes" bullet counts the `-1` placeholder (1,293 patients) as a code.
   - The T63 anomaly can name the ICD-9 to ICD-10 conversion as its likely cause.

No leak was found in the remaining families. The antecedent red flags (carpal tunnel, tenosynovitis, spinal stenosis, conduction disease, flutter, pericardial effusion) are the paper's own predictors and fine. The work-up findings (R93.1, R77, R74) are weak and covered by the whole-history note. The name cleaning and the duplicate drop are correct.

</details>

<details><summary>Split audit</summary>

**Split audit: wild_type_attr_cardiac_amyloidosis**

**Verdict: right with notes.** The split is 3 x 3-fold, stratified (every test fold holds 50.0% cases), on 15,394 patients. No hidden group, matched-pair structure or near copy across the folds moves the score. The only point for a reviewer is the forced leaf itself.

**Tree walk (SPLIT-36)**

- Type `Clinical Study`: a study cohort drawn from a claims extract. `Database Snapshot` would also fit, and it reaches the same leaf through [DB.meets] and the place step.
- [CLI.meets]: another health system. The source validated on Optum and Northwestern, "the setting in which it would be used clinically".
- **Place step.** [PLACE.several]: no. The file comes from one source and has no site, region or practice column.
- [PLACE.units]: no. There is one row per patient (0 duplicate `patient_id`s).
- This reaches **L-PLACE.random** (`ForcedIIDFromGrouped`). That is the `split_leaf` the definition names, with a group basis and a time basis that says later patients are not tested (the rule for a use case that meets both another place and a later time). The definition ships the leaf's split and tag.
- **Other branch.** "Same database, later patients" leads to [CLI.dated] no, then to the order step. No order can be rebuilt:
  - in the raw file order, the next row has the same label 49.7% of the time;
  - the numeric `patient_id` scores ROC AUC 0.481 as a predictor;
  - the time probe is flat (p 0.63).
- That branch ends at [L-FORCED.random], so it is random too. The decision does not hinge on which branch is taken.

**Checks**

| Check | Result |
|---|---|
| Stratification | test case share 0.4999 to 0.5001 in all 9 folds |
| Matched pairs (1:1 propensity on age, sex, history length, visit count) | No pair id is released, and none of the matching variables is a feature. The nearest neighbour (Jaccard on the shipped flags) has the same label 59.5% of the time: above chance, not below, so the matched partner (opposite label) is not what the nearest neighbour finds. Splitting pairs across folds cannot be exploited. The number of flags alone scores ROC AUC 0.548, so the visit matching mostly holds. |
| Near copies | Median nearest-neighbour Jaccard 0.31, 99.9th percentile 0.63. 6 rows lie in groups at Jaccard >= 0.8. The 2 exact-duplicate pairs agree on the label in 1 of 2. |
| Grouped alternative (near-copy components at >= 0.8, StratifiedGroupKFold 3-fold) | LightGBM ROC AUC 0.837 (0.835, 0.841, 0.836), against 0.837 on shipped repeat 0 (0.832, 0.840, 0.841). No change. |
| T63 artefact patients | 58 patients carry 20 or more T63 codes (53% cases). Every T63 flag fails the 2% case rule (about 0.7% of cases), so the shipped features hold no T63 column and the artefact cannot form a cluster across the folds. |
| Leave-one-out 10-NN label share | ROC AUC 0.726, below LightGBM's 0.837. The signal is spread across many flags, not carried by neighbours. |
| Overlap with the derivation file | 597 patients (505 cases, 92 controls) are also rows of Huda's `training_input`. That file is not shipped, so nothing crosses this split. Shipping both would be a cross-dataset leak (PROV-6). |

Scripts and output:
- script: (a script in the run folder)
- output: (the run folder) (a cluster run)

**Problems, ranked**

1\. **The leaf is forced and no definition has reached it before (SPLIT-36, SPLIT-35; Should).**
   - The use case is another health system, which this data cannot test. The source's own drop from 0.93 to 0.80 at Northwestern shows that the step matters.
   - **Remedy:** none is possible on this data. The group basis already says that the score is optimistic for another system.
   - **For the curator:** the main session should list the issue as a forced leaf that no v0.2 definition has reached yet, so the curator can confirm it. This is not a defect.
2\. **The record's Screening `Split:` line still describes the derivation file.** It says 2,142 patients, an 80:20 source split, and that the "derivation file holds one source".
   - The leaf is unchanged.
   - **Remedy:** add an Assessment line that restates the split for the validation file (15,394 patients, the same leaf) so a reader does not take the old line as current. This is wording only.
3\. **(Note, not a split defect.)** The lifetime flags (`Features: Read Later`) mean the folds mix pre- and post-work-up codes. No split can remove them. This is issue 1 of the review (USE-3, LEAK-10), not this audit's remedy.
4\. **(For the claim auditor.)** Check whether the group basis's "0.93 on its IQVIA holdout to 0.80 at Northwestern" refers to the wild-type ATTR-CM model rather than the Cohort 3 label shipped here. If it does, it should say so. I did not verify this.

No re-split, gap or filter is recommended.

</details>

<details><summary>Domain practitioner</summary>

**domain-practitioner: `wild_type_attr_cardiac_amyloidosis`**

I took the role of a cardiologist, or a payer or health-system screening programme, that scores heart-failure patients on their coded claims history and refers the high scorers for bone scintigraphy. Everything below comes from reading files and light pandas inspection on the login node. I fitted no model. My notes are in (the run folder).

**Fit: approximate (USE-8).** I agree with the definition, but the case is weaker than the stated `fit_reason` says. The decision and the actor are real: the paper's Discussion says the model is for raising suspicion in heart-failure patients before confirmatory testing. Three things weaken it:
- The target is any single amyloidosis code. It is not confirmed cardiac amyloidosis, and for 47% of cases nothing in the list links the code to the heart.
- The history includes the codes written during the work-up.
- The sample is 1:1 matched.

**Gaps, ranked by how much they change the task**

1\. **The target is a proxy, and a noisy one (USE-5). This is the largest gap.**
   - What I act on is scintigraphy-confirmed ATTR cardiomyopathy, which is the one eligible for tafamidis. The label is instead "the list holds E85.4 or E85.82".
   - The code lists are sets: no list repeats a code. So I cannot apply the usual claims rule for a validated diagnosis, which needs two or more outpatient claims or one inpatient claim. One mention is enough to make a case, and that includes a code entered to rule amyloidosis out when a test is ordered.
   - Cases with neither I43 nor E85.82 (no code linking the amyloidosis to the heart): 3,593 of 7,697 (47%).
   - Cases whose only amyloidosis code is E85.4, with no I43 either: 2,678 (35%). E85.4 means "organ-limited", which also covers localized amyloid of the bladder, skin, larynx or gut.
   - 783 cases also carry hereditary or secondary systemic codes (E85.1 in 716, E85.3 in 783). Hereditary ATTR goes through a different pathway (genetic testing). Secondary AA amyloid is not a disease I would send for scintigraphy.
   - So "cardiac amyloidosis" in the `task_summary` overstates what the label holds. The paper does define Cohort 3 this way, so the label is faithful to the source.
   - An expert would tighten the label to E85.82, or E85.4 together with I43. That leaves 4,104 cases; the 3,593 cases without that link would be dropped, not relabelled. This is our own redefinition, so it needs the curator.
   - A nuance: I43 is removed from the features as a leak, but here it would only select which rows count as cases. That is allowed.
   - It costs balance: the classes go from 7,697:7,697 to 4,104:7,697.
   - I have not run it. The next step is to score this variant on the cluster.

2\. **The prediction point: the history includes codes from the work-up (USE-3, USE-4, LEAK-10).** This bears on settled issue 1; I am adding evidence, not reopening it.
   - At referral I would have the history up to today. That includes heart failure, atrial fibrillation, CKD and the real early signs: carpal tunnel G56.0 (13.8% of cases against 5.1% of controls), bilateral carpal tunnel G56.03 (2.4% against 0.8%), lumbar stenosis M48.06 (20.1% against 14.8%).
   - I would not yet have the codes that echo, MRI and the amyloid work-up write:

     | Code | Cases | Controls |
     |---|---|---|
     | I42 cardiomyopathy | 51.9% | 26.5% |
     | I51.7 cardiomegaly | 49.1% | 33.0% |
     | R93.1 abnormal heart imaging | 6.6% | 2.8% |
     | R94.31 abnormal ECG | 42.8% | 34.0% |
     | the more specific I50.3x HFpEF codes | (counted in the builder's probe, not by me) | |

   - The builder's single-feature leak probe ranks almost only cardiac and work-up flags at the top: `cardiomyopathy` 0.627, `cardiomegaly` 0.581.
   - Dropping the cardiomyopathy family costs little: LightGBM 0.837 → 0.829 (`variants.json`). So the harm from the work-up codes is moderate.
   - No index date is released, so a clean cut before referral cannot be built.
   - The history is shorter than the row text says. No list holds a single ICD-9 code (0 of 15,394), although the paper says ICD-9 codes were extracted. So the history covers the ICD-10 era only, from October 2015, not 2008 to 2019. The row text ("2008 to April 2019 ... every diagnosis code of the patient's history") should say this; it is a claim for the claim auditor.

3\. **The sample is not the population I screen (Selection Bias, already a record marker).**
   - The real prevalence is 0.7% (261 of 39,654 at Northwestern), or about 4% pre-test probability according to the paper.
   - The 1:1 matching removes age and sex. In practice those are strong priors: wild-type ATTR is mostly in older men.
   - 785 controls (10.2%) carry exclusion diagnoses that the source's case-only exclusion rules out for every case. My real population would not be filtered that way.
   - The controls have no amyloid code at all, but undiagnosed cases sit among real heart-failure patients.
   - The source's own model fell from ROC AUC 0.93 to 0.80 at Northwestern. The definition already discloses this.

4\. **The test data is not what I would face (already disclosed).**
   - The test patients are random patients from the same database. I would face another system and later patients.
   - The window ends in April 2019, before tafamidis was approved in May 2019. After that, testing and E85.82 coding rose sharply.
   - E85.82 was usable for only a few months of the window; coding sites give 1 October 2018 as its start. I did not check that date against the CMS addenda.
   - One row matches one referral decision, which fits. The decision happens at one moment, and the row has no time cut.

**Would I use the model?**

Yes, as a flag that raises suspicion in a claims-based programme; never on its own.
- I would trust it if its signal came from real early signs: carpal tunnel, spinal stenosis, conduction disease, pericardial effusion.
- I would distrust it because a third of the positives may not be cardiac amyloid at all, and because the strongest inputs are codes the work-up itself writes.
- A clinic would also have NT-proBNP, troponin, echo wall thickness and low ECG voltage. A payer would not, so for a payer, codes only is realistic.

**Metric: partly scores my decision (MET-1, MET-6, MET-8, MET-9)**

- My decision is which few percent of heart-failure patients get referred within scintigraphy capacity. What matters to me is the precision (PPV) among those top few percent, at a prevalence between 0.7% and 4%. That sits in the high-specificity, low-false-positive part of the ROC curve.
- The ideal measure would be precision at k at the true prevalence. It cannot be computed on a 1:1 matched set, and neither can a PR AUC: both depend on the prevalence, and a matched set's floor is 0.5.
- Log loss would score calibration at a 50% prevalence that I never meet.
- ROC AUC does not depend on the prevalence, so it is the only honest choice this sample supports. The source reports several metrics and fixes no threshold by a decision, so the fallback is right under MET-5 and MET-8. Imbalance at deployment alone is no reason to switch under MET-9.
- What I would choose: keep `roc_auc`. If the framework allowed it, a partial ROC AUC up to a 10% false-positive rate, or the sensitivity at 90% specificity, would match the screening decision better. No rule requires either, so this is a note, not a change.

**What an expert would change, in order**

1. Tighten the label to E85.82, or E85.4 together with I43, and score that variant against the shipped one. This needs the curator (USE-5).
2. Correct the history description to "ICD-10 codes only, roughly Oct 2015 to the end of the extract".
3. On issue 1 (now reopened), add `cardiomegaly` and R93.1 to the work-up family the curator is weighing.
4. Add a note that age and sex are matched away, so deployment needs a prior that this score cannot carry.

**Sources**

- Huda et al. 2021, PMC8113237 (`panel/../paper/pmc.html`): Methods "Dataset curation", Tables 1 to 4, Discussion.
- The raw `ca_validation_group_input` file and the builder's `variants.json` and `leak/*.json`.
- E85.82 effective date, from coding sites only, not official: https://www.veroscribe.com/icd-10/codes/E85.82, https://icdlist.com/icd-10/E8582
- Rules cited: USE-3, USE-4, USE-5, USE-8, LEAK-10; MET-1, MET-5, MET-6, MET-8, MET-9.

</details>

<details><summary>Blind review</summary>

**Verdict**

**Include with changes** — it is real, well-prepared claims data with honest, non-trivial signal (LGBM 3×3 CV AUROC 0.835 ± 0.005), and I could reproduce the entire table bit-for-bit from the paper's public Source Data, but the task card must stop implying a prospective clinical prediction and the dataset must be renamed, because the label is an ICD code drawn from the same undated code list that generates the features.

---

**What I did**

Reconstructed the prepared table from scratch out of the public Source Data zip (`41467_2021_22876_MOESM4_ESM.zip`), which contains `ca_validation_group_input (IQVIA validation dataset).csv` (15,394 rows of `patient_id` + a comma-separated raw ICD-10 string, **no label column**), `icd_map.csv`, and the two Jupyter notebooks. Result:

- Label reproduced **exactly**: `cohort_flag = 1` iff the patient's code string contains `E8582` or `E854` (Model Validation.ipynb, cell 18) → 7,697 / 7,697, matching `data.parquet` to the row.
- Features reproduced **exactly**: explode codes → join `icd_map.csv` → melt `short_desc`/`major`/`sub_chapter` → lowercase/slugify → restrict to the model's feature list. After removing feature contributions coming from `E85*` codes, **all 1,733 column prevalences match the released parquet with zero differences**, and 15,390/15,394 rows hash-match with 100% label agreement.

So the provenance is confirmed and the preparation is faithful.

---

**Concerns, most to least serious**

**1. No temporal separation: the label is a code inside the same record that makes the features**

The validation file is an undated bag of ICD codes per patient. The target is "this bag contains E85.4 or E85.82 (plus a heart-failure code)". Nothing restricts features to the period before the amyloidosis code, and there is no index date for controls at all. The paper gives only database-wide observation windows (`1 January 2008 to 30 April 2019`), never a per-patient lookback.

The fingerprints of post-/peri-diagnosis coding are visible in the raw codes (cases vs controls, n=7,697 each):

| raw code | meaning | cases | controls |
|---|---|---|---|
| `I43` | Cardiomyopathy in diseases **classified elsewhere** | 4,037 | 111 |
| `J99` | Respiratory disorders in diseases classified elsewhere | 180 | 11 |
| `Z941` | Heart transplant status | 155 | 12 |
| `I611` | Nontraumatic intracerebral hemorrhage, cortical (CAA) | 238 | 17 |
| `L99` | Other skin disorders in diseases classified elsewhere | 121 | 0 |

`I43` alone is a 97%-precision label proxy. **The good news:** the preparer (and the paper's own feature selection) already closed the worst channels — I verified `cardiomyopathy_in_diseases_classified_elsewhere`, `other_forms_of_heart_disease`, `light_chain__al__amyloidosis`, `monoclonal_gammopathy`, `end_stage_renal_disease` and `oth_disorders_of_skin__subcu_in_diseases_classd_elswhr` are **absent** from the 1,733 columns, so `I43` and `L99` contribute literally nothing. The paper's own notebook names these: `potential_target_leaks = ['cardiomyopathy_in_diseases_classified_elsewhere','other_forms_of_heart_disease']`.

What remains is modest. Ablations (3-fold, LGBM):

| feature set | AUROC |
|---|---|
| all 1,733 | 0.835 |
| minus `respiratory_disorders_in_diseases_classified_elsewhere`, `heart_transplant_status` | 0.826 |
| minus all 8 `*cardiomyop*` columns | 0.827 |
| minus cardiomyopathy + all heart-failure + the two above (1,705 left) | 0.806 |

So no single column carries the task; the signal is broad and survives aggressive ablation.

**Change:** drop `respiratory_disorders_in_diseases_classified_elsewhere` (J99) and `heart_transplant_status` (Z94.1) — both are consequences of having the diagnosis, cost 0.009 AUROC, and are indefensible as predictors. Keep the rest. In `task.md`, state plainly that features and label are drawn from the same undated claims record and that this is a **record-classification** task, not early detection.

**2. The dataset is misnamed: this is not the wild-type ATTR cohort**

The folder is `wild_type_attr_cardiac_amyloidosis`, but the label is `E854` (organ-limited amyloidosis, not specifically cardiac) or `E8582`. **All 7,697 cases have `E854`; only 516 (6.7%) have the wild-type ATTR code `E8582`.** This is the paper's *general cardiac amyloidosis validation cohort* (Cohort 3), described as "patients with organ-specific amyloidosis (ICD-10 code E85.4) and HF" intended to capture "cases that had wild-type **or hereditary** ATTR-CM but were coded as the more general cardiac amyloidosis term." The ATTRwt derivation cohort is the *other* file in the same zip (`training_input`, 2,142 rows × 1,877 columns, with an explicit `cohort_type` of `Wild Type`/`Control Group`).

**Change:** rename to something like `cardiac_amyloidosis_icd_claims`; the target column name `cardiac_amyloidosis` is fine, the folder/task name is not. Note in `task.md` that the label is a code-based proxy — the paper's own limitation: "our study is limited by the use of ICD codes ... as the gold standard for assigning cases and controls."

**3. 1:1 propensity-matched case-control — prevalence and threshold metrics are meaningless**

Exactly 50% positives. In the paper's unmatched real-world EHR cohort the prevalence was 261/39,654 and **PPV at threshold 0.5 was 1.9%**. Matching was on "age, gender, duration of medical history in the database, and number of healthcare visits", which is why age and sex are absent from the table and why the trivial volume baseline is dead: **AUROC from row-sum (number of distinct features) alone = 0.548**, despite cases averaging 201 codes vs 183 for controls.

**Change:** score with AUROC/AUPRC only; do not report accuracy or PPV as if clinically meaningful, and say in `task.md` that this is a matched case-control sample with an artificial base rate.

**4. Cohort-construction exclusions are one-directional**

Several codes appear in controls and in **zero** cases — an artifact of excluding AL-amyloidosis mimics from the case arm ("we excluded blood cancers and other non-ATTR-related amyloidosis terms"): `N186` ESRD 0/498, `D472` MGUS 0/136, `E8809` 0/161, `C9000` myeloma 0/70, `E8581` AL amyloidosis 0/0. By construction, "has MGUS ⇒ control" is a certainty.

Severity is low only because none of those codes has its own feature column; the effect is diluted into broad parents: `chronic_kidney_disease__ckd_` 0.552 (case) vs 0.459 (control), `malignant_neoplasms_of_lymphoid__hematopoietic_and_related_tissue` 0.026 vs 0.044. Worth one sentence in `task.md`; no change to the data.

**5. Two label-contradicting duplicate pairs**

4 rows form 2 pairs that are **identical across all 1,733 features but carry opposite labels** (`[No, Yes, Yes, No]`). No other duplicates (3 duplicated feature rows total, 2 fully-duplicated rows including target). This is 0.03% of the data — a negligible irreducible error floor, not a leak — but random CV will place partners on both sides. **Change:** optional, drop the 4 rows.

**6. Split regime**

`IID (random rows)` over 3×3 folds is right for the data as it stands (~5,131 test rows/fold, ~2,566 positives — plenty to score). The one caveat: matched pairs get split across folds. The partners are distinct patients, so this is a weak dependency, not a copy; I'd leave it.

**7. Small unreconciled provenance discrepancy**

The paper reports Cohort 3 as **7,296 cases / 7,296 controls**; the released Source Data file has **7,697 / 7,697**, and all 15,394 patients already satisfy the notebook's heart-failure filter (I checked: 15,394/15,394 carry an `I50*` code). I could not account for the 401-per-arm difference. It doesn't affect the table's validity but should be noted so nobody tries to match the paper's numbers.

---

**What is fine**

- **Real data, not generated.** Heavy-tailed, realistic claims structure (median 184 codes/patient, max 1,034), plausible comorbidity co-occurrence, and the whole table reproduces from the published Source Data.
- **Signal is in the right band.** LGBM 0.835, logistic regression 0.810, trivial baseline 0.548. Not trivial, not saturated. For reference the paper got AUROC 0.76 on this cohort with a model trained on the *other* cohort; in-domain CV at 0.835 is consistent.
- **Top features are clinically coherent**, not junk: `cardiomyopathy` (0.519 vs 0.265), `cardiomegaly` (0.491 vs 0.330), `chronic_diastolic_CHF`, `pleural_effusion`, `atrial_fibrillation_and_flutter` (0.655 vs 0.514), `mononeuropathies_of_upper_limb` (0.176 vs 0.075), `carpal_tunnel_syndrome__bilateral` (3.2× enriched) — the textbook ATTR red flags; controls are enriched for diabetes, COPD and CABG.
- **Preparation is clean and shows real care.** All features `int8` ∈ {0,1}, target an ordered-free `category` with `['No','Yes']`, zero NaN, no constant columns, minimum column prevalence 167 (1.1%), 26.7 MB in memory. Critically, the preparer **found and fixed a genuine leak I would have flagged**: `E85*` codes map up to sub-chapter `Metabolic Disorders`, so every case would mechanically have `metabolic_disorders = 1`. The raw mapping gives 14,626 positives for that column; the released file has 13,895 — a difference of exactly 731 — and once I removed `E85`-derived contributions, all 1,733 prevalences matched exactly. Post-fix it is 0.905 (case) vs 0.900 (control). Correctly handled.
- **No training-weight column** is declared in `task.md`, and none is needed for a balanced matched design.

---

**What I could not check**

- **The crux: timing.** The released file has no dates, so I cannot measure what fraction of feature codes precede the amyloidosis code. Everything in concern #1 is inference from code semantics and prevalence ratios, not from timestamps. The paper asserts in a figure caption that "all diagnoses included here preceded the ATTR cardiomyopathy diagnosis" — that claim is about the derivation cohort and is unverifiable for this file.
- **Whether the 1,733 columns are exactly the paper's model features.** `feature_importance.csv` and `rf_best_excl_1_CM_3_6.sav` are referenced by the notebook but are **not in the Source Data zip**. I confirmed the 1,733 names are a subset of the 23,861 names the mapping generates and that each reproduces exactly, but I cannot confirm the selection rule, and I cannot rule out that other manifestation-style columns were retained that the authors meant to drop.
- **nature.com is behind a login redirect** (303 to `idp.nature.com`), so I read the paper via PMC8113237 and resolved the other two DOIs through the Crossref API only. Link 2 (`s41467-024-45879-8`) is the ChatGPT-ADA-vs-manual-ML paper; link 3 (`s12911-026-03654-3`) is a 2026 BMC benchmark of TabPFN against twelve ML methods on twelve binary clinical tasks. I read only their abstracts, so I cannot say how either preprocessed this table or whether their numbers are comparable.
- **Whether the underlying IQVIA records are genuine patients** — unauditable from outside; the distributional evidence is consistent with real claims.

I worked only from the clean room and the public web. I downloaded the Springer Source Data zip into the session scratchpad and did not open any other file on this machine.

</details>

<details><summary>Task gamer</summary>

**Verdict**

The task is **mildly gameable (≈ +0.008 to +0.016 AUC on a 0.835 baseline)** — the preparers correctly stripped the one big leak the original authors flagged (I43), but one manifestation code of the same class survives as its own column, and the cohort's case-exclusion rules leave a block of patients that are controls by construction; the split itself is clean and the published source file gives the label outright.

Baseline (untuned LightGBM on `features()`, 9 shipped splits): **0.83456** (per split 0.82860–0.83867, sd 0.00284).
Better honest model (LGBM 1000×0.03, 63 leaves, colsample 0.3): **0.83952**. Logistic regression: 0.81314.
Noise floor: adding one column of random numbers moves the mean by −0.0005 / −0.0006 / −0.0007 (3 seeds) ⇒ treat **|Δ| ≲ 0.0007 as noise**.

**Exploits**

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | `respiratory_disorders_in_diseases_classified_elsewhere` (ICD‑10 **J99**) — a dagger/asterisk manifestation code, codeable only once the underlying systemic disease is known. 180 cases vs 11 controls | `work/ablate.py`, `work/last.py` | 0.82647 (untuned) / 0.83172 (tuned) | 0.83456 / 0.83952 | **+0.0081** (9/9 splits, +0.0066…+0.0093); tuned +0.0078 | No | Drop the column (as was done for `cardiomyopathy_in_diseases_classified_elsewhere`) |
| 2 | Case-exclusion artefact: 797 controls (10.4%) carry a code **no case can carry** (N186 ESRD, E8809 plasma‑protein disorder, D472 MGUS, C9000 myeloma, C8588 lymphoma + dialysis Z-codes). Label-determined cohort membership | `work/oracle.py`, `work/final.py` | 0.82678 (train without those rows) | 0.83456 as shipped; **0.85063** with the flag decoded at test time | as-shipped **+0.0078**; ceiling **+0.0161** (9/9, +0.0142…+0.0173) | No | Apply the same exclusions to controls, or drop controls that meet a case-exclusion rule |
| 3 | Hierarchy-residual features: for each kit column *P*, `P==1 AND no in-kit child column ==1` ⇒ "patient has a code in this family that is not a model feature". 427 such columns, built from kit columns + the paper's public `icd_map.csv` | `work/resid.py`, `work/aug.py`, `work/final2.py` | 0.83952 (tuned) | 0.84079 | **+0.0013** (8/9 splits up; noise ±0.0007). Alone: AUC 0.599 | Partly — the ICD hierarchy is public, but what it decodes here is cohort construction | Ship only one hierarchy level, or ship the full child set for every parent |
| — | *Yardstick, already fixed:* restoring **I43** (`cardiomyopathy in diseases classified elsewhere`, 4037 cases vs 111 controls, univariate AUC 0.755) | `work/i43.py` | 0.83456 | **0.89142** | +0.0569 | No | Already removed by the preparers — correct |

**Flaws that hurt an honest model**

None found. The one honest choice I tested — dropping the 797 construction-determined controls from training — **costs** 0.0078 (0.83456 → 0.82678), because the test folds carry the same artefact. That is evidence for exploit 2, not a separate flaw.

**Mechanisms**

**1 — J99.** The kit is, row for row, the paper's published validation file; features are the patient's ICD‑10 codes mapped to three hierarchy levels (short description / major / sub-chapter), with every E85* code stripped first (I verified: `metabolic_disorders`, the sub-chapter of E85.4, is 90.5% in cases vs 90.0% in controls — it would be 100% in cases otherwise). The original authors removed `cardiomyopathy_in_diseases_classified_elsewhere` and `other_forms_of_heart_disease` as target leaks "that tend to accompany a cardiac amyloid diagnosis", and the kit does not contain either. But the asterisk family is larger: scanning the source codes whose description ends in *"in diseases classified elsewhere"* gives L99 skin 121:0, I43 4037:111, N33 bladder 30:1, **J99 respiratory 180:11**, K77 liver 56:3. Only J99 has a dedicated kit column — and it is the single highest-lift column in the whole table (2.34% of cases, 0.14% of controls, lift 10 after smoothing). L99/K77/N33 reach the kit only diluted into sub-chapters. Removing J99 costs 0.0081 on every one of the 9 splits, more than ten times the noise band, from a column present in 1.2% of rows. Mildest fix: drop that column.

**2 — exclusion artefact.** Cases were defined as E85.4/E85.82 + heart failure with blood cancers and AL-amyloid proxies excluded; controls were HF patients with no amyloid-related condition. In the raw source, five codes occur in ≥20 controls and **zero** cases: N186 (498), E8809 (161), D472 (136), C9000 (70), C8588 (20); dialysis Z-codes follow the same pattern (Z992 39:324). 797 controls carry at least one. None of these survives as a standalone kit column (no kit column has a zero cell), but the signature is diffuse and recoverable: a model predicting the flag from kit columns + residuals reaches AUC 0.941, and the strongest *negative* columns in the kit are exactly these families (`malignant_neoplasms_of_lymphoid…` lift 0.59, `other_and_unspecified_metabolic_disorders` 0.76, advanced-CKD/dialysis columns). Clinically this is backwards — an HF patient with MGUS or myeloma is a *prime* AL cardiac-amyloid suspect — so the model is learning the recruitment rule, not the disease. Flagging those rows perfectly adds 0.0161. Mildest fix: apply the same exclusion list to controls (or drop controls that would have been excluded as cases).

**3 — residuals.** Only 1,733 of ~98,000 hierarchy names are kit columns, so a parent column set with no in-kit child means "this patient has a code outside the feature set". The residual block alone scores 0.599 (its row-count alone only 0.525, so it is the pattern, not utilisation), it predicts the exclusion flag at AUC 0.657, and its sharpest members are exactly the cohort-definition families: CKD-parent-without-child 52 controls : 3 cases, dialysis-dependence residual lift 0.27, skin sub-chapter residual (where L99 hides) lift 2.2. Net gain is small because LightGBM already approximates it from the raw columns. Mildest fix: ship one hierarchy level only.

**Timing.** The Methods state only presence/absence of codes over the 2008–2019 window was used, with no index date, and a case is anyone coded E85.4 anywhere in that window — so features include the post-diagnosis period. The proof is in the data: 52% of cases carry I43, a code that by definition requires the underlying systemic diagnosis to already be on the record. That means other diagnosis-era cardiac columns are post-prediction-point for an unknown share of cases — `other_hypertrophic_cardiomyopathy` (lift 6.3), `pericardial_effusion__noninflammatory_` (4.2), `heart_transplant_status` (8.3), `other_restrictive_cardiomyopathy` (1.8). Dropping all seven cardiomyopathy columns on top of J99 costs a further 0.0073 (0.82647 → 0.81913). I do **not** rank these: the published file carries no dates, so I cannot tell a pre-diagnosis "misdiagnosed as HCM" code from a post-diagnosis relabel, and the paper asserts (Fig. 2 caption) that these diagnoses preceded the amyloid diagnosis. **The fact that would decide it:** each code's date relative to the patient's first E85.4/E85.82 date.

**Source lookup (not ranked).** The kit is exactly the paper's supplementary `ca_validation_group_input (IQVIA validation dataset).csv` — 15,394 patients, 7,697 of them case-flagged. I reconstructed the entire 15,394 × 1,733 matrix from that file and the shipped `icd_map.csv` and matched every kit row to its source patient by exact feature pattern (99.99% label agreement; 2 rows ambiguous because 2 duplicate patterns exist). The label is literally `'E854' in codes or 'E8582' in codes`, so the target can be read off the published file. That is a property of every public dataset, not of this task.

**Attacks that found nothing**

* **Formats** — all 1,733 columns are int8 ∈ {0,1}, no missing values, no sentinels, no duplicate columns. Nothing to mine.
* **Order and ids** — no id column; AUC of row position 0.5008; adjacent-row label agreement 0.5024 (max run 14, as expected for a shuffle).
* **Copies across the split** — only 2 duplicate feature patterns (4 rows), both with mixed labels. 1-nearest-neighbour training label as the prediction scores 0.589, far below the baseline: no matched-pair or near-copy leakage, despite the 1:1 propensity matching (which was on age, sex, history duration and visit count — none of which are features).
* **The test rows** — train-vs-test classifier AUC 0.4952 / 0.5009 on two folds: the IID split is clean.
* **Transforms over all rows** — row code count, its percentile rank, and an inverse-frequency rarity score, computed over train+test: alone 0.524, added to the baseline −0.0001. (Row count alone is AUC 0.548, 183 vs 201 mean codes — but a referral model sees the patient's code count, so that is signal.)
* **Amplifying a known leak** — adding α·J99 to the baseline probability (α = 0.1/0.3/1.0) gives 0.83456/0.83449/0.83444: LightGBM already weights it optimally.
* **Subtracting a kit-only exclusion proxy** from the tuned model: 0.83965 at α = 0.05, 0.83725 at α = 0.2 — no gain.
* **The weight** — `task.json` has `sample_weight: null`; no weight, no time column, no group column.
* **Columns from after the prediction point, taken one at a time** — strongest single column is `cardiomyopathy` at AUC 0.627; no column or shallow rule comes close to recovering the target.

**What I could not check**

* Whether any individual code predates or postdates the amyloid diagnosis — the published file is an unordered, undated code set. This is the one question that would turn the cardiomyopathy/pericardial-effusion/transplant block from "ambiguous" into a ranked exploit worth roughly 0.007 more.
* Whether the propensity match drew controls from a pool that was itself conditioned on anything beyond the four stated variables — the matching output (pair ids, scores) is not published.
* The third source link (`doi.org/10.1186/s12911-026-03654-3`) is behind a Cloudflare JavaScript challenge and I could not retrieve it; any criticism in that paper is unread. The other two links I read in full (PMC8113237; the 2024 Nature Communications paper is the LLM-AutoML benchmark that packaged this dataset, not an amyloidosis study).

Sources: [Huda et al., Nat Commun 2021 (PMC8113237)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8113237/) · [nature.com/articles/s41467-021-22876-9](https://www.nature.com/articles/s41467-021-22876-9) · [Supplementary code+data (MOESM4)](https://static-content.springer.com/esm/art%3A10.1038%2Fs41467-021-22876-9/MediaObjects/41467_2021_22876_MOESM4_ESM.zip) · [nature.com/articles/s41467-024-45879-8](https://www.nature.com/articles/s41467-024-45879-8)

</details>

<details><summary>Precedent check</summary>

**Precedent check: `wild_type_attr_cardiac_amyloidosis`**

I ran the register (`panel/register.json`: 7,375 decisions, 46 flags). None of its 46 flags concerns this dataset. The LEAK-10 "exception to a Must" flag is about loan_default_prediction_imperial_college, where Andrej on 2026-11-03 kept aggregates of a measured leak out as a block. I compared this dataset against SAheart, stroke_prediction, cdc_diabetes_health_indicators, distribution_transformers_at_cauca_department, home_credit, qsar_bioconcentration, numerai, gallstone, pheochromocytoma and deafness. No medical sibling built from claims or code histories exists: every "claims" hit in the register is insurance, and every other record tagged `Features: Read Later` is non-medical. I ran no compute and used the builder's `variants.json`.

**Per decision**

| # | Decision | Verdict | Closest precedents |
|---|---|---|---|
| 1 | Lifetime code flags with an undated past-diagnosis label, kept as a screening task | **departs, reason not written down** | SEL-7: cdc_diabetes_health_indicators (Lennart, 2026-10-15) and stroke_prediction (2026-10-26). south_africa_coronary_heart_disease, retired by Andrej on 2026-11-10: "a model learns who has had one, not who will, and no screening decision uses it" |
| 2 | Cardiomyopathy family (I42 and others) kept as "Potential leak, kept on purpose" (issue 1 A, which the curator asked to reopen) | **departs from LEAK-10 (a Must), reason not written down**. LEAK-11 does not cover it, because the family raises the score (LightGBM 0.837 with it, 0.829 without, B2 0.818) | distribution_transformers_at_cauca_department (Lennart, 2026-10-21): values changed after the outcome for an unknown subset of positives are dropped, "no amendment for a gain that may sit on the changed rows". SAheart is a LEAK-11 keep only because there the late values weakened the signal |
| 3 | The 2% case-prevalence rule computed on all cases, test folds included, kept with a note | **departs from LEAK-31's "remove it when we can"**. The stated reason is "it is the source's rule", but we rebuild it ourselves | LEAK-31 removals: home_credit (our own pipeline, 2026-10-19), qsar_bioconcentration (2026-10-26), numerai_v5_2_1m (2026-10-26). LEAK-29 (Must, our own cleaning never computes from all rows), sf_permit_time and home_credit |
| 4 | 1:1 propensity-matched sample, `Selection Bias`, prevalence 50% | consistent | the Selection Bias set of 2026-10-20 (hepatitis_c, early_stage_diabetes, SAheart). The no-marker exception (credit_g, amex) covers class oversampling only, and matching on visits is more than that |
| 5 | 785 controls (10.2%) with conditions the source excluded from the cases only (ESRD, MGUS and others) kept, because dropping them changes nothing (0.837 both ways) | consistent | LEAK-13's "first measure how much the fix removes". The minimal-preprocessing rule: fix only what separates the classes for non-target reasons |
| 6 | Split `L-PLACE.random`, time basis `ForcedIIDFromTemporal` | consistent | pheochromocytoma_paraganglioma_metastasis (same leaf, same time basis), deafness_gene_carrier_hearing_loss |
| 7 | Validation file used instead of the derivation file, label from E85 codes, all E85 codes removed | consistent with the settled issue 2 c and PROV-6 | none |
| 8 | Metric: fallback `roc_auc` | consistent | MET-1, MET-5, MET-6 |
| 9 | 2 exact duplicate feature rows kept | consistent | none |

Side note on decision 7: the record's `name` and the `unique_name` still say "wild type ATTR", but the label is now any cardiac amyloidosis. Every case holds E85.4 and only 516 hold E85.82. The `## Review` **Outcome** line also still describes the 2,142-patient file. The editor should fix both.

**Reflection prompts (record-review issue shape)**

**R1. Is a coded history read over the whole lifetime, with an undated past-diagnosis label, a screening task, when SAheart, stroke and cdc_diabetes were retired as look-backs?**

* **Problem:**
  - The label is an amyloidosis code the patient already carries. The flags cover the whole history, including the time after the diagnosis ("not the temporal sequence", Methods). That is the SEL-7 pattern: stroke_prediction was "a stroke the patient already had, undated", and "a screening task would need a first stroke within a horizon, from dated records".
  - Andrej retired SAheart on 2026-11-10 because the cases were measured after the event. Here the work-up codes are written after the event as well.
  - What may set it apart: the source names a screening decision and validated the model in another system (NMEDW). Its Fig. 3 shows non-cardiac phenotypes (carpal tunnel, spinal stenosis) present years before the ATTR-CM diagnosis. Without the cardiomyopathy and HF-subtype codes the score stays at 0.818 (LightGBM), against 0.837 shipped.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | Keep. Record the distinguishing fact: a source-named screening use, external validation, and signal mostly from codes that come years before the diagnosis | follows the source's task; the fact can be checked against the paper | the antecedent claim cannot be tested on this release, because it has no dates |
  | b | Keep, but only with the issue 1 B or B2 drop, so the look-back codes go | closer to the SEL-7 requirement; costs 0.008 to 0.019 AUC | our own cut; late non-cardiac codes stay in |
  | c | Retire under SEL-7 (`No Good Target / Scientific Discovery`) like SAheart | consistent with three retirements | loses the only screening dataset that has a named actor and an external validation |

* **Recommendation:** b, with the distinguishing fact from a written into the record, so that SEL-7 gets an explicit exception instead of silent drift.[^sel7]

**R2. Keep the cardiomyopathy family when it raises the score?** This goes into the reopened issue 1.

* **Problem:** LEAK-11 keeps a late value only when it weakens the signal. Here it strengthens it (+0.008). distribution_transformers set the rule: drop values that changed for an unknown subset of positives.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | Keep (A as implemented), with an amendment to LEAK-10 for coded histories | keeps the paper's features | a third kind of exception to a Must |
  | b | Drop the family (B) | follows distribution_transformers | removes real antecedent cardiomyopathy codes too |

* **Recommendation:** b.[^leak10]

**R3. Build the 2% rule without labels or per fold?**

* **Problem:** we compute the selection ourselves from raw codes, and LEAK-31 and LEAK-29 say "remove it when we can". The label-free rule (2% of all patients) scores 0.839, against 0.837 shipped, so we lose nothing.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | Keep Huda's rule on all cases, as resolved in issue 2 c | matches the source exactly | departs from home_credit, qsar_bioconcentration and numarai |
  | b | Use the label-free 2%-of-all-patients rule | no label use, same score, follows the precedents | departs from Huda's selection |

* **Recommendation:** b. The curator settled the build in issue 2 c, so this goes to the curator for a decision rather than being changed by us.[^leak31]

[^sel7]: **SEL-7** (Must): a label the respondent already knows is predicted by nobody; a screening task needs positives that do not know yet.
[^leak10]: **LEAK-10** (Must), with **LEAK-11** (Should): a late value stays only when it weakens the signal.
[^leak31]: **LEAK-31** (Should): supervised feature selection on the full labelled set is measured, and removed when we can. **LEAK-29** (Must): our own cleaning never computes from all rows.

No files were written. Sources: the record (the SAheart record is in the same folder as `south_africa_coronary_heart_disease.md`), the builder's scores in (the run folder), and the rules in the knowledge-curation references (`selection.md` for SEL-7, `leak_checks.md` for LEAK-10/11/29/31).

</details>

<details><summary>Advocate (brief and rebuttal)</summary>

**Advocate: wild_type_attr_cardiac_amyloidosis (opening brief)**

Position: **ship, after two small definition fixes** (drop J99 and heart-transplant status; apply the source's case
exclusions to both classes) and a rename. Every problem the panel found is fixed in the definition (remedy ladder,
step 2) at a measured cost of at most 0.011 ROC AUC; none needs exclusion.

**1. Real, faithful data for a task the source names (P2, P3, P5 hold)**

- **Evidence.** The blind reviewer rebuilt the whole 15,394 x 1,733 table from the public Source Data. All 1,733 flag
  prevalences match with zero differences. 15,390 of 15,394 rows hash-match, with 100% label agreement. The label rule
  is Huda's own notebook line (`cohort_flag` from E8582/E854, claim 3).
- **Use case.** Huda's Discussion names the actor and the decision: "calculate the probability of wild-type ATTR-CM in
  HF patients and elevate the index of suspicion, after which further confirmatory testing can be done". The source
  validated this use externally: AUC 0.80 at Northwestern, prevalence 0.66%.
- **Fit.** `fit="approximate"` already states the gaps: whole-history flags, 1:1 matching, a prevalence far from use
  (USE-8).
- **Rules.** USE-1 (Must) holds. PROV-6 (Must) holds: the derivation file is not shipped, so its 597 shared patients
  cross no split.

**2. SEL-7 does not apply on its own terms; the timing problem is LEAK-10's, and LEAK-10 is fixed by drops**

- **Answers.** Precedent R1 (retire like stroke_prediction and cdc_diabetes).
- **Why SEL-7 does not reach this case.** SEL-7 (Must) covers "a label the respondent already knows, asked in the same
  interview". It requires "an independent measurement such as a lab test".
  - Here the label is a clinician's E85 code, set after biopsy or scintigraphy. That is an independent diagnostic
    measurement, not a self-report.
  - The features are other codes, not answers to the same questionnaire.
  - stroke_prediction and cdc_diabetes had no named decision and no external validation. This source has both.
- **What R1 really points at.** Its concern is that work-up and post-diagnosis codes sit in the features. That is a
  LEAK-10 matter.
- **The tension row that decides it.** "A real task against a leak (P3 and P4; USE-12, LEAK-10)" says "fix the leak
  and keep the task: a leak is no reason to reject a task whose use case is real".
- **The signal survives the drops.** It is broad: the ablations go 0.837, then 0.829, 0.818, and 0.806 with
  cardiomyopathy, every HF code, J99 and transplant all dropped. The baseline is 0.548. So no single family carries
  the task, and dropping more does not empty it (TP-2).

**3. Concede: J99 and heart-transplant status are LEAK-10 leaks; drop them (mildest remedy)**

- **J99.** `respiratory_disorders_in_diseases_classified_elsewhere` is a code-first manifestation code. It works by
  the same mechanism as the dropped I43.
  - Prevalence: 180 cases and 11 controls (likelihood ratio 16).
  - Its gain is +0.0081 on all 9 of 9 splits, more than 10 times the noise band (task gamer).
- **Transplant.** `heart_transplant_status` (Z94.1) is 2.0% of cases and 0.2% of controls. The transplant follows the
  diagnosis or is the event that makes it.
- **Measured cost.** Together, 0.837 → 0.829 (column auditor G, blind reviewer 0.826).
- **Remedy.** Add both to the leak list next to the source's two. Also state the rule behind the list: drop every
  "in diseases classified elsewhere" flag whose code-first note names amyloidosis.
- **The Z94 group flag** (`transplanted_organ_and_tissue_status`, 3.1% against 1.4%) is mixed. I would drop it too
  for a clean cut, but that is a weighing call.
- **Rule.** LEAK-10 (Must). Fixing the definition is step 2 of the remedy ladder.

**4. Apply the source's own case exclusions to both classes (repair from the origin, the top of the ladder)**

- **Controls carrying excluded codes.** 785 to 797 controls (10%) carry codes that no case can carry: N18.6, D47.2,
  E88.09, C90, I68.0, lymphoma codes and dialysis codes (claims 14 and 16, task gamer exploit 2).
- **Intracranial haemorrhage.** The paper's case definition excludes it, but 798 cases carry I60-I62.
  - Their profile is cerebral amyloid angiopathy: lobar ICH 238 against 17.
  - The model scores these cases at 0.915, against 0.828 for the other cases (column auditor problem 3).
- **Remedy.** Drop every patient with any excluded code from both classes. This is the paper's cohort definition made
  symmetric. It is not a definition of our own (tension row "a better version against our own fix").
- **Cost.**
  - Builder's variant C, symmetric exclusion of the ESRD and blood-disorder codes: 0.8366 against 0.8372.
  - Column auditor I2, symmetric ICH exclusion: 0.834.
  - The task gamer's ceiling exploit (+0.016) disappears with the remedy.
- **Rules.** LEAK-13 (Must): harmonise recording conventions that are specific to one class. The house
  minimal-preprocessing rule: fix what separates the classes for reasons other than the target.
- **Why this outranks keeping the rows "as the source selected them".** That reason keeps an artefact. The source's own
  stated rule removes it, and the fix costs no measurable score.
- **Cohort size.** About 13,500 patients remain, still roughly 6 times the derivation set.

**5. The cardiomyopathy family (issue 1, reopened): a weighing call, not a verdict driver**

- **The facts.**
  - The family cannot be dated: the release holds no per-code timestamps, as every panel member says.
  - It is mixed. HCM (I42.1/I42.2, 7.6% against 1.3%) is an antecedent; the paper says HCM misdiagnoses "preceded the
    ATTR-CM diagnosis". I42.5/I42.8/I42.9 and end-stage HF are work-up or disease-course codes.
  - Dropping the family costs 0.008 (B), or 0.019 with the HF subtypes (B2).
- **My position.**
  - The curator's A stands as the default.
  - The mildest cut that addresses the work-up concern is the narrower one: keep the HCM flags, drop
    `other_restrictive_cardiomyopathy`, `cardiomyopathy__unspecified` and `end_stage_heart_failure`.
  - Run that cut and put it beside A and B before the curator decides.
- **Concession.** distribution_transformers (drop values that changed after the outcome for an unknown subset) favours
  B over A. LEAK-11 does not save A, because the family raises the score.
- **The point that matters for the panel.** A, the narrow cut, and B all ship the dataset. The choice moves 0.008 and
  changes nothing at P2-P5. Under independent failures and the remedy ladder, it is the curator's weighing call, not a
  reason to exclude.

**6. Label: keep the source's Cohort 3 label, fix the name (USE-5 with a note; P5 over our own redefinition)**

- **What the label is.** "E85.4 or E85.82 in an HF patient" is exactly the paper's Cohort 3. The paper says it is
  meant to catch ATTR-CM coded under the general term.
- **The noise is real.** 47% of cases have no I43 or E85.82 link to the heart; E85.3 is in 10% of cases and E85.1 in 9%
  (domain practitioner, claim U1).
- **Why the label still ships.** USE-5 lets a documented source label ship as `fit="approximate"` with a note naming
  the gap. The curator chose option 2c knowing its "con: a broader label".
- **Why not tighten it.** Tightening to E85.82, or E85.4 together with I43, would be our own redefinition. The tension
  row says "a fix of our own invention does not" replace the source's version.
- **Concessions.**
  - The name is wrong. `unique_name` and the record name say "wild type ATTR", but only 516 of 7,697 cases hold
    E85.82. Rename it, for example to `cardiac_amyloidosis_claims_codes`.
  - `predicted` should state the shares of the E85 codes.
  - The row text should say the codes are ICD-10 only, from about October 2015 (no list holds an ICD-9 code).

**7. Split, metric and value all hold; the rest is cheap cleanup**

- **Split.** The split auditor finds it "right with notes".
  - Both branches of the tree reach a random leaf.
  - A grouped alternative scores the same (0.837).
  - Neither matched pairs nor near copies can be exploited.
  - The train-against-test classifier scores 0.50.
  - The forced leaf goes to the curator as a first-of-its-kind confirmation (SPLIT-36, Should), not as a defect.
- **Value (TP-2).** 15,394 rows, about 2,566 positives per test fold. LightGBM 0.837 and LR 0.813 against a baseline of
  0.548: a real signal that does not saturate.
- **Metric.** `roc_auc` stands. Per the claim auditor, it should be declared as the source's own metric: the model was
  selected "as evaluated by the AUROC" (MET-5). The score does not change.
- **2% selection (LEAK-31, Should).** It is measured: 0.837 with the rule on all cases, 0.838 per fold, 0.839
  label-free. "Remove it when we can": the label-free rule costs nothing and ends the argument. I support switching to
  it, but issue 2c fixed Huda's rule, so the switch goes to the curator.
- **Quality (P7).** Type the 1,733 presence flags categorical (CLEAN-14 and the zillow precedent).
- **Wording fixes.** The exclusion-list citation (Cohort 5), the duplicate count (one group of 4 rows), the `-1`
  placeholder, the medians, and the record's stale `Split:` and Outcome lines.

**Judgment record (advocate's view)**

```text
Verdict: ship after changes.
Validity: SEL-7 does not apply (a clinician's coded diagnosis, not self-report); USE-1 holds (approximate fit);
  USE-5 holds with a note (source's Cohort 3 label), rename; LEAK-10 triggered, fixed (drop J99, heart_transplant_status);
  LEAK-13 triggered, fixed (source's case exclusions incl. ICH applied to both classes); SPLIT-36 forced leaf, holds;
  PROV-6 holds (derivation file not shipped).
Value: TP-2 real signal (0.83 vs 0.55 baseline), survives every ablation (0.806 floor).
Quality: CLEAN-14 flags to categorical; LEAK-31 label-free 2% rule (curator); wording fixes.
Weighed: size + (15k), source + (Nat Commun, external validation), label noise -, matched sample -.
For the curator: issue 1 (A / narrow cut / B, 0.008 at stake); the label-free 2% rule; the rename.
```

**Rebuttal**

The critic and I agree on the verdict: ship after changes, with no exclusion. We agree on the fixes in points 2 to 7.
What is left is one question of rule labelling (point 1) and one choice of default (point 4).

**1. SEL-7: dispute that it is triggered; concede both writing asks**

- **Concede the fact.** I43 in 52.4% of cases shows that the history runs past the diagnosis for at least half the
  cases.
- **Concede the two asks.** The task card should say plainly that the features and the label come from one undated
  claims record. The distinguishing facts should be written into the record: a screening decision named by the source,
  external validation at 0.80, and antecedents shown in the paper's figure (Fig. 3 per the critic, Fig. 2 per the task
  gamer) that come before the diagnosis.
- **Dispute "SEL-7 triggered".** SEL-7's text is a label "the respondent already knows, asked in the same interview".
  It requires "an independent measurement such as a lab test", and a clinician's E85 code set after biopsy or
  scintigraphy is one.
  - The critic's own mechanism, post-diagnosis codes among the features, is LEAK-10's, and it is fixed by drops.
  - The critic's remedy (points 3 and 4 applied) is the same as mine.
  - This matters for the label the record carries. Recorded as an exception to SEL-7, it would be an exception to a
    Must, and principles.md says a Must has none. A SEL-7 exception would therefore need an amendment and would invite
    a `No` in a later pass. Recorded as "LEAK-10 triggered, fixed", the same facts stand on a rule that holds.
- **Dispute "the model learns who has been diagnosed".** After the drops, 0.818 to 0.829 remains. The column auditor
  traces it to the paper's antecedent families: carpal tunnel at 17.3% against 6.8%, spinal stenosis, conduction
  disease, and pericardial effusion.
- **What follows.** The curator is asked to confirm that SEL-7 does not apply and why. That is wording, not a decision
  about whether the dataset ships.

**2. Label: concede (a) and (b); agree (c) is measured, not imposed**

- (a) Concede the rename and the statement of what the cases hold.
- (b) Concede the symmetric ICH exclusion: it repairs from the source at a cost of 0.003. This was my point 4.
- (c) Agree that it is scored beside the shipped label and left to the curator. Tightening would be our own
  redefinition, and the tension row on a better version against our own fix puts the source's version first. The
  default stays the source's Cohort 3 label, with a USE-5 note.

**3. J99 and Z94.1: concede in full**

Same remedy and same rule as my point 3: drop both flags, write the "classified elsewhere" rule into the definition,
and leave the Z94 group flag to the curator.

**4. Cardiomyopathy family: concede LEAK-11; I move my default from A to the narrow cut**

- **Concede.** The family raises the score, so LEAK-11 cannot keep it. The distribution_transformers precedent wins
  over keeping A without an amendment.
- **Agree on the narrow cut as the default.** It drops the `cardiomyopathy` parent flag, I42.5, I42.8, I42.9,
  `end_stage_heart_failure` and the acute-on-chronic heart-failure flags. It keeps the HCM description flags. Score it
  beside A, B and B2.
- **One reservation for the issue table.** `cardiomegaly` (I51.7, 49% against 33%) and R93.1 can arise before the
  work-up (on a chest X-ray, or a first echo for the heart failure itself). I would list them as a separate curator
  option, not put them in the default cut. The critic does not put them in its remedy either.

**5. Control-only exclusions: concede in full**

This is my point 4. "Unchanged score" is the reason to apply the fix, not to keep the artefact.

**6. 2% selection: concede, and accept the new fact**

- **The new fact.** The claim auditor found that the validation notebook reused the trained model's feature list. So
  the label-aware selection on this file is our own cleaning step, and the precedents that removed such steps apply:
  home_credit, qsar_bioconcentration and numerai.
- **The rule.** LEAK-31 (remove it when we can), not LEAK-29. LEAK-29 covers feature values computed over all rows;
  this is a selection of columns.
- **The remedy.** The label-free rule, which costs nothing (0.839). It goes back to the curator because issue 2 c named
  Huda's rule.

**7. Quality and wording: concede in full**

That covers the declaration of the metric's origin (MET-5), the categorical typing (CLEAN-14), and the seven claim
corrections. It also covers the group basis's 0.93 to 0.80, which was measured with the wild-type model, and the
out-of-date Outcome and `Split:` lines.

**Judgment record after the rebuttal**

```text
Verdict: ship after changes (advocate and critic agree; no exclusion).
Validity: SEL-7 not applicable (a clinician's coded diagnosis); its facts written in the record and the task card;
  LEAK-10 fixed: J99, Z94.1, narrow cardiomyopathy and HF cut (default), score beside A/B/B2;
  LEAK-13 pattern fixed: the source's exclusions (incl. ICH) on both arms; USE-5 note + rename; SPLIT-36 holds.
Value: TP-2 real signal (about 0.82 after the fixes vs a 0.548 baseline).
Quality: LEAK-31 label-free 2% rule (curator), CLEAN-14, MET-5 origin, claim fixes.
For the curator: SEL-7 framing (wording); the narrow cut vs A/B; cardiomegaly/R93.1; tightening the label (scored); 2% rule.
```

</details>

<details><summary>Critic (brief and rebuttal)</summary>

**Critic, opening brief: wild_type_attr_cardiac_amyloidosis**

**Position: do not ship as defined; ship after changes 2 to 6, and only if the curator accepts point 1 with the fact that sets it apart written down.** The data is real and reproduces bit for bit (blind reviewer), the split is right for what the file allows (split auditor), and the signal is broad (0.806 even after the harshest ablation). But the shipped table still holds two Must-level leaks of the very kind the source removed, a label that is not what the name and task card say, and a selection artefact the model can learn. None of this needs exclusion; it needs the definition fixed.

Settled by the curator and not reargued here: issue 2 c (the validation file) and issue 1 A as a starting point, which the curator asked to reopen with data (point 4).

**1. The label is a diagnosis already in the same undated record (P2, SEL-7 Must; P3, USE-3 Must)**

- **Decisive fact:** 52.4% of cases carry I43, a manifestation code that can only be written once the amyloidosis is on record (column auditor, task gamer). So for at least half the cases the "history" runs past the diagnosis, and the flags have no dates to cut it (Methods: "not the temporal sequence of ICD codes").
- **Effect:** a model learns who has been diagnosed, while the use case scores patients nobody has diagnosed yet. That is the SEL-7 pattern that retired stroke_prediction ("a stroke the patient already had, undated"; "a screening task would need a first stroke within a horizon, from dated records") and, by Andrej on 2026-11-10, south_africa_coronary_heart_disease (precedent checker R1). The definition does not say why this case is different.
- **What may set it apart, and must be written if the task stays:** the source names a screening decision; it validated externally (ROC AUC 0.80 at Northwestern); its Fig. 3 shows non-cardiac antecedents years before diagnosis; and the signal survives removing the diagnosis-era families (0.818 for B2, 0.806 for the blind reviewer's harshest cut).
- **Remedy (mildest):** keep, but only with the diagnosis-era codes removed (points 3 and 4), the task card saying plainly that features and label come from one undated claims record, and the distinguishing fact recorded beside SEL-7 for the curator. If the curator does not accept that fact, SEL-7 is a Must, and the outcome is `No Good Target / Scientific Discovery` as for stroke_prediction. I do not ask for that: the fix is available.

**2. The target is not "cardiac amyloidosis", let alone wild-type ATTR (P3, USE-5 Must)**

- **Decisive fact:** every case holds E85.4 ("organ-limited amyloidosis"); only 516 of 7,697 hold E85.82 (claim auditor 5, blind reviewer 2). 3,593 cases (47%) have no code linking the amyloid to the heart (neither I43 nor E85.82). 783 carry E85.3 secondary systemic (AA) and 716 E85.1 hereditary neuropathic (domain practitioner 1, claim auditor U1).
- **Cerebral amyloid angiopathy inside the positives:** 798 cases (10.4%, against 4.7% of controls) have intracranial haemorrhage I60-I62, with a CAA profile (lobar ICH 238 vs 17, LR 14); 484 of them carry no cardiomyopathy code at all. The shipped model scores this subgroup at 0.915 against 0.828 for the other cases, so it inflates the score (column auditor 3). The paper's case definition excludes ICH and CAA; the file did not apply it, which may account for the 7,697 vs 7,296 gap.
- **Effect:** the name, `question` and `predicted` promise cardiac amyloidosis; a share of the positives is brain or other-organ amyloid. The actor acts on cardiac amyloid (scintigraphy referral).
- **Remedy:**
  - (a, required) Rename `unique_name` and the record `name` away from "wild type ATTR" (e.g. `cardiac_amyloidosis_claims_iqvia`); state the case composition (E85.82, E85.3, E85.1, no heart link) in the label note.
  - (b, required, mildest repair from the source) Apply the paper's ICH exclusion to both classes (drop the patients with I60-I62): measured 0.834, cost 0.003.
  - (c, curator option, measure first) Tighten the label to E85.82, or E85.4 together with I43: 4,104 cases, the 3,593 without a heart link dropped, not relabelled. This is our own redefinition, so I ask for it scored beside the shipped one, not imposed.

**3. Two companion and consequence codes stay as features (P4, LEAK-10 Must)**

- **Decisive fact:** `respiratory_disorders_in_diseases_classified_elsewhere` (J99) is a manifestation code with the same code-first mechanism as the dropped I43: 180 cases vs 11 controls, the highest-lift column in the table. Removing it costs 0.0081 on all 9 shipped splits, more than ten times the noise band (task gamer exploit 1). `heart_transplant_status` (Z94.1, 2.0% vs 0.2%) is a consequence of the diagnosis, or the event that makes it (column auditor 2).
- **Effect:** a deployed model on an undiagnosed patient never sees either; both are "a part, a consequence or another encoding of the target", which LEAK-10 puts out with no exception. The definition drops I43 on exactly this reasoning and keeps J99, which is inconsistent.
- **Remedy:** drop both flags, and write the rule in the definition: every "in diseases classified elsewhere" flag whose code-first note names amyloidosis goes (today only J99 passes the 2% rule; L99, K77, N33 would enter if the rule changes). `transplanted_organ_and_tissue_status` (Z94 group, mixed) to the curator. Combined cost measured: 0.837 to 0.829.

**4. Issue 1, reopened as asked: the work-up codes raise the score, so LEAK-11 cannot keep them (P4, LEAK-10 Must, LEAK-11 Should)**

- **Decisive fact:** LEAK-11 keeps a value measured after the outcome only when it weakens the signal. The cardiomyopathy family raises it: 0.837 with, 0.829 without (B), 0.818 with the HF subtypes also out (B2). `cardiomyopathy` is the top single flag (AUC 0.627).
- **Precedent:** distribution_transformers_at_cauca_department (Lennart, 2026-10-21): attributes that changed after the outcome for an unknown subset of positives are dropped, "no amendment for a gain that may sit on the changed rows". SAheart kept its late values only because they weakened the signal (precedent checker R2). The definition's "Potential leak, kept on purpose" for this family has no LEAK-11 basis.
- **But the family is not uniform** (column auditor 4): HCM (I42.1/I42.2) is an antecedent the paper names as an initial misdiagnosis; restrictive/other/unspecified (I42.5/I42.8/I42.9), `end_stage_heart_failure` and acute-on-chronic HF follow the work-up or the disease course; `cardiomegaly` (I51.7) and R93.1 abnormal cardiac imaging are work-up findings (domain practitioner 2).
- **Remedy (mildest that meets LEAK-10):** a narrow cut, not B: drop the `cardiomyopathy` parent flag, I42.5/I42.8/I42.9, `end_stage_heart_failure` and the acute-on-chronic HF flags; keep the HCM description flags. Not run yet: score it beside A, B and B2 for the issue table. If the curator prefers A, it needs a written amendment of LEAK-10 for coded histories, since a Must has no exceptions.

**5. 10% of controls are controls by construction (P4, recording by class: LEAK-13/LEAK-14 pattern, verification P4)**

- **Decisive fact:** 785 to 797 controls (10.2-10.4%) carry a code no case can carry because the exclusion was applied to cases only: ESRD N18.6 (498), E88.09 (161), MGUS D47.2 (136), myeloma C90 (73), lymphoma and dialysis codes (claim auditor 14, 16; task gamer exploit 2). None is its own column, but the kit predicts the flag at AUC 0.941, the strongest negative columns are those families, and decoding it would add up to +0.016.
- **Effect:** the model learns the recruitment rule, and clinically backwards: an HF patient with MGUS or myeloma is a prime suspect for AL cardiac amyloid, and the model learns "control".
- **The definition's argument does not hold:** "dropping those controls leaves the score unchanged" is the reason to drop them, not to keep them. The fix costs nothing (0.8366 vs 0.8372, builder's variant C) and removes a separation that has nothing to do with the target. That is the minimal-preprocessing rule: fix what separates classes for non-target reasons.
- **Remedy:** drop the controls that meet the source's case-exclusion list, the same list on both arms. Together with point 2b, the source's exclusions become symmetric.

**6. The 2% selection uses every label, and it is not even the source's step here (P4, LEAK-31 Should; LEAK-29 Must for our own cleaning)**

- **Decisive fact:** Huda applied the 2% rule to the wild-type derivation cases; the validation notebook did not reselect but reused the trained model's feature list (claim auditor 10). So the label-aware selection on all 7,697 cases, test folds included, is our own cleaning step, not "the data as published". The precedents of our own pipelines removed such steps (home_credit, qsar_bioconcentration, numerai).
- **Effect:** small (0.837 shipped, 0.838 per fold, 0.839 label-free), but LEAK-31 says "remove it when we can", and we can at zero cost.
- **Remedy:** a label-free rule (a flag in at least 2% of all patients; 0.839). The curator wrote "Huda's 2% rule" in issue 2 c, so this goes back to the curator with the new fact, not changed unasked.

**7. Quality and wording (P6 MET-5 Should; P7 CLEAN-14 Should; claims)**

- **Metric origin:** the paper selects its model "as evaluated by the AUROC" (Methods) and ranks the NMEDW models by AUROC only, so `roc_auc` is the source's metric under MET-5, not the fallback. Same score; fix the declaration and the record's Metric line.
- **Typing:** the flags are presence flags of named diagnoses; CLEAN-14 makes such 0/1 columns categorical (zillow precedent). Type them categorical, or write the reason for numeric.
- **Claims to correct** (claim auditor, column auditor, domain practitioner): the case-exclusion quote is the NMEDW (Cohort 5) definition, not Cohorts 3 and 4; the duplicates are one group of 4 identical rows with both labels, not "2 patients"; "22,220 of 22,222 codes" counts the `-1` placeholder (1,293 patients); the median 114/102 includes the E85 codes (112/102 without); the history is ICD-10 only (no ICD-9 code in any list), so roughly October 2015 to April 2019, not "2008 to April 2019"; the group basis's 0.93 to 0.80 is the wild-type model, not this label; the T63 bulk likely comes from the ICD-9 to ICD-10 conversion.
- **Stale record lines:** the `## Review` Outcome and the Screening `Split:` line still describe the 2,142-patient derivation file.

**Judgment record**

```text
Verdict: ship after changes (no exclusion asked).
Validity: SEL-7 triggered (look-back label), kept only with the distinguishing fact written and points 3-4 applied, curator to confirm;
          USE-5 triggered, fixed by rename + symmetric ICH exclusion, tighter label offered measured;
          LEAK-10 triggered twice: J99 and Z94.1 dropped (fix); cardiomyopathy work-up codes, LEAK-11 not available, narrow cut;
          class-dependent selection of controls, fixed at no cost; LEAK-31 label-free rule at no cost; SPLIT-36 holds (forced leaf, noted).
Value: signal survives every cut (0.806-0.837), well above the 0.548 code-count baseline.
Quality: MET-5 origin, CLEAN-14 typing, seven claim corrections.
For the curator: SEL-7 distinguishing fact (point 1); label tightening (2c); narrow vs B cut (4); 2% rule (6).
```

**Rebuttal**

The advocate and I agree on the verdict (ship after changes, no exclusion) and on most of the remedies. Two disputes are left: whether issue 1 is a weighing call (advocate 5), and what the narrow cut must drop. On SEL-7 we agree on the remedy, but its wording does not let the record skip writing the distinguishing fact (advocate 2).

**Advocate 1 (real, faithful data, a named use): concede**, with one wording gap.
- Provenance, use case and PROV-6 hold.
- `fit_reason` does not yet name the label noise (47% of cases without a heart link; AA and hereditary codes). USE-5 lets a noisy source label ship only "with a note naming the gap", so it has to be added there.

**Advocate 2 (SEL-7 does not apply): concede the remedy, dispute the reading.**
- Conceded: the label is a clinician's code set after a diagnostic test, not a self-report. That is the independent measurement SEL-7 asks for, so retirement is not required.
- Disputed: SEL-7 is not limited to interviews. stroke_prediction was retired under SEL-7 although it was "in a hackathon release rather than an interview" (selection.md Cases). What decided that case was an undated past diagnosis and no screening decision. Here the diagnosis is also undated, and I43 in 52% of cases shows the history runs past it.
- The tension row "fix the leak and keep the task" holds only once the use case is real for these rows. That is the question R1 raises.
- So the record must state why this case differs from stroke_prediction: a diagnostic test behind the label, a named decision, external validation, and the signal surviving once the diagnosis-era codes are removed. Otherwise the next curator meets two opposite SEL-7 outcomes on similar facts (principles: "treat like cases alike").
- No change to the verdict: this is one sentence in the record.

**Advocate 3 (drop J99 and heart-transplant status): agreed.**
- The rule on "in diseases classified elsewhere" flags is written into the definition.
- Z94 (`transplanted_organ_and_tissue_status`) goes to the curator.

**Advocate 4 (exclusions on both classes, including ICH): agreed, with one correction of the source claim.**
- The full exclusion list, ICH and CAA included, is stated in the paper only for the Northwestern cohort (claim auditor 13). For Cohort 3 the Methods say "blood cancers and other non-ATTR-CM-related amyloidosis terms".
- The ICH exclusion still follows from that clause: CAA is a non-ATTR amyloidosis, and the subgroup scores 0.915. The note should cite the clause, not claim that the source's Cohort 3 rule names ICH.
- Remedy and costs unchanged (0.834 and 0.8366). I file the ICH part under USE-5 and the advocate under LEAK-13; it is one remedy either way.

**Advocate 5 (cardiomyopathy family as a weighing call): dispute.**
- *A is not a default the curator can weigh.* The advocate concedes that LEAK-11 cannot keep the family (it raises the score) and that distribution_transformers favours dropping it. What is left is LEAK-10, a Must, and "a Must has no exceptions: only a higher-ranked Must overrides it, and anything else is an amendment" (principles).
  - So the curator's choice is between a cut, B or the narrow one, and A with a written amendment of LEAK-10 for coded histories.
  - It is not a weighing of A against B. I agree it does not drive exclusion.
- *The advocate's narrow cut keeps the leak through the parent flag.*
  - It drops `other_restrictive_cardiomyopathy` and `cardiomyopathy__unspecified` but keeps `cardiomyopathy`. That parent flag is the I42 category, which those very codes switch on.
  - It is the top single flag in the table (AUC 0.627; 51.9% of cases against 26.5% of controls).
  - With the parent kept, dropping its children removes almost nothing. The task gamer showed that a parent set without a child in the table decodes the codes left out (exploit 3).
  - The narrow cut must drop the parent and keep only the HCM description flags (`other_hypertrophic_cardiomyopathy`, `obstructive_hypertrophic_cardiomyopathy`).
  - The variant to run before the curator decides: drop the parent, I42.5/I42.8/I42.9, `end_stage_heart_failure` and the acute-on-chronic HF flags, with `cardiomegaly` and R93.1 measured as an add-on.

**Advocate 6 (keep the Cohort 3 label, fix the name): concede, with a condition.**
- Conceded: tightening the label is our redefinition and stays a curator option, measured, not imposed. Cohort 3 is the source's own version.
- Agreed: rename and state the E85 shares.
- Condition: the label ships as `fit="approximate"` only together with the ICH exclusion (advocate 4) and a `fit_reason` that names the gap (see advocate 1).
- Without those two, part of the positives is brain amyloid. That would be "another quantity than the one the actor acts on", which USE-5 fails (diabetes_3).

**Advocate 7 (split, metric, value, cleanup): agreed on every item.**
- The split is right, `roc_auc` is declared as the source's metric (MET-5), the label-free 2% rule goes to the curator, the flags are typed categorical, and the wording is fixed.

**What is left for the mediator:**
- (i) issue 1: is A an amendment of a Must or a weighing call? On rank, it is an amendment.
- (ii) the narrow cut must drop the `cardiomyopathy` parent flag.
- (iii) the SEL-7 distinguishing fact goes into the record.

</details>
