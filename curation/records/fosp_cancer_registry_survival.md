---
unique_name: fosp_cancer_registry_survival
name: Hospital-Based Cancer Registry of Sao Paulo (RHC/SP), 3-year survival after diagnosis
checked_by:
- AI (UNVERIFIED)
suggestion: TBD -> Yes
priority: 2
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
- Dated Event Log
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Fixed Delay'
- 'Target: Revised Later'
- 'Features: Revised Later'
original_source: GOV Website
collection_period: Jan 2000 - Jun 2026
domain: medical & healthcare
required_split:
- Temporal (NON-IID)
problem_type: Binary Classification
source_links:
- https://fosp.saude.sp.gov.br/fosp/diretoria-adjunta-de-informacao-e-epidemiologia/rhc-registro-hospitalar-de-cancer/banco-de-dados-do-rhc/
- https://doi.org/10.1038/s41598-025-34133-w
- https://github.com/CDIA-NSEE/cancer_cross_prediction
- https://fosp.saude.sp.gov.br/wp-content/uploads/DICIONARIO_DADOS__RHC-SP_FOSP_28042026.pdf
- https://doi.org/10.1186/s12911-026-03654-3
- https://doi.org/10.3390/cancers16183205
- https://doi.org/10.1038/s41598-023-35649-9
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 2: deep re-check after Shaktah et al. 2026 used the same registry (colorectal only) in a clinical tabular benchmark; the public data dictionary and the openly linked 2000 file confirm the follow-up fields (`ULTINFO` 1 alive with cancer, 2 alive, 3 death from cancer, 4 death from other causes; `DTULTINFO`; a loss-to-follow-up flag `PERDASEG`) and recurrence fields (`DTRECIDIVA`, `RECNENHUM`, `RECLOCAL`, `RECREGIO`, `RECDIST`, `REC01`-`REC04`); recommend all sites, 3-year overall survival from diagnosis, alive patients followed less than 3 years dropped, temporal by diagnosis date with a 3-year gap.
- Source: RHC/SP of the Fundação Oncocentro de São Paulo (FOSP). Its page now says "Faça um cadastro prévio para acessar os arquivos segundo ano de diagnóstico do tumor, com dados referentes ao período de Janeiro de 2000 a Junho de 2026" and "A atualização deste banco de dados é trimestral"; the files hold the "casos analíticos" (patients who arrived untreated). The data dictionary is public: "Dicionário de Dados – RHC/SP – FOSP (Geral)", revision 16/04/2026 (https://fosp.saude.sp.gov.br/wp-content/uploads/DICIONARIO_DADOS__RHC-SP_FOSP_28042026.pdf; older versions 2024-08, 2024-11 and 2026-02 in the same folder). Field 99 "ULTINFO Última informação sobre o paciente": "1 – VIVO, COM CÂNCER 2 – VIVO, SOE 3 – OBITO POR CANCER 4 – OBITO POR OUTRAS CAUSAS, SOE"; field 98 "DTULTINFO Data da última informação do paciente"; field 113 "PERDASEG Perda de seguimento" (0, 1, 8 not applicable); field 69 `NAOTRAT` (reason for no treatment) includes "5 – OBITO POR CANCER 6 – OBITO POR OUTRAS CAUSAS, SOE"; it adds race, marital status, occupation, alcohol, tobacco, family history and breast and HPV biomarkers as "Novas variáveis recém-adicionadas ... em início de registro pelos hospitais". Preview: the diagnosis-year 2000 file is linked openly (https://fosp.saude.sp.gov.br/wp-content/uploads/RHC_SP_2000.zip, a 58.6 MB DBF, uploaded 2025-01-31; HEAD requests for 2001, 2010, 2019 and 2023 return 404, so the other years need the registration): 28,284 rows x 105 columns, 68 hospitals (`INSTITU`), `ULTINFO` 1: 1,159, 2: 7,122, 3: 12,048, 4: 7,955, `PERDASEG` = 1 on 5,222 rows (all alive), `DTULTINFO` up to 2024-10-11, recurrence dates a median 2.0 years after diagnosis (10% 0.5, 90% 8.4 years). Third-party copy: the cross-prediction repository's notebooks load `pacigeral_12_23.csv` (1,178,688 x 100) from a Google Drive link, not FOSP's release.
- Use case: as on 2026-10-31 (an oncology team's prognosis for a newly diagnosed patient; fit approximate, no decision named). Cardoso et al. 2023 name the planning use: "the prediction of survival can be very useful to estimate the potential loss of survival" "in conditions of disruption of health services" (Discussion). Collection: `Samples: Over Time` (patients diagnosed one by one since 2000), `Time: Dated` (`DTDIAG`, `DTCONSULT`, `DTTRAT` and `ANODIAG` in the raw rows), `Target: Fixed Delay` for a horizon label, `Target: Revised Later` (the vital status and its date are updated with each quarterly release, so the newest diagnoses' labels are not final), `Features: Revised Later` (follow-up fields such as recurrence and treatment after admission are filled into the row after its diagnosis date); type `Dated Event Log` (a registry whose rows record the diagnosis date, SPLIT-34 rule 3; was effectively a clinical study in the 2026-10-31 block, which named no type).
- Split: leaf [L-ORDER.windows] (Temporal · windows on the time key) because [CLI.dated] yes (`DTDIAG` per row, so the type is a dated event log), [LOG.meets] cases after the data (new patients), [ORDER.order] yes (the diagnosis date), [ORDER.windows] yes (diagnoses from 2000; with a 3-year horizon labels mature up to about mid-2023 in the current release), [ORDER.small] no (a large table). Open: the test window length (one diagnosis year proposed, for sign-off, SPLIT-12); the gap equals the horizon (a training row's label is final only 3 years after its diagnosis, SPLIT-9, SPLIT-10); 2020 (COVID) inside a test window; whether the hospital is also held out (SPLIT-13; no hospital use case named); whether a patient with two primary tumours has two rows (no patient id in the release; `Entities` left unset). All three papers on the data split randomly (75/25, 75/25, 70/30), a claim, not a choice for the use case (SPLIT-5).
- Siblings and duplicates: unchanged; no other record of the RHC/SP. The SEER survival records from the same benchmark paper (`seer_renal_cell_carcinoma_5y_survival`, `seer_osteosarcoma_survival`) are another registry. Do not add a colorectal record: Shaktah's five FOSP tasks are cuts of this source (options below, PROV-7).
- Better data: none from another source (data scout, 2026-11-25). The source's own release is newer than the papers' cuts: the RHC/SP page now covers diagnoses from January 2000 to about mid-2026, updated quarterly, a version of this record (PROV-6), not a new candidate. INCA's national IntegradorRHC (https://www.gov.br/inca/pt-br/assuntos/cancer/numeros/registros/rhc) is larger (all states) but showed no follow-up or vital-status fields, so it does not carry a survival target (data dictionary not seen); the CDC USCS public-use database offers rates, not survival. Looked in: FOSP, INCA, CDC USCS, NCDB, Zenodo, Kaggle.
- Papers and pages: Shaktah et al. 2026, BMC Med Inform Decis Mak 26:364, https://doi.org/10.1186/s12911-026-03654-3 (full text and supplement read): Methods, "Data preprocessing": "FOSP data were filtered to colorectal cancer patients using TOPO codes C18–C20. Outcome variables were defined as follows: overall_death = 1 if ULTINFO = 3 or 4, and cancer_death = 1 if ULTINFO = 3. Survival targets (1-year, 3-year, and 5-year) were computed from DTDIAG and DTULTINFO."; "FOSP Overall Death and Cancer Death were analyzed as reproduced binary endpoint tasks mirroring previous publications, without modeling follow-up time or censoring" (Methods), "and should therefore not be interpreted as survival-modeling benchmarks" (Discussion); data accessed Feb 2025; random 70/30 split, tables above 100,000 rows sampled down; Supplemental List 1 names the leakage columns removed for the three SEER tasks and none for FOSP, and the text says only that "derived outcome-related features, such as “days_survived”" were excluded and that date strings became day counts, so whether `DTULTINFO`, `PERDASEG` or the recurrence fields were inputs is not documented. AUROC (best ML / logistic regression / TabPFN): 1-year 0.873 / 0.674 / 0.867, 3-year 0.867 / 0.624 / 0.864, 5-year 0.880 / 0.607 / 0.877, cancer death 0.873 / 0.614 / 0.870, overall death 0.875 / 0.646 / 0.873. Woźniacki, Książek, Mrowczyk 2024, "A novel approach for predicting the survival of colorectal cancer patients using machine learning techniques and advanced parameter optimization methods", Cancers 16:3205, https://doi.org/10.3390/cancers16183205 (PMC11430446, read): "72,961 colorectal cancer patients" from 2000-2023 (2.1, "Dataset"), but Table 3 gives 32,291 rows per task without saying why; 58 feature columns listed in Table 2 include `DTULTINFO`, `ULTINFO`, `DTRECIDIVA`, `RECNENHUM` and the other recurrence fields; the horizon labels count the censored as deaths: "a value of 0 indicates that the patient has died or is no longer under follow-up after the specified period" (2.1); random 75/25 split; SHAP for overall death: "Clinical staging (EC), year of diagnosis (ANODIAG), and absence of recurrence (RECENHUM) emerge as key factors" (3, Results), and recurrence is second for 1-year survival. It follows Buk Cardoso, Cunha Parro, Verzinhasse Peres, Curado, Fernandes, Wünsch Filho, Toporcov, "Machine learning for predicting survival of colorectal cancer patients", Sci Rep 13:8874 (2023), https://doi.org/10.1038/s41598-023-35649-9 (read), which defined the five targets on 31,916 colorectal adenocarcinomas (C18-C20, morphology 8140/3) treated 2000-2021 and drops the censored for the horizons: "patients with the time between diagnosis and last information greater or equal than the survival time of the analysis, or who died in the period, were eligible" (Methods, "Selection of variables"; the lost were "7%, 17.8%, and 26.9% for 1, 3, and 5-year survival", Discussion), random 75/25, presence of recurrence among the top five features for cancer death, overall death and 1-year survival. Code for Cardoso et al. 2026: https://github.com/CDIA-NSEE/cancer_cross_prediction (read): `get_labels` sets death as `ULTINFO > 2` and survival as days from `DTDIAG` to `DTULTINFO` above 365 x horizon, the notebooks drop the alive rows short of the horizon before modelling, and `presenca_rec` (from `RECNENHUM` and `DTRECIDIVA`) is kept as a feature. Cited, not read: Silva et al., "Machine learning for longitudinal mortality risk prediction in patients with malignant neoplasm in São Paulo, Brazil", Artif Intell Life Sci 3:100061 (2023).
- Metric: Shaktah et al. rank by AUROC ("assessing discrimination performance", Introduction; AUPRC, balanced accuracy and F1 at the Youden threshold in Supplementary Table 2); Woźniacki et al. report accuracy, F1 and AUC; Cardoso et al. 2023 accuracy and AUC; Cardoso et al. 2026 balanced accuracy and F1. No source fixes a threshold, so `roc_auc` (MET-5, MET-6, MET-8), which is also the newest paper's ranking metric. Inputs none.
- Target and cohort, options (a decision for the curator; censoring is weighed case by case, no blanket rule): (A) all sites, 3-year overall survival from diagnosis, dropping alive patients followed less than 3 years (Cardoso et al. 2026's task; the largest table, the topography as a feature, mixed cancers in every window); (B) colorectal only (C18-C20), the same label at 1, 3 or 5 years (Cardoso et al. 2023; the cohort of Woźniacki et al. and Shaktah et al.; about 72,500 rows, one cancer, a published TabPFN baseline under a random split); (C) the published death endpoints without a horizon (`ULTINFO` in 3, 4, or 3 alone): a status cut by the release date, so a patient diagnosed in 2022 has had less time to die than one from 2005; LEAK-24 (Must) asks to cut where follow-up is complete, and the year of diagnosis ranking among the top features in both colorectal papers fits that; (D) Woźniacki's horizon labels with the censored counted as deaths: in the 2000 file 12% (colorectal) to 21% (all sites) of the 3-year zeros are alive patients lost before 3 years (LEAK-25 mixes "no event" with "not recorded"). How to treat the alive patients short of the horizon, for (A) or (B): drop them (the papers' rule; the loss is uninformative only if loss of follow-up is unrelated to prognosis; in the 2000 file 10% of all rows, 6% of colorectal rows); count them as deaths ((D), mislabels); or keep the horizon open and train on the closed cases only (the same as dropping for a fixed horizon). Cancer death at a horizon keeps deaths from other causes as No (LEAK-22). The horizon: 1 year keeps the most diagnosis years (labels to about mid-2025) but is 70/30; 3 years is near balanced (in the 2000 file 54% survive among those not censored, all sites) and Cardoso et al. 2026's; 5 years loses the 2021-2023 diagnoses to the gap. Recommendation: (A), 3 years, drop the alive rows short of the horizon; (B) only if the curator prefers the single-cancer task the newest paper scored, as one definition (not both: a cut without a distinct task, PROV-7).
- Risks for /add-dataset: drop the follow-up and outcome fields `DTULTINFO`, `ULTINFO`, `PERDASEG`, `DTRECIDIVA`, `RECNENHUM`, `RECLOCAL`, `RECREGIO`, `RECDIST`, `REC01`-`REC04` (LEAK-10; both colorectal papers used recurrence as an input); `NAOTRAT` codes 5 and 6 encode a death as the reason for no treatment (merge them into "other" or drop the column, LEAK-10); the treatment fields after admission outside the hospital (`TRATFAPOS`, `*APOS`), `DTTRAT`, `TRATCONS`, `DIAGTRAT` and the in-hospital treatment flags put the prediction point after first-course treatment, and `PT`, `PN`, `PM` after surgery (USE-3, USE-4: decide the stage); the TNM edition changes in 2006 and 2014 and the CID-O edition in 2006, so stage and topography codes change meaning across windows; the newly added variables (race, smoking, biomarkers) are missing in the older years; the release is updated quarterly, so pin the download date (LEAK-24, compare two downloads, probe 13); row cap and site choice per the options (PROV-7); registration needed for all years but 2000, licence terms not stated on the page (not checked further).
- Priority: gap 0 (medical, binary and temporal are not thin), use case 0 (prognosis named in general, fit approximate), source + (a state registry with a public data dictionary and three peer-reviewed papers), shape + (over a million rows, mixed types, 24+ diagnosis years, 68+ hospitals), risk - (recurrence and follow-up columns that the published work used as inputs, and a target to build against censoring).

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 2: the São Paulo state hospital cancer registry (FOSP's RHC/SP: 1,178,688 patients diagnosed 2000-2023 in 79 hospitals) with demographics, stage, first-course treatment and follow-up, used for 3-year survival after diagnosis by Cardoso et al. 2026; a large real prognostic task with a temporal split by year of diagnosis, but a recurrence column, the treatment timing and the target's construction are to settle.
- Source: Registro Hospitalar de Câncer do Estado de São Paulo (RHC/SP), Fundação Oncocentro de São Paulo (FOSP), São Paulo state health department. Its page "Banco de dados do RHC" (link 1): cases diagnosed from January 2000, updated quarterly ("A atualização deste banco de dados é trimestral"), anonymised, files by year of diagnosis, download after registration ("Faça um cadastro prévio para acessar os arquivos"); the file list did not load, so the data dictionary was not seen. As described by Cardoso et al. (Methods, "Study population"): "The registry spans cases recorded from January 2000 to December 2023, totaling 1,178,688 patients", from 79 public and private hospitals. Their cut: diagnoses 2000-2019, adults, residents of the state, clinical stage known, microscopic confirmation; 23 predictors (Table 4: age, sex, municipality, care category, prior diagnosis and treatment, clinical stage, seven first-course treatment flags, days from consultation to diagnosis and from diagnosis to treatment, year of diagnosis, health regions, the treating hospital's municipality and qualification, education, `presenca_rec`). Their target: 1 if the patient survived at least three years after diagnosis, from the last follow-up date and vital status; patients with less than three years of follow-up excluded ("Selection of variables").
- Use case: an oncology team estimating a patient's prognosis after diagnosis and first-course treatment. The paper says cross-prediction can "support clinical decision-making when expert models are unavailable" (Discussion), that it is "not yet ready for clinical application", and that overall survival "was justified by the purpose of estimating the general prognosis of patients"; fit approximate (no decision named, and the treatment flags are the hospital's own choice, so a model that informs treatment cannot take them as given). Regime temporal by year of diagnosis (a model fit on past cases is used on new ones); the paper used a random 75/25 split (SPLIT-5, a claim).
- Siblings and duplicates: no other record of the RHC/SP; `seer_breast_cancer_survival` and `seer_breast_cancer_5y_survival` (unscreened, US SEER) are the nearest tasks, another registry and population. External collections: none in our vocabulary.
- Better data: from the curator's Zotero collection (item 146, Cardoso et al.); no search for better data in this run.
- Papers and pages: Cardoso, Egydio, Toporcov, Utida, Curado, Fernandes, Ribeiro, Chin, Parro, "Cross-cancer survival prediction using machine learning models", Sci Rep 16:9623 (2026), https://doi.org/10.1038/s41598-025-34133-w (read from the UFG repository's PDF), code at https://github.com/CDIA-NSEE/cancer_cross_prediction; the same group's colorectal survival comparison on about 45,000 patients (arXiv 2510.24473, abstract read: C-index, IPCW C-index, time-dependent AUC and integrated Brier score).
- Metric: Cardoso et al. report balanced accuracy and F1 per cancer type ("We selected balanced accuracy and f1-score to capture overall model performance with reduced sensitivity to class imbalance", Results, "Phase 2") and sensitivity, specificity, accuracy and AUC in Supplementary Table 1: two threshold metrics side by side and no threshold fixed, so the fallback `roc_auc` (MET-5, MET-6, MET-8). Inputs none.
- Risks for /add-dataset: `presenca_rec` (presence of recurrence) is known only during follow-up and goes (LEAK); the follow-up and death dates build the target and go; the treatment flags and the diagnosis-to-treatment interval put the prediction point after the first treatment (USE-3, to decide); rows alive with less than three years of follow-up go, and the newest diagnosis years cannot reach the horizon (SPLIT-9); one dataset per cancer site or all sites with the topography as a feature, and a row cap, are to decide (PROV-7); the treating hospital is a grouping candidate inside the temporal task (SPLIT-13); the download needs a registration (no criterion, EV-4).
- Priority: gap 0 (medical, binary and temporal are not thin), use case 0 (decision support named only in general, fit approximate), source + (the state registry's documented page and a peer-reviewed paper), shape + (over a million patients, mixed types, 24 diagnosis years), risk - (a post-outcome recurrence column and a target to build from follow-up dates).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through the curator's Zotero collection, item 146: "Cross-cancer survival prediction using machine learning models".
- as published: cancer patients, 1,178,688 rows 2000-2023 per the paper, 79 hospitals; ~23 predictors used (age, sex, residence, stage, first-course treatments, diagnosis-to-treatment days, hospital, education); target: survival 3 years after diagnosis (binary; or other horizons), from vital status and last follow-up date; access: registration.
- Why: very large public hospital registry with a real prognostic target, temporal split by diagnosis year, many cancer sites
- Adds: a large Latin-American oncology registry; no cancer registry in the records. Risks: drop presenca_rec (recurrence, after outcome); exclude patients followed less than the horizon (LEAK-23/24); one table per diagnosis year

## Review

**Outcome:** not added; screened `TBD -> Yes`, priority 2. São Paulo hospital cancer registry (RHC/SP, about 1.18 million patients since 2000); the published tasks fed recurrence and follow-up columns in as inputs, and the death targets without a horizon ignore censoring.

**Main points:** Target and cohort (issue 1); prediction point (issue 2); test window length (issue 3).

**Issues for Andrej:**

1. **Which target and cohort?**

   * **Problem:**
     - Cardoso et al. 2026 take all sites at 3 years; Woźniacki et al. 2024 and Shaktah et al. 2026 take colorectal cancer (C18-C20) with five targets.
     - Two of those targets (cancer death, overall death without a horizon) are a status cut at the release date[^leak24]; Woźniacki's horizon labels count patients lost to follow-up as deaths[^leak25].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | All sites, 3-year overall survival, alive patients followed under 3 years dropped (implemented) | Cardoso et al. 2026's task | the largest table; near balanced; topography as a feature | mixed cancers in every window |
     | B | Colorectal only, 3-year survival, same drop | Cardoso et al. 2023's cohort | one cancer; the paper's TabPFN numbers as a reference | about 72,500 rows |
     | C | Death without a horizon | `ULTINFO` 3 or 4 | the published endpoints | censored by the release date |
     | D | Horizon labels with the lost counted as deaths | Woźniacki's labels | published | 12-21% of the 3-year zeros in the 2000 file are alive patients lost |

   * **Recommendation:** A; B as the one definition instead if you prefer the single-cancer task (not both). **Decision:** A, B, C or D?

   [^leak24]: **LEAK-24** (Must): a target right-censored in the newest periods (a duration or a final status cut by the download date) is cut where follow-up is complete, or re-sourced from an archive with settled labels.
   [^leak25]: **LEAK-25** (Must): "No event" mixed with "not recorded" is a censoring bias: retire unless the recording process can be recovered; recovered includes unrecorded rows located by a rule that does not read the label, and dropped.
   [^prov7]: **PROV-7** (Must): records that share a source but give different tasks are not duplicates; the comments say why they are distinct.

2. **Prediction point: after first-course treatment, or at diagnosis?**

   * **Problem:**
     - The registry records the first-course treatment flags, the diagnosis-to-treatment interval and pathological TNM after surgery; all three papers used them[^use3].
     - Recurrence and follow-up fields go in either case[^leak10].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | After first-course treatment (implemented) | treatment flags and pathological TNM kept | the papers' feature sets; prognosis once treatment is under way | not a guide to choosing treatment |
     | B | At diagnosis | treatment and pathological TNM dropped | a first-visit prognosis | weaker; not what the papers scored |

   * **Recommendation:** A. **Decision:** A or B?

   [^use3]: **USE-3** (Must): name the prediction point: when the model is used and what is known then. A value that did not exist at that point is a leak.
   [^leak10]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target away; out: a column recorded after the outcome, a part, a consequence or another encoding of the target.

3. **Test window length?**

   * **Problem:**
     - Temporal by diagnosis date, with a 3-year gap so that every training label is final; the registry is updated quarterly[^split12].
     - 2020 (COVID) falls into one test window.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | One diagnosis year (implemented) | yearly windows | many windows of tens of thousands | 2020 as its own window |
     | B | Two diagnosis years | wider windows | steadier; 2020 shared with 2021 | half the windows |

   * **Recommendation:** A. **Decision:** A or B?

   [^split12]: **SPLIT-12** (Should): the horizon is a human judgment from the source: how far ahead the actor predicts, the competition's own test window, the refit cadence. Choose the test windows to match it.
