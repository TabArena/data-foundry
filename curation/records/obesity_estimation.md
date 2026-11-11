---
unique_name: obesity_estimation
name: Estimation of Obesity Levels Based On Eating Habits and Physical Condition
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
suggestion: No (Retired)
decision_markers:
- Data Quality Issue
- Selection Bias
- No Good Target / Scientific Discovery
tags:
- Tiny Data
- 'Samples: One Moment'
collections:
- New (BeyondArena)
- TabSTAR
original_source: UCI
year: '2019'
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.24432/C5H31Z
- https://www.openml.org/search?type=data&id=46597&sort=runs&status=active
- https://www.kaggle.com/datasets/fatemehmehrparvar/obesity-levels
notebook_path: datasets/beyond_iid/new_iid/obesity_estimation/obesity_estimation.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/obesity_estimation/dataset.py
source_row: 673
type_adapter_id: curation-record-v1
---

## Comments

"77% of the data was generated synthetically using the Weka tool and the SMOTE filter, 23% of the data was collected directly from users through a web platform."

No problem! We can filter the SMOTE data as they are clearly different (float instead of int) values and later in the file. Filter them and then use, might become trivial

Maybe need to transform labels (bins) back to Mass body index regression value instead?...
Need to recompute the body index, remove weight and height which give the target

TODO: remove height / weight, make regression task, remove SMOTE samples

**Assessment (AI, 2026-10-14):** the first 498 rows are the real answers. Their class counts (34/287/58/58/47/11/3) equal Fig. 1 of Palechor & De la Hoz 2019, all 287 Normal_Weight rows are among them, and the later rows come in per-class blocks whose totals match Fig. 2 (2,111 rows). 1,598 of the 1,613 later rows have values with 3 or more decimals; the other 15 are whole-number SMOTE rows between identical neighbours, so a filter on values would let them in. The 498 rows hold 10 exact duplicates (488 distinct).

**Assessment (AI, 2026-10-14):** the 498 real rows hold 10 exact copies in 8 groups (rows 97/98, 105/106, 208/209, 466/467, 295/309, 282/460, 443/496, and 145/174/179/184). Each repeats all 16 answers, age, height to the centimetre and weight to the kilogram. Of the 14 rows that repeat another row's answers, 10 also repeat height and weight, which different people would almost never do, and two more are neighbouring rows that differ only in height (rows 420/421: 1.85 and 1.84 m), like a corrected resubmission. So they are the same person sending the web form again.

CC (2026-10-14, Lennart): Drop the duplicates: 488 rows.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — The source is a data descriptor for a 7-class obesity-level task with no defined evaluation metric, and we changed the task to BMI regression (weight and height dropped), so no source metric applies.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): 7 ordinal scales typed as ordered categories in the codebook's order (CLEAN-14, amended): `FCVC`, `NCP`, `CAEC`, `CH2O`, `FAF`, `TUE`, `CALC` (the README lists their levels).

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `nhanes_bmi_from_habits` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-01, Lennart): the decode rule (a code whose codebook says in words what each level is carries the words; a score without them is a number): 5 coded columns carry their words.

CC (2026-11-11, Andrej): retired (`No (Retired)`, `No Good Target / Scientific Discovery`; BeyondArena v0.2 review page, issue 1, B): the source's own tool takes weight and height, and its label is the body mass index class computed from them, so the published task is circular. Without weight and height only a target we built is left, a body mass index from habit answers that no source and no stated user predicts where a scale is at hand. The folder stays until the retirement PR removes it and clears `v2_path`.

CC (2026-11-11, Andrej): task text rewritten (issue 2, B): the question names age, sex and family history, which carry about 90% of the gain over the mean; the use case no longer says the source's tool works from habits alone. The self-reported, rounded weights (40.8% at multiples of 5 kg) and the 37 minors are noted in the curation comments. Time basis (issue 3, B): the random split is a `Snapshot` of the 30-day survey, with the tag in `data_tags` and its bullet in the curation comments. Data unchanged; `dataset check` 0 errors.

## Review

**Outcome:** added. Web-questionnaire answers from Mexico, Peru and Colombia (UCI 544; Palechor and De la Hoz Manotas
2019, https://doi.org/10.1016/j.dib.2019.104344): the body mass index predicted from sex, age, family history and 11
habit answers, over the source's 488 real respondents. Retired on 2026-11-11 (issue 1, B).
Reviewed on 2026-11-04 without a panel, from the gathered evidence (the record, an earlier check on the v0.2 rows, the
model runs on the shipped data, one new check); both issues of 2026-10-27 are still open. Validity: the 1,613
synthetic rows and 10 repeated submissions are dropped (Lennart, 2026-10-14); the source's obesity level is a fixed
rule on weight and height, so both are dropped and the body mass index is predicted from the other answers, the
remedy the rule for labels computed from the columns names. Andrej disputes that anyone makes this prediction (issue
1). The leak found earlier on the shipped data (repeated submissions that give away a test row's BMI) is the one v0.2
already drops: a check on the v0.2 rows finds 4 pairs that share all 14 answers but differ in BMI, none an exact copy.
Value: the signal is real (TabPFN R² 0.18, shuffled labels -0.01) and tuned methods spread. Quality: the ordinal
answers are typed and decoded since 2026-10-30/11-01; weights are rounded and 37 respondents are minors (issue 2). A
measured national version of the task (`nhanes_bmi_from_habits`) was found on 2026-10-31; it is not added and its use
case is as thin. Weighed: real answers and a documented source +, real signal and spread +, a target we built and a
prediction nobody may need -, signal mostly demographic -.

**Main points:** Retired (issue 1, B, 2026-11-11): the source's tool takes weight and height, and nobody predicts
a body mass index from habits alone. The folder leaves in a retirement PR. Issues 2 and 3 were resolved the same day.

**Record judgment:** real survey answers with a target we rebuilt from the source's own rule; the signal is real but
mostly demographic, and the use case is one the source states but nobody would need where a scale is at hand.

**Issues for Andrej:**

1. **Retire, because nobody estimates a body mass index from habit answers?**

   * **Problem:**
     - The source labels each respondent with an obesity level computed from the reported weight and height, so we
       dropped both and predict the body mass index (weight over height squared) from sex, age, family history and
       the habit answers.
     - The same form asks for weight and height, and `fit_reason` already says a body mass index "is measured with a
       scale and a tape in a minute", so the task may be one nobody makes.
     - Retire it, or keep it as an approximate fit?
   * **Effect on the task:** the use case is a tool that flags a risk of overweight without weight and height, which
     the source names as its aim ("estimation of obesity levels based on eating habits and physical condition"). If
     no one makes that decision, the task is a constructed one.
   * **Experiments:**
     - An earlier check on the v0.2 rows (60 splits, 20 x 3-fold): TabPFN-3.5 R² 0.18, above the training mean on 60
       of 60; on shuffled labels -0.01 (20 splits). A spline on age with sex and family history reaches RMSE 4.38
       against 4.79 for the mean and 4.33 for TabPFN on all 14 features, so the 11 habit answers add 0.047 RMSE
       (better on 45 of 60 splits).
     - On the BeyondArena results the tuned methods beat the dummy on 29 of 29 folds and spread (Kendall's W 0.65).
     - Model runs on the shipped data (498 rows with the repeated submissions; 40 benchmark methods, 20 x 3
       splits): RMSE 4.28 (TabDPT) to 4.55 (default random forest), median 4.37; a ridge scorecard on age splines and
       the one-hot answers ranks 12th of 41 (4.33).
   * **Background:** a measured version of the task was found on 2026-10-31, `nhanes_bmi_from_habits` (CDC's NHANES:
     measured BMI with diet, activity, alcohol and smoking questions of thousands of adults); it is an AI screening,
     not added, and its use case is as thin as this one's. Whether a better version exists is a separate question
     from whether this task is valid[^1d].
   * **Consistency:** account_debt_south_africa is the case of dropping a rule's inputs and keeping the rest[^1a].
   * **Sources:** Palechor FM, De la Hoz Manotas A, "Dataset for estimation of obesity levels based on eating habits
     and physical condition in individuals from Colombia, Peru and Mexico", Data in Brief 2019;25:104344,
     https://doi.org/10.1016/j.dib.2019.104344; the UCI deposit https://doi.org/10.24432/C5H31Z.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 488 respondents, body mass index regression without weight and height, fit `approximate`; issue 2 applies | the source states the habit-based aim; the rule for labels computed from the columns names this remedy; real signal and a spread of tuned methods[^1c] | a target we built; nobody needs the estimate where a scale is at hand; the signal is mostly age, sex and family history |
     | B | Retire | record `No (Retired)` + `No Good Target`, a CC line, the folder removed | no constructed task in the benchmark | the source's stated aim is set aside; a task with real signal and spread leaves |

   * **Recommendation:** A, since the source states the habit-based use and the rule for labels computed from the
     columns names this remedy; B if Andrej holds that no decision is made with such an estimate, as retiring needs
     the rule that a dataset serves a decision to fail[^1b]. **Decision:** keep (A), or retire (B)?

   **Notes for the AI:** on B, set the record to `No (Retired)` with `No Good Target`, add a
   `CC (<date>, Andrej):` line (a target we built; weight and height are asked in the same form), remove the folder,
   clear `v2_path`, and add a CHANGELOG entry; issue 2 then lapses.

   [^1a]: **SEL-5** (Must; narrows SEL-3): a label the source computes with a published, deterministic rule from the
     columns: drop the rule's inputs when the rest still makes a real task. Cases: account_debt_south_africa.
   [^1b]: **SEL-3** (Must): the dataset is published for a predictive task, simulating a decision someone makes with
     the prediction; a table without a genuine predictive target is out.
   [^1c]: **TP-3** (Must): if tuned methods spread, keep the dataset (a rule of an earlier part still wins).
   [^1d]: **TP-6** (Must): keep two questions apart, is the task valid and is it the best version; a valid task
     stays.

   **Andrej (2026-11-11, discuss):** Look at the source again, did they train the model for prediction or for scientific
   discovery to study how features like family history relate to obesity?

   **Answer (AI, 2026-11-11):** for prediction, but their predictor takes weight and height, so it never made the
   prediction we kept.
   - The companion paper (De-La-Hoz-Correa et al. 2019, J. Comput. Sci. 15:67-77,
     https://doi.org/10.3844/jcssp.2019.67.77) aims at "a software for prediction and detection of obesity levels in
     young people". It trains J48, Naive Bayes and logistic regression and ships a Weka tool, the "Information System
     for Detection of Obesity Levels in Youth".
   - That tool's input form asks for weight (kg) and height (m) next to the habits. Its 97.4% precision is the tree
     relearning the body mass index cut-offs, which is the leak we removed.
   - The data paper says the same: "tools to identify the obesity level of an individual" and "recommender systems that
     monitor obesity levels". Only one sentence points at discovery ("validate the impact of several factors").
   - So no source predicts the body mass index from habits without weight and height. That version is ours. The use
     case's claim that the source aims at habit-based tools was wrong, and issue 2's rewrite corrects it.
   - Scientific discovery is not the source's aim either. The habits-only reading is closest to it, though: what remains
     is how age, sex, family history and habits relate to the body mass index.

   | Evidence | What it says |
   |---|---|
   | Source tool's inputs | sex, age, **weight, height**, family history, habits |
   | Source tool's precision | 97.4% (label = rule on weight and height) |
   | Ours, habits and demographics only | TabPFN R² 0.18; age, sex and family history about 90% of the gain |

   | | Option | Fits |
   |---|---|---|
   | A | Keep | a habit-based screening nobody, the source included, has built |
   | B | Retire, `No Good Target` | the source's real task is circular; without weight and height only an invented target is left |

   - **Recommendation:** B now. The pro for keeping was the source's stated habit-based aim, and the source does not
     have it. **Decision:** keep (A) or retire (B)?

   **Andrej (2026-11-11, chat):** But the source actively aims for a predictive tool, not scientific discovery or
   insights about obesity?

   **Answer (AI, 2026-11-11):** yes. My point above that the habits-only reading is closest to discovery was wrong, and
   option B now carries `No Good Target` alone, without `Scientific Discovery`. The aim is still a tool whose task was
   circular.
   - Its motivation: web BMI calculators "are limited to the calculation of the body mass index, omitting relevant
     factors such as family background". So the authors wanted habits **added to** weight and height, not used **instead
     of** them.
   - Their label is the BMI class, though, so the added habits cannot change it. The tool only reproduces the BMI table
     (97.4%).
   - Dropping weight and height is the remedy the rule for labels computed from the columns offers when the rest still
     makes a real task. The source's aim does not show that the rest does: no one in it estimates a BMI without a scale.

   | Reading | Supports |
   |---|---|
   | Source wants a predictive obesity tool | the dataset is published for prediction (A) |
   | Its tool needs weight and height, and the label is their rule | the published task is circular |
   | Habits-only BMI: no source, no stated user | the kept task is one we built (B) |

   - **Recommendation:** still B, `No Good Target`. A is defensible if you read the source's predictive aim as enough
     for the repaired task. **Decision:** keep (A) or retire (B)?

   **Resolved (2026-11-11, Andrej):** B ("Agree." with the answer above, verdict dont): retired. The record is
   `No (Retired)` with `No Good Target / Scientific Discovery` (the vocabulary's only no-good-target marker for a
   finished case), priority removed, a CC line. The folder and `v2_path` stay until a retirement PR removes them; the
   claim stays.

2. **If it stays: say what carries the signal, and note the rounding and the minors?**

   * **Problem:**
     - `task_summary.question` reads "judged from eating habits and lifestyle alone", while age, sex and family
       history give about 90% of the gain over the mean (issue 1).
     - 40.8% of the reported weights are multiples of 5 kg, and 37 of the 488 respondents are under 18, for whom a
       body mass index is read against age-specific percentiles.
     - Rewrite the text to say both, or leave it?
   * **Effect on the task:** none on the data; a reader of the summary expects a habits task and does not learn that
     the target is self-reported and rounded.
   * **Experiments:** the 2026-11-04 check on the v0.2 rows confirms 40.8% of weights at multiples of 5 kg and 37
     respondents under 18.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave the text (implemented) | no change | none found | the summary oversells the habits; the self-reported, rounded target goes unmentioned |
     | B | Rewrite the text | `question` and `fit_reason` name the demographic answers; the rounding and the minors go into `curation_comments`; data unchanged | the summary says what the model predicts from[^2a]; the data stays as published | none found |

   * **Recommendation:** B: the data stays as published, and the text says what carries the signal and how the target
     was reported. **Decision:** leave the text (A), or rewrite it (B)?

   **Notes for the AI:** on B, `question` e.g. "What is a person's body mass index, judged from age, sex, family
   history and eating and activity habits?"; add to `fit_reason` that age, sex and family history carry about 90% of
   the gain over the mean; add a `curation_comments` bullet with the 40.8% of weights at multiples of 5 kg and the 37
   respondents under 18. Text only, no rebuild of the data needed.

   [^2a]: **USE-8** (Must): write how closely the data mirrors the use case; an approximate fit names its known gap.

   **Andrej (2026-11-11, change):** Option B: Rewrite the text.

   **Resolved (2026-11-11, Andrej):** B: the question names age, sex and family history and the habits; `fit_reason`
   says age, sex and family history carry about 90% of the gain over the mean; a `curation_comments` bullet notes 40.8%
   of weights at multiples of 5 kg and the 37 respondents under 18. The use case no longer says the source's tool works
   from habits alone (issue 1's answer). Text only, data unchanged.

3. **Time basis: if kept, name the random split a `Snapshot` of the 30-day survey?**

   * **Problem:**
     - Every row is one answer to a web survey open for 30 days, and the body mass index comes from the weight and height given in the same form as the habits, so the target exists with the features at one moment.
     - The record's collection fact fits (`Samples: One Moment`, no target tag), and the random split carries no time basis.
     - Name it a `Snapshot`, though the use case screens people after the survey?
   * **Background:** a release of one moment gets `Snapshot` or `DelayedTarget`, never the forced tag, and with the
     target of the same moment that is `Snapshot`[^3t1]. Its question, does the use case only fill in the moment the
     data covers, fits awkwardly: a screening tool is used on people later, so the line has to say that a later
     population is not tested. A relation of habits to body mass index that a month does not move is the
     `StationaryRelation` reading, but that prototype is for rows that arrive over a period and is measured on dated
     data, which this survey has not. Whether the task stays is issue 1.
   * **Effect on the task:** none on rows, splits or scores.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random, no time basis (implemented) | as now | none found | the score's time meaning is not stated; `dataset check` notes the missing basis |
     | B | Random, named `Snapshot` | `data_tags` gain `Snapshot`; a `Time basis:` line names the survey and what is not tested | the prototype the rules give a release of one moment with a target of that moment | the use case screens people later, not the survey's own respondents |
     | C | Random, named `StationaryRelation` | the line argues from the source that the relation does not move | names the forward use | the prototype is for rows over a period and is measured where dated; nothing here to measure |

   * **Recommendation:** B, if issue 1 keeps the dataset. **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("Snapshot",)` (no tag is listed now) and the curation
   bullet "- Time basis: Snapshot: one web survey open for 30 days (dates not stated; published 2019) in Mexico, Peru
   and Colombia; sex, age, family history, habits, weight and height reported in the same form, so the body mass
   index is of the same moment. Not tested: respondents of a later time or another population."; `dataset check`.
   The record's facts stay.

   [^3t1]: **SPLIT-8** (Must; reworded 2026-11-05): a release that is one moment (one extract, one stock month, one
     exam round) is not forced; SPLIT-32 gives it `Snapshot` or `DelayedTarget`. **SPLIT-32** (Should): a `Snapshot`
     only fills in a time the data covers; a `StationaryRelation` is a present state read through a relation that time
     does not move, for samples that arrive over time, measured on a dated source and argued from the source where
     time is lost.

   **Andrej (2026-11-11, change):** Option B: Random, named Snapshot.

   **Resolved (2026-11-11, Andrej):** B: the `Time basis: Snapshot` line is in `curation_comments` (one 30-day web
   survey; not tested: respondents of a later time or another population). The `Snapshot` tag enters `data_tags` once PR
   #50 is in the working copy. The record's facts stay.

   **Resolved (2026-11-11, Andrej):** the time-basis tags are in this working copy, so `data_tags =
   ("Snapshot",)` is set in the definition; the text changes of issue 2 are applied here too (they were not in this
   lineage's definition). `dataset check`: 0 errors, 0 warnings.

## Reference

@article{palechor2019dataset,
  title={Dataset for estimation of obesity levels based on eating habits and physical condition in individuals from Colombia, Peru and Mexico},
  author={Palechor, Fabio Mendoza and De la Hoz Manotas, Alexis},
  journal={Data in brief},
  volume={25},
  pages={104344},
  year={2019},
  publisher={Elsevier}
}
