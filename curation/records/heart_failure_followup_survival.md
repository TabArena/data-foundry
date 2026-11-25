---
unique_name: heart_failure_followup_survival
name: Heart Failure Clinical Records
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: 'Yes'
decision_markers:
- Class-dependent Recording
tags:
- Tiny Data
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Later'
- Clinical Study
collections:
- New (BeyondArena)
original_source: Other
year: '2017'
collection_period: Apr 2015 - Dec 2015
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5Z89R
notebook_path: datasets/beyond_iid/new_iid/heart_failure_followup_survival/heart_failure_followup_survival.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/heart_failure_followup_survival/dataset.py
source_row: 766
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed: dropped `time` (follow-up days), which is only known after the outcome.** Chicco & Jurman 2020 (BMC Med Inform Decis Mak 20:16), Table 1: "Time | Follow-up period | Days | [4,...,285]" and "death event | If the patient died during the follow-up period"; the source study (Ahmad et al. 2017, PLOS ONE 12:e0181001) is a survival analysis with "dead and censored patients at the end of follow up period". Follow-up ends at death or censoring, so early deaths get short times (Chicco & Jurman, Fig. 4: 88.6% of month-0 patients died). Alone it gives ROC AUC 0.84; LightGBM 0.90 -> 0.75 without it (leak audit 2026-09-24). The label is still "died within a patient-specific follow-up of 4-285 days", so some censored patients may have died later.

Looks good

**Assessment (AI, 2026-10-14):** whether follow-up ended on one date for all patients cannot be determined: Ahmad et al. 2017 and Chicco & Jurman 2020 do not say, and neither file has dates. The censored follow-ups (12 to 285 days) fit a common end around mid-January 2016 but do not prove it. Each patient's window starts at their own admission, so the task stays as it is (Lennart's instruction).

CC (2026-10-21, Andrej): The rows are 299 heart-failure patients (Faisalabad, 2015); the source label is death during a follow-up of 4-285 days that differs by patient. Keep, with the label and three lab columns fixed in `dataset.py` (not built).
- **Problems found:**
  - Creatinine filled with the outcome's group mean: serum creatinine (a blood marker of kidney function) is exactly 1.18 in 11 rows, all survivors, and 1.83 in 8 rows, all deaths, the two group means in Ahmad et al. 2017, Table 1. Models use it: TabPFN 3.5 log loss on these rows is 0.27, against 0.41 once the values are neutralised.
  - Undocumented mean filling: creatine phosphokinase (CPK, a muscle enzyme) is the column mean 582 in 47 rows, and platelets the column mean 263358.03 in 25 rows. Neither paper mentions missing values.
  - "Survived" often meant "not followed long enough": 55 of the 203 survivors were followed for under 100 days. A Kaplan-Meier estimate (the standard survival curve) puts about 31 deaths within 285 days among them.
  - Minor: anaemia among deaths is 46 in the file, 54 in the paper.
- **Fixed:**
  - The target is death within 60 days; the 8 survivors followed less than 60 days are dropped (291 rows, 54 deaths). 30 days would leave 35 deaths, 90 days would drop 45 survivors.
  - The 91 filled-in values are missing again.
  - The citation is Ahmad et al. 2017, which published the data, instead of the later re-analysis by Chicco & Jurman 2020.
  - The fixed task keeps its signal: TabPFN 3.5 ROC AUC about 0.72, logistic regression about 0.68 (20 x 3 splits).
- Reference: Ahmad T, Munir A, Bhatti SH, Aftab M, Raza MA. Survival analysis of heart failure patients: A case study. PLoS One. 2017;12(7):e0181001. doi:10.1371/journal.pone.0181001

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback roc_auc — Ahmad et al. 2017 (first publication) score a Cox model by time-dependent ROC AUC, which needs the follow-up time we drop (leak); Chicco & Jurman 2020 (the binary task we ship) rank by MCC at threshold 0.5, a default threshold, not a decision (MET-6). roc_auc is the binary fallback.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `zigong_heart_failure_mortality` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the target rule (CLEAN-25) and the cut-end rule (CLEAN-14): the target ships as No/Yes, Yes the event (1 is the event).

CC (2026-11-05, Andrej): ship as defined (Review issue 2, A). The declared split (random patients) and the declared metric (ROC AUC on death within 60 days) checked and kept.

CC (2026-11-11, Andrej): Review issue 3, option B, forced from temporal: the random split is tagged `ForcedIIDFromTemporal` (SPLIT-8) with a `Time basis:` line: patients admitted April to December 2015, only the survivors' admissions can be dated from the follow-up, so no split by admission date can be built without the outcome. The default split and the record's collection facts stay.

CC (2026-11-17, Andrej): the declared split (random, 20x3 folds, `ForcedIIDFromTemporal`) is checked: the split decision tree, walked without the current split, reaches the split it ships (blind split walk).

CC (2026-11-18, Andrej): the forced tag stays (Review issue 4, A; stationarity reasoning, SPLIT-32 as amended today): no reason to take later samples as interchangeable. Treatment changes move survival given the same findings, and the label itself depends on admission time; against outweighs the short span.

**Assessment (AI, 2026-11-23):** the 60-day label and the source-filled lab values set back to missing (CC 2026-10-21) re-applied on the current definition with the `Class-dependent Recording` marker; the `Time basis:` line now says that the 2026-11-18 point on a label depending on admission time held for the old all-follow-up label, which the 60-day horizon fixes.

## Review

**Outcome:** added. Of the 299 heart-failure patients of Ahmad et al. 2017 (Faisalabad, 2015), 291 remain, and the task
is whether they died within 60 days. Reviewed without a panel, from the gathered evidence: the record, the earlier
checks of 2026-10-21 and model runs on the shipped BeyondArena data. Kept with fixes on Andrej's review of
2026-10-21 (issue 1, resolved); the AI recommends shipping it as defined. Validity: the follow-up time is dropped as a
leak (Lennart, 2026-09-30); the label is death within 60 days over the patients followed that long, instead of death
during a follow-up of 4 to 285 days that differed by patient; the 91 filled-in lab values are missing again, among them
19 creatinine values filled with the mean of the patient's outcome group, which gave the label away (LEAK-10). The
model runs used the shipped BeyondArena task, which still has the follow-up time: their best models read the
outcome from it (survivors' follow-up ends in enrolment batches), which confirms the drop; no number carries over to
v0.2. Value: TabPFN 3.5 reaches ROC AUC about 0.72 and logistic regression 0.68 (20 x 3 splits); the probes raise no
flag. Quality: the anaemia count among deaths differs from the paper (46 against 54), kept. The marker
`Class-dependent Recording` (2026-10-27) records the undone fill and does not change the verdict. Weighed: a
documented cohort repaired to a fixed-horizon label, against its small size and an unusual 60-day horizon. Stationarity reasoning of 2026-11-18: the definition reaches the forced step with no time to measure; the forced
tag stays (issue 4).

**Main points:** All issues resolved: shipped as defined (issue 2, 2026-11-05); the random split is tagged
`ForcedIIDFromTemporal`, as only the survivors' admissions could be dated (issue 3, 2026-11-11), and stays so (issue 4,
A, 2026-11-18). Nothing is left open.

**Record judgment:** valid with an approximate fit: a real cohort of 299 heart-failure patients (Faisalabad, 2015),
repaired to a fixed-horizon label; small, with an unusual horizon. The data-scouting run of 2026-10-31 screened
`zigong_heart_failure_mortality` (AI-filled, unverified): 2,008 admissions of one Chinese hospital on PhysioNet, whose
publisher's target is readmission and where death is rare (about 3% at 6 months), so it does not replace this task.

**Issues for Andrej:**

1. **Ship in TabArena v0.2 as defined?**
   - Checked and settled: the follow-up time dropped as a leak (CC 2026-09-30, Lennart); the 60-day label, the filled
     values set to missing and the citation of Ahmad et al. 2017 (https://doi.org/10.1371/journal.pone.0181001), which
     published the data (CC 2026-10-21, Andrej). After the fix, missing-value indicators score ROC AUC 0.45 to 0.50
     and the number format alone 0.48, so no recording trace of the class is left.
   - Kept on purpose: 60 days is not the usual horizon (30 days or 1 year); 30 days would leave 35 deaths and 90 days
     would drop 45 survivors. Where follow-up starts and when the blood values were taken is not stated; Andrej
     judged on 2026-10-21 that this does not matter. The larger Zigong cohort on PhysioNet is restricted access, so
     there is no public replacement.
   - Recommendation: ship. Decision: ship as defined, or name what is missing.

   **Resolved (2026-10-21, Andrej):** kept, with the 60-day label, the 91 filled-in lab values set back to missing and
   the citation of Ahmad et al. 2017 (CC 2026-10-21); the target ships as No/Yes with Yes the death (CC 2026-11-01,
   Lennart). Nothing found since reopens it.

2. **Ship as defined?**

   * **Problem:**
     - Nothing open was found: the review of 2026-10-21 fixed the label and the outcome-filled lab values, and the
       evidence since (model runs, the screened Zigong cohort) raises no new question.
   * **Experiments:** after the fixes, TabPFN 3.5 ROC AUC about 0.72 and logistic regression 0.68 (20 x 3 splits);
     missing-value indicators 0.45 to 0.50 and the number format alone 0.48, so no recording trace of the class is
     left.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 291 patients, death within 60 days | a documented cohort with a fixed-horizon label | small, with an unusual horizon |
     | B | Retire | `No (Retired)`; the folder leaves the working copy | none found | a real, repaired task leaves |

   * **Recommendation:** A. **Decision:** ship (A) or retire (B)?

   **Resolved (2026-11-05, Andrej):** ship as defined (A); the declared split and metric checked and kept.

3. **Time basis: name the random split forced from temporal (`ForcedIIDFromTemporal`)?**

   * **Problem:**
     - Patients were admitted from April to December 2015, each followed from their own admission, and the time can
       be read back only for survivors: with one common end of follow-up (about mid-January 2016) a survivor's
       admission is the end minus the follow-up, while a death's follow-up is the time to death, so a split by
       admission date would be built from the outcome.
     - The record's collection facts fit what was found (`Samples: Over Time`, `Time: Lost`, `Target: Later`), the
       random split was checked and kept on 2026-11-05, and the definition names no time basis.
     - The use case estimates the risk of patients to come, and none of the four prototypes fits a prognosis with
       staggered entry, so the forced tag is the one that fits: name it, or another one?
   * **Background:** the questions that tell the time bases apart[^3a]:
     - Can time affect the target? Yes in principle: 60-day mortality follows care and season.
     - Does the use case predict for a time after its data? Yes: a cardiologist estimates a new patient's risk.
     - One shared prediction moment? No: each patient at their own admission, so a delayed target does not fit,
       though the 60-day window is fixed and closed for every patient kept.
     - Does arrival over time move the target? Argued from the source, as nothing dated can measure it: over nine
       months at two hospitals a change is possible but not reported; a stationary relation fits a present state (a
       diagnosis), not a death in the next 60 days. With the time lost that is the forced case[^3b].
     - The time facts behind the cohort, as decided on 2026-10-21: the 8 survivors followed less than 60 days are the
       late admissions; deaths of late admissions stay, which the 60-day label accepts.
   * **Experiments:** today's checks on the source file (299 patients), model-free: the file is sorted by follow-up
     time (rank correlation with the row 0.9999), which the time probe reads as sorted by the target; follow-up runs
     12 to 285 days for the 203 censored patients and 4 to 241 days for the 96 deaths. The leak test across a forced
     split: one row per patient, the outcome-filled creatinine undone (2026-10-21), no order in the frame; whether
     patients of one period share their outcome cannot be tested.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No time basis (implemented) | no time tag; `dataset check` notes a split that is not temporal and does not say why | nothing changes | the score's meaning in time is not stated |
     | B | Forced from temporal | the tag `ForcedIIDFromTemporal` and a `Time basis:` line on the nine months and the survivors-only dates | says what the random score stands for; keeps the split kept on 2026-11-05 | none found |
     | C | Stationary relation | the tag `StationaryRelation` and a line arguing that baseline findings predict 60-day death alike over nine months | a short period at two hospitals | the prototype is for a present state; nothing dated to measure it on, as only survivors can be dated |

   * **Recommendation:** B: a forward use case whose time cannot be recovered without the outcome is what the forced
     tag names. **Decision:** no time basis (A), forced (B) or stationary relation (C)?

   **Notes for the AI:** once the time-basis tags are in, on B: `data_tags = ("ForcedIIDFromTemporal",)` and the curation bullet
   "- Time basis: ForcedIIDFromTemporal: heart-failure patients admitted from April to December 2015, each followed
   from their own admission; the follow-up time dates the survivors (one end of follow-up, about mid-January 2016)
   but not the deaths, so no split by admission date can be built without the outcome, and random patients stand in
   for the patients to come. A release with admission dates would allow a split by date."; no `splits_comment`
   (default split); the record's facts stay.

   [^3a]: **SPLIT-32** (Should): how and when samples, features and the target arrive is information for the split;
     a definition can name the use-case prototype it follows (`Timeless`, `Snapshot`, `DelayedTarget`,
     `StationaryRelation`) with a `Time basis:` line; a delayed target needs one shared prediction moment, a
     stationary relation reads a present state through a relation time does not move; a forward task whose time is
     lost is forced.
   [^3b]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows ships in the
     closest regime that keeps the rows, tagged as forced from temporal, after a leak test across the split; it says
     what a dated release would change.

   **Resolved (2026-11-11, Andrej):** B: `data_tags = ("ForcedIIDFromTemporal",)` and the drafted `Time basis:` bullet in
   `curation_comments` (a split by admission date needs a release with admission dates); the default split and the
   record's facts unchanged; `dataset check` rerun.

4. **Keep `ForcedIIDFromTemporal`, or tag `AssumedStationaryRelation`?**

   * **Problem:**
     - Time: Lost for the split: admissions April-December 2015; follow-up time dates survivors only (end ~mid-January 2016), not deaths, so no outcome-free order.
     - Use: A cardiologist estimates death risk in the coming months for heart-failure patients after 2015.
     - Mechanism: Ejection fraction, creatinine, sodium and age to death: physiology, but mortality given these depends on therapy, which changed (ARNI, SGLT2 inhibitors, guideline-directed therapy).
   * **Background:** similar datasets[^asr].

     | Similar dataset or source | What was measured | Verdict | Why similar |
     |---|---|---|---|
     | 2_month_survival_rate_prediction (SUPPORT) | v3 stationary-relation test, phase I 1989-91 -> phase II 1992-94, death ROC AUC forward vs contemporaneous | flat (LightGBM gap 0.0008, TabPFN gap 0.0027) | clinical prognosis of hospitalised patients from admission physiology, one 3-year step |
     | McDonagh TA et al., 2021 ESC Guidelines for heart failure, Eur Heart J 2021;42:3599-3726 (literature, cited from memory: check) | four-pillar therapy (ARNI, beta-blocker, MRA, SGLT2i) with mortality benefit | changed treatments | HFrEF prognosis after 2015 |
     | Davis SE et al., 'Calibration drift in regression and machine learning models for acute kidney injury', JAMIA 2017;24(6):1052-1061 (literature, cited from memory: check) | VA hospital models over 9 years | discrimination stable, calibration drifted | routine-lab clinical risk model used years after fitting |

   * **For a stationary use case:**
     - nine months of collection.
     - SUPPORT tested flat over a 3-year step for hospital prognosis.
   * **Against:**
     - changed treatments since 2015 lower mortality at the same EF/creatinine.
     - variable follow-up 4-285 days: label depends on admission month (later admissions censored earlier)
     - single Faisalabad setting.
   * **Earlier views:**
     - Time basis line (Andrej, 2026-11-11, issue 3): no split by admission date can be built without the outcome.
     - CC 2026-11-17 (Andrej): random 20x3 checked by blind walk.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `ForcedIIDFromTemporal` (implemented) | The folds stay; the Time basis line names the reasoning below | Claims only what is known | The split stands for later samples only as far as the use case is stationary |
     | B | `AssumedStationaryRelation` | The folds stay; you give the reason (eight words or more) | Documents why random folds stand for later samples | changed treatments since 2015 lower mortality at the same EF/creatinine; variable follow-up 4-285 days: label depends on admission month (later admissions censored earlier) |

   * **Recommendation:** A, treatment changes move survival given the same findings, and the label itself depends on admission time; against outweighs the short span. Confidence: high. **Decision:** A or B?

   [^asr]: **SPLIT-32** (Should; amended 2026-11-18, Andrej): "where it holds none, the review reasons whether the use case can be taken as stationary, from the domain's mechanism and from similar datasets ..., where the AI offers `AssumedStationaryRelation` with a recommendation for a person to decide." `AssumedStationaryRelation` keeps the forced split's folds and replaces only the tag; its line opens `AssumedStationaryRelation (<person>, <date>): <reason>`.

   **Andrej (2026-11-18, ok):** as implemented.

   **Resolved (2026-11-18, Andrej):** A, as implemented: the forced tag stays; the `Time basis:` line gives the reasoning (Treatment changes move survival given the same findings, and the label itself depends on admission time; against outweighs the short span.)

## Reference

@article{ahmad2017survival,
  title={Survival analysis of heart failure patients: A case study},
  author={Ahmad, Tanvir and Munir, Assia and Bhatti, Sajjad Haider and Aftab, Muhammad and Raza, Muhammad Ali},
  journal={PLOS ONE},
  volume={12},
  number={7},
  pages={e0181001},
  year={2017},
  publisher={Public Library of Science},
  doi={10.1371/journal.pone.0181001}
}
