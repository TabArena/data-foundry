---
unique_name: cirrhosis_patient_survival_prediction
name: Cirrhosis Prediction Dataset
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 2
decision_markers:
- Outdated
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Dated'
- 'Target: Later'
collections:
- New (BeyondArena)
original_source: Other
year: '1991'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/fedesoriano/cirrhosis-prediction-dataset
- https://www.mayo.edu/research/documents/pbchtml/doc-10027635
- https://doi.org/10.24432/C5R02G
notebook_path: datasets/beyond_iid/new_iid/cirrhosis_patient_survival_prediction/cirrhosis_patient_survival_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/cirrhosis_patient_survival_prediction/dataset.py
source_row: 772
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Deaths-only target is intended: a survival-time task without censoring by design.** The leak audit (2026-09-24) flagged that the target (time to death) is defined only for patients who died, so censored patients are dropped. This is on purpose: the task is to predict the survival time of patients who die, not a censored survival analysis, so no change. The 36 of 161 rows with Drug/Ascites/Hepatomegaly/Spiders/Copper/Alk_Phos/SGOT missing are the non-trial patients (a cohort signal, not a leak).

Need to check for duplicates and original source.

Might be RCT data, not sure what the target might become?

Status contains censored data, need to figure out how to use and work with this.
Clearly a survival task as it seems.

We treat it as an uncensored time to death prediction task or similar as we do not score original survival prediction tasks so far.

**Assessment (AI, 2026-10-14):** The deaths-only target was right truncation. N_Days ends at death, transplant or the July 1986 analysis for every patient, and the IDs follow the registration order within the trial (1-312) and within the other patients (313-418): among the censored, Spearman of ID with N_Days is -0.96 and -0.87. Estimating each patient's registration from the longest follow-up of anyone registered at or after them in the same group, the median time to death is 3.98 years for the 74 deaths among 1974-76 registrations and 1.86 years for the 9 among 1982-84 (the earlier investigation had 4.35 and 1.86; its registration estimate differed). The population is not end-stage: Kaplan-Meier median survival 9.3 years (transplant censored); 157 of 418 patients have bilirubin at most 1.0, and 93% of them are alive without transplant at 5 years, yet a random forest fit on the deaths only (bilirubin, albumin, age, prothrombin) predicts them a median 4.7 years to death.
- New label: death (D) or transplant (CL) with N_Days at most 5 * 365.25 (day 1,826 or earlier) is 1; at least 5 years of follow-up without either is 0; the 5 patients lost to follow-up before 5 years (IDs 199, 234, 318, 321, 326) are dropped.
- Cohort: 304 patients, 107 positives (103 D, 4 CL), 238 in the trial and 66 outside it. The rule without the registration condition gives 329 / 132: the 25 extra are patients registered after about mid-1981 (12 D, 13 CL) whose follow-up could not reach 5 years, so they can only be positives (the other 84 late registrants are censored). On 329 the estimated registration year alone gives ROC AUC 0.61, on 304 0.52, so the definition keeps 304.
- ROC AUC on 304 (repeated stratified 3-fold, 10 repeats, untuned): logistic regression 0.87, random forest 0.89, LightGBM 0.86, bilirubin alone 0.86, registration year 0.52. Task probes on the shipped splits (30 of 60): linear 0.872, random forest 0.891, LightGBM 0.872, best single feature 0.792 (bilirubin in 23 splits), no flags. Leak probes: bilirubin alone 0.825; missing indicators 0.46-0.50 (being outside the trial carries no label signal); no test row has an exact copy in train.
- The features are the values at registration: the pbcseq documentation (R survival package) says "The F&H data set contains only baseline measurements of the laboratory parameters", and the drug is the randomised arm.
- Sources checked: Dickson et al. 1989 (Hepatology 10:1-7, abstract) built the Mayo model on the 312 trial patients and validated it on the 106 others, as an aid "in the selection of patients for and timing of orthotopic liver transplantation"; its abstract names survival as the endpoint, not transplant-free survival, so the definition does not call this the Mayo endpoint. Lammers et al. 2015 (Gastroenterology 149:1804-1812, the GLOBE score) predicts transplant-free survival (death or liver transplantation) of patients on ursodeoxycholic acid and reports 5- and 10-year predictions.

CC (2026-10-14, Lennart): New task: death or liver transplant within 5 years of registration, over the patients followed 5 years; replaces the deaths-only time to death.

CC (2026-10-14, Lennart): The 5-year task has a good target: marker `No Good Target (yet)` and the open `?` in required_split removed.

CC (2026-10-15, Andrej): Keep `Yes`; marker `Outdated` added. A real, non-trivial task whose risk ranking still holds today; no issue below leaks the outcome. Potential reasons to exclude, and why none is severe enough to act on:
- Outdated: the patients were treated 1974-86. Since the 1990s the liver disease (primary biliary cholangitis, PBC) is treated with a drug (ursodeoxycholic acid) that slows it, and liver transplants became common (here only 4 of 107 events). So the share of patients who die or get a transplant within 5 years (35% here) is much lower today. Not severe: the relation between the findings and the risk still holds today; the absolute risk is that of an earlier treatment era, named in the fit. The risk formula built on this cohort in 1989 (the Mayo score) ranks drug-treated patients about as well as the newer formulas built on them (GLOBE, UK-PBC): concordance (ROC AUC for survival) 0.76 vs 0.80 and 0.74 in 1,100 patients, differences not significant. Reference: Goet JC, Murillo Perez CF, Harms MH, Floreani A, Cazzagon N, Bruns T, et al. A Comparison of Prognostic Scores (Mayo, UK-PBC, and GLOBE) in Primary Biliary Cholangitis. Am J Gastroenterol. 2021;116(7):1514-1522. doi:10.14309/ajg.0000000000001285.
- Trivial (criterion 4C): the fixed 1989 Mayo formula (5 inputs: bilirubin, a blood marker of liver function; albumin; age; blood clotting time; fluid retention) reaches ROC AUC 0.901, and bilirubin alone 0.863. Not severe: TabPFN 3.5 reaches 0.907 and beats logistic regression (0.896) and random forest (0.893) by about 0.012 in 85% of splits (stratified 3-fold x 20), so better models are still rewarded; the gaps are small next to the fold SD of 0.027.
- Features a clinic would not have today: Stage (how scarred the liver is) needs a liver biopsy, a tissue sample that is rarely taken for this disease today; alone it gives ROC AUC 0.73. Drug is the arm of the 1970s trial (D-penicillamine or placebo), a drug no longer used for this disease. Not severe: both were recorded when the patient entered the study, so neither leaks the outcome, and Drug carries no signal (positive rate 0.317 on the drug, 0.347 on placebo).
- Drift: the blood clotting time (Prothrombin) is about 1 s lower for patients entering after 1977. Not severe for the random split: it is a change in the lab's measurement scale, not in the patients (within each period it predicts the label equally well, ROC AUC 0.72-0.73), and the label has no time trend (positive rate 0.33 / 0.39 / 0.34 by third of the entry years).

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — The source is a survival study (Cox model); our binary 5-year label is a derived task with no defined metric. The 5-year c-statistic used for GLOBE / Mayo risk scores equals ROC AUC on a binary label, so roc_auc also follows from context.

**Assessment (AI, 2026-10-27):** The open questions for the curator are in the record's Review (review of the Tiny Data datasets, written from the earlier findings, no review panel); the AI recommends shipping it. Priority 2: gap -, use case - (fit approximate: the treatment era), source + (the Mayo trial data, documented), shape -, risk +.
**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 2 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `Edema`, `Stage` (the README lists their levels).

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 1 scores are numbers (Stage).

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: the Mayo PBC cohort's 5-year death or transplant, the decision its source names; only the record's metric-based reason for keeping the old treatment era should be restated. Priority 2: gap 0, use case 0, source 1, shape 0, risk -0.

CC (2026-11-05, Andrej): ship as defined (issue 1, B); the `Outdated` bullet of 2026-10-15 now argues from the data, not the metric: the relation between the findings and the risk still holds today, and the absolute risk is that of an earlier treatment era, named in the fit. The declared split and metric checked and kept.

CC (2026-11-12, Andrej): random patients kept, as a stationary relation (BeyondArena v0.2 review page, issue 2, A). The measurement behind it is in the curation notes (`Time basis: StationaryRelation`): along the registration order the event rate is flat (34%, 40%, 34%, 35% by two-year period), the outcome is not autocorrelated (lag-1 -0.05, p 0.39; trial -0.11, p 0.08), the 10 nearest patients' event rate adds nothing (logistic regression ROC AUC 0.895 against 0.892), and the newest of three windows of 50 patients scores as high as random folds (0.921 against 0.861, untuned LightGBM). The tag enters the definition with PR #50. The declared split and metric checked and kept.

## Review

**Outcome:** added. The Mayo Clinic cohort of primary biliary cirrhosis, a slowly progressing autoimmune liver
disease (1974-1986; UCI 878 is a copy): 304 patients registered early enough to be followed 5 years, and whether they
died or received a liver transplant within 5 years (107 did). Reviewed without a panel, from the gathered evidence:
the record, the earlier checks of 2026-10-14 and 2026-10-15 and model runs on the shipped BeyondArena data.
The AI recommends shipping it as defined. Validity: Lennart replaced the deaths-only time to death, which was right
truncated (a late patient entered only with an early death; LEAK-23), by the 5-year outcome (CC 2026-10-14); the
features are the values at registration, and the registration order carries no label signal (ROC AUC 0.52), so a
random split fits. Andrej kept it with `Outdated` (CC 2026-10-15). Value: the fixed 1989 Mayo formula reaches ROC AUC
0.901 and TabPFN 3.5 0.907, ahead of logistic regression and a random forest in 85% of 60 splits, so `Trivial` is
not proven (TP-4). Quality: a shift of the clotting-time scale after 1977 is kept. Weighed: the source's own decision
(selecting patients for transplant) on a documented cohort, against an earlier treatment era. Left for Andrej: issue
1, one reason of the record to restate.

**Main points:** Nothing open. Settled: random patients kept as a stationary relation, the neighbour test, the flat
event rate and the windows' nil cost written into the curation notes (issue 2, A, 2026-11-12); ship as defined, the
treatment-era reason restated (issue 1, 2026-11-05).

**Record judgment:** valid with an approximate fit: the Mayo Clinic PBC cohort, the decision named by its source
(Dickson et al. 1989: selecting patients for liver transplant), from an earlier treatment era.

**Issues for Andrej:**

1. **Ship as defined, and restate the record's reason for keeping the treatment era?**

   * **Problem:**
     - The 5-year task (CC 2026-10-14, Lennart) and the keep with `Outdated` (CC 2026-10-15, Andrej) settle the
       definition, and nothing found since reopens it.
     - One reason in the CC of 2026-10-15 calls the treatment era not severe because "ROC AUC only scores the
       ranking", an argument from the metric that your later calls set aside[^1a].
     - Ship as defined, and restate that reason with the evidence that holds whatever the metric?
   * **Background:** the patients were treated 1974-1986, before ursodeoxycholic acid became the standard drug and
     while transplants were rare (4 of 107 events); 35% died or had a transplant within 5 years, far more than today.
     The reason that holds without the metric is in the same CC: the relation between the findings and the risk
     still holds, since the Mayo score built on this cohort in 1989 ranks today's treated patients about as well as
     the scores built on them (concordance 0.76 against 0.80 for GLOBE and 0.74 for UK-PBC in 1,100 patients,
     differences not significant; Goet JC, Murillo Perez CF, Harms MH, Floreani A, Cazzagon N, Bruns T, et al. A
     Comparison of Prognostic Scores (Mayo, UK-PBC, and GLOBE) in Primary Biliary Cholangitis. Am J Gastroenterol.
     2021;116(7):1514-1522. https://doi.org/10.14309/ajg.0000000000001285). The absolute risk is that of the earlier
     era, a known gap the definition names in `fit_reason` (fit approximate)[^1b].
   * **Experiments:**
     - CC 2026-10-15 (stratified 3-fold x 20): the fixed Mayo formula ROC AUC 0.901, bilirubin alone 0.863, TabPFN
       3.5 0.907, logistic regression 0.896, random forest 0.893; TabPFN ahead by about 0.012 in 85% of the splits,
       with a fold standard deviation of 0.027. Stage alone 0.73; Drug carries no signal (event rate 0.317 on the
       drug, 0.347 on placebo); the clotting time is about 1 s lower after 1977 but predicts equally well within each
       period (0.72 to 0.73), and the label has no time trend (0.33 / 0.39 / 0.34 by third of the entry years).
     - Model runs used the shipped BeyondArena task, the deaths-only time to death (161 rows), which v0.2
       replaced; they found that the patient order, which follows enrolment, carries that target, the right
       truncation the 5-year task removes. No number carries over to v0.2.
   * **Consistency:** age alone excludes no dataset: on 2026-10-15, 11 records marked `Outdated` were a plain `Yes`,
     among them horse_colic_survival and covertype. A separate metric review (2026-11-04) proposes log
     loss in place of ROC AUC for this dataset; that is decided there, and the restated reason holds under either.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship, record as is (implemented) | definition and record unchanged | nothing to do | the record argues from the metric |
     | B | Ship, restate the reason | definition unchanged; the CC's "Not severe" sentence on the era cites the Goet evidence and the gap named in `fit_reason` | the reason holds whatever the metric | an edit of your own comment |
     | C | Retire as outdated | `No (Retired)`; the folder leaves the working copy | no 1970s treatment era in the benchmark | a real task whose risk ranking still holds; age alone excludes no dataset |

   * **Recommendation:** B: the task stays as defined, and the record's reason no longer rests on the metric.
     **Decision:** as is (A), restate (B) or retire (C)?

   **Notes for the AI:** on B, replace in the `Outdated` bullet of the CC (2026-10-15, Andrej) the sentence "Not
   severe: ROC AUC only scores the ranking of patients by risk, and that ranking still holds today." with "Not severe:
   the relation between the findings and the risk still holds today; the absolute risk is that of an earlier
   treatment era, named in the fit." Keep the Goet reference; no definition change.

   [^1a]: Andrej's standing preference, from credit_g (2026-10-15) and heart_disease (2026-10-20): a blind spot of
     the metric we chose is no reason; severity is argued from the data and the use case.
   [^1b]: **USE-8** (Must): an approximate fit is a stand-in with a known gap, named as such in `fit_reason`.

   **Andrej (2026-11-05, change):** I go with B

   **Resolved (2026-11-05, Andrej):** ship as defined, the reason restated (B): the `Outdated` bullet of the CC of
   2026-10-15 now reads "Not severe: the relation between the findings and the risk still holds today; the absolute risk
   is that of an earlier treatment era, named in the fit.", with the Goet reference kept. No definition change; the
   declared split and metric checked and kept.

2. **Split by time, or keep the random split as a stationary relation?**

   * **Problem:**
     - New since your split mark of 2026-11-05: the registration order is recoverable from the source, since the IDs follow registration within the trial (1-312) and within the other patients (313-418), and a patient alive at the July 1986 analysis registered `N_Days` before it, which places the 304 kept patients from 1974 to mid-1981.
     - How the data was collected is information for the split: the patients arrived over 1974 to 1981 and a hepatologist scores new referrals, so the split you accepted is yours to revisit with that fact[^2a].
     - Split in windows of registration order, or keep the random patients as a stationary relation?
   * **Background:**
     - The order: within each group an isotonic fit of the censored patients' registration (July 1986 minus `N_Days`, 143 of the 304) on the ID gives every patient an estimate, exact in ID order within the group; the two groups merge by the estimate. Among the censored the ID follows `N_Days` with Spearman -0.96 and -0.87 (record, 2026-10-14).
     - The event rate shows no trend: 34% for patients registered 1974-1975, 40% for 1976-1977, 34% for 1978-1979, 35% for 1980-1981; the clotting time reads about 1 s lower after 1977 (issue 1).
     - The 5-year outcome closes for every patient by the 1986 analysis (the cohort rule keeps only such patients), so no window trains on an outcome cut short; a gap of the label's delay (5 years) would leave no training patient for any window[^2b].
   * **Experiments:** the definition's 304 patients and features, untuned LightGBM and logistic regression (LR), ROC AUC; three windows of 50 patients from the newest (registered about mid-1978 to mid-1981), each trained on every earlier patient (51%, 67% and 84% of the rows):

     | Split | LightGBM | LR | Event rate in test |
     |---|---|---|---|
     | A, random 3 x 20 folds (implemented) | 0.861 (fold SD 0.035) | 0.874 (0.031) | 35% |
     | B, newest window (1980.5 to 1981.5) | 0.921 | 0.846 | 44% |
     | B, three windows, newest first | 0.921, 0.837, 0.928 (mean 0.895) | 0.846, 0.870, 0.910 (mean 0.875) | 44%, 22%, 40% (training 34% to 36%) |

     - On the same test rows of the two older windows, training on as many patients drawn at random from all others (later ones included) scores 0.853 and 0.884 (LR 0.866 and 0.894): no gain from later patients.
     - A check of October 2026 with TabPFN 3.5 found the same: trained on the oldest two thirds, 0.916 on the newest third, against 0.907 on random folds (CC 2026-10-15).
     - With 50 patients and 11 to 22 events a window's ROC AUC moves by about 0.04, as much as the fold SD of the random split; the estimated registration year as a feature changes the windows by 0.003 (LightGBM).
   * **Effect on the task:** random folds test patients referred in the same years as the training patients; windows test later referrals with the history a clinic had. The measured cost of the random split is nil, so the choice is what the split claims and how precise the score is: 60 folds of 101 patients against 3 windows of 50.
   * **Consistency:** distribution_transformers_at_cauca_department and the other forced splits measured their cost on the valid windows the same way; infrared_thermography_temperature kept a random split over a measured shift in time, as a calibration with no signal across time; this task predicts later patients[^2c].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random patients (implemented), as a stationary relation | stratified random 3 x 20 folds; definition tag `StationaryRelation`, its `Time basis:` line giving the flat event rate and the windows' nil cost | 60 folds, a precise score; nothing measurable lost (the windows score as high or higher), which is the check the prototype asks | tests patients of the same years as training; a recovered order left unused; the target is a 5-year outcome rather than a present state, so the prototype rests on the measurement alone |
     | B | Windows of registration order | a registration rank built from the ID order and the censored patients' dates; 3 windows of 50 patients back from the newest | tests later referrals, as a clinic meets them; no outcome cut short | three test sets of 50 patients, about 0.04 ROC AUC of noise each; the order of the 161 patients who died or were transplanted is interpolated between dated neighbours |

   * **Recommendation:** B: the order is in the source, the use case scores later referrals, and the windows meet the size rules; A stays defensible as a stationary relation, since the event rate is flat and the random split measurably flatters nothing here. **Decision:** windows (B), or random patients as a stationary relation (A)?

   **Notes for the AI:** on B, in `_clean` before `drop_columns`: per group (`ID <= LAST_TRIAL_ID` and the rest), `IsotonicRegression(out_of_bounds="clip")` fitted on the censored patients (`Status == "C"`) of `1986.5 - N_Days / 365.25` against `ID`, predicted for every patient; `df["registration_rank"]` the rank of (estimate, ID) over the kept patients, 1 to 304 (a rank, so no follow-up time ships as a value; it is a feature, as a time column is); `temporal = Temporal(on="registration_rank", splits=TemporalSplits(window=50, unit="rows", n_windows=3))`; `splits_comment`: three windows of 50 referrals, expanding training, no gap since every 5-year outcome closed by the 1986 analysis and a 5-year gap leaves no training patient; rewrite the task summary's `split` and `fit_reason` (drop "so a random split fits"); a curation note with the order evidence; record `required_split` `Temporal (NON-IID)`; `dataset check`, rebuild. On A, once PR #50 is in: the definition tag `StationaryRelation` (no date column, so no `meta_time_present_unused` to accept) and the curation note "- Time basis: StationaryRelation: the IDs follow registration within the trial and within the other patients, and the censored patients' follow-up dates it (1974 to mid-1981); the event rate shows no trend over the years (34%, 40%, 34% and 35% by two-year period), and the newest of three windows of 50 patients scores ROC AUC 0.921 against 0.861 on random folds (untuned LightGBM; logistic regression 0.846 against 0.874), with no gain from later patients at equal training size", followed by the reason of your decision. Under either option the record gets the tags `Samples: Over Time` and `Time: Dated` (it carries `Non-IID (Temporal)` now).

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record's collection facts and, where one fits, the definition's use-case prototype with its `Time basis:` line. **SPLIT-14** (Must): at least 3 windows, none trained on less than half of the data. **SPLIT-17** (Should): widen windows below about 50 test rows.
   [^2b]: **SPLIT-10** (Should; amended 2026-11-05): a label known only after a delay gets a gap of about that delay, except where a fixed outcome horizon, every label final at release, removes the selection by the outcome; a gap that breaks the floor of SPLIT-14 is an exception.
   [^2c]: **SPLIT-8** (Must): a forced split measures its cost against the valid windows where the data has any (distribution_transformers_at_cauca_department: ROC AUC 0.648 trained on 2019 and tested on 2020, against 0.639 on random folds). **SPLIT-31** (Should): IID can match how a task is framed even when it is optimistic (infrared_thermography_temperature: IID kept over a measured year-to-year shift, 2026-10-21, Lennart).

   **Andrej (2026-11-12, discuss):** In this dataset, is it fair to assume that neighboring samples closer in time
   influence each other somehow?

   **Answer (AI, 2026-11-12):** no. Patients registered next to each other share nothing beyond their findings: the
   outcome is not autocorrelated along the registration order, and the outcomes of the nearest patients add nothing
   to a model.

   * The patients are separate referrals to the Mayo Clinic with an autoimmune disease that does not spread from one
     patient to another. The 238 trial patients were randomised, double blind, to D-penicillamine or placebo, so the
     order decides no treatment (and the drug carries no signal, issue 1).
   * No outcome could pass from one patient to the next: the label is a 5-year outcome, so when a patient registered,
     the outcomes of the patients just before were still years away.
   * What patients close in time do share is the era: the clotting-time scale moved by about 1 s after 1977 (issue
     1). That is a slow shift with no effect on the label, not one patient influencing another.

   | Along the registration order (lag-1 autocorrelation; permutation p, 2,000 shuffles) | All 304, estimated order | 238 trial patients, exact ID order |
   |---|---|---|
   | Outcome | -0.05 (p 0.39) | -0.11 (p 0.08) |
   | Outcome minus the findings' prediction (logistic regression, out of fold, ROC AUC 0.901) | -0.08 (p 0.15) | -0.06 (p 0.40) |
   | Bilirubin (log), albumin, clotting time, stage, oedema | -0.03 to 0.06 (p 0.32 to 0.86) | -0.02 to 0.08 (p 0.24 to 0.97) |
   | Age | -0.11 (p 0.06) | -0.16 (p 0.015) |

   | Logistic regression, stratified 3-fold x 20 | ROC AUC |
   |---|---|
   | findings at registration | 0.895 (SD 0.026) |
   | + event rate of the 10 training patients nearest in registration order | 0.892 (SD 0.025) |

   - The neighbours' event rate alone scores 0.52 to 0.54 (5 to 10 neighbours) and does not correlate with what the
     findings miss (r -0.08 to 0.02).
   - In blocks of 51 patients the event rate moves from 24% to 43%, and the findings' predicted rate moves with it
     (27% and 35% in the lowest and highest blocks): the swings follow who was referred, near the binomial noise of
     51 patients (SD about 7 points).
   - The one signal is age in the trial (consecutive IDs alternate slightly in age, p 0.015 among 18 tests); it does
     not reach the outcome.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | A | Random patients (implemented), as a stationary relation | 3 x 20 stratified folds; `StationaryRelation` with its `Time basis:` line once PR #50 is in | rows measured independent in order and in outcome; 60 folds, a precise score | tests patients of the same years as training |
   | B | Windows of registration order | 3 windows of 50 later referrals, expanding training | tests later referrals | 3 test sets of 50 (about 0.04 ROC AUC noise each) on an interpolated order, guarding against a dependence the data does not show |

   * **Recommendation:** A, changed from B: neighbours do not influence each other, the event rate has no trend, and
     the windows cost nothing measurable either way (issue 2's experiments), so the random split loses no realism
     and keeps 60 folds. **Decision:** A or B?

   **Andrej (2026-11-12, discuss):** Reply (A): Random patients, as a stationary relation. Also document your
   experiment.

   **Resolved (2026-11-12, Andrej):** A: the random 3 x 20 stratified folds stay. A curation bullet `- Time basis:
   StationaryRelation: ...` documents the measurement: the order (IDs, dated by the censored patients' follow-up,
   1974 to mid-1981), the flat event rate (34%, 40%, 34%, 35%), the lag-1 autocorrelations of the outcome (-0.05; trial
   -0.11), of what the findings miss (-0.08) and of age (trial -0.16, not reaching the outcome), the neighbours' event
   rate adding nothing (0.895 against 0.892), and the newest window against random folds (0.921 against 0.861,
   LightGBM); it ends with what the split cannot test. The tag `StationaryRelation` enters `data_tags` once PR #50 is
   in the working copy. The record already carries `Samples: Over Time` and `Time: Dated`; record CC line. `dataset
   check`: 0 errors, 0 warnings, 0 info; README regenerated (curation notes only); not rebuilt.

## Reference

Fleming, T.R. and Harrington, D.P. (1991) Counting Processes and Survival Analysis. Wiley Series in Probability and Mathematical Statistics: Applied Probability and Statistics, John Wiley and Sons Inc., New York.

(get correct version ref)

Real
