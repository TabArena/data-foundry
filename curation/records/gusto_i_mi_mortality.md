---
unique_name: gusto_i_mi_mortality
name: GUSTO-I trial patient data (30-day mortality after acute myocardial infarction) / gusto (hbiostat.org/data; R package predtools)
checked_by:
- AI (UNVERIFIED)
- Andrej
suggestion: 'Yes'
priority: 4
decision_markers:
- Outdated
- Class-dependent Recording
tags:
- AI-Filled (Verify)
- 'Samples: Over Time'
- 'Time: Lost'
- 'Target: Fixed Delay'
- Clinical Study
original_source: Website
year: '? (1995)'
collection_period: 1990-1993
domain: medical & healthcare
problem_type: Binary Classification
original_data_state: One Table
source_links:
- https://doi.org/10.1161/01.cir.91.6.1659
- https://cran.r-project.org/package=predtools
- https://github.com/resplab/predtools/blob/master/R/gusto.R
- https://hbiostat.org/data/repo/gusto.rda
- https://hbiostat.org/data/
- https://doi.org/10.1056/NEJM199309023291001
- https://pmc.ncbi.nlm.nih.gov/articles/PMC4155437/
v2_path: datasets/_dev/tabarena-v0pt2/gusto_i_mi_mortality/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers (and, where the block says so, a preview of the files), NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 4: the GUSTO-I trial's 40,830 patients with acute MI (15 countries, 1990-1993), death by day 30 from the data at presentation, a decision the source names (therapy and resources), an open release with a permission text; its one weakness is that methods do not separate on it (logistic regression = LightGBM), a `no_spread` question for the curator, not a reject. Deep pass; the measured numbers come from the hbiostat file (downloaded 2026-11-11, md5 de877ace...) and the 2026-11-25 baselines of `mic`'s better-data item.
- Source: the trial: GUSTO investigators, "An international randomized trial comparing four thrombolytic strategies for acute myocardial infarction", N Engl J Med 1993;329:673-682 (https://doi.org/10.1056/NEJM199309023291001): "In 15 countries and 1081 hospitals, 41,021 patients with evolving myocardial infarction were randomly assigned to four different thrombolytic strategies ... The primary end point was 30-day mortality" (abstract). The prediction model: Lee et al., Circulation 1995;91:1659-1668 (https://doi.org/10.1161/01.cir.91.6.1659). The patient file as released: `gusto.rda` on the Vanderbilt Department of Biostatistics repository (https://hbiostat.org/data/repo/gusto.rda; served, not listed in the index of https://hbiostat.org/data, whose text says "Permission is granted to anyone wishing to use the data sets provided here. Please reference the original paper ..."); the R package predtools ships the same 40,830 x 29 table with "@source Internet". As published (measured): 40,830 patients x 29 columns, one row per patient, 2,851 deaths by day 30 (7.0%), 4 duplicate rows, no blanks except `tpa` (10,320, exactly the SK+tPA arm; `tx` holds the arm: SK 20,162 (both streptokinase arms merged), tPA 10,348, SK+tPA 10,320, death 7.3%, 6.3% and 7.0% as in the NEJM abstract). 191 of the 41,021 enrolled are not in the file (unexplained; Steyerberg's case study uses the same 40,830). Steyerberg and Vergouwe 2014 (Eur Heart J, https://pmc.ncbi.nlm.nih.gov/articles/PMC4155437/) say missing predictor values of this cohort were filled "with a single imputation procedure", so the file's complete columns are partly imputed.
- Use case: the cardiologist at initial presentation of an acute MI estimates the risk of death; Lee et al. name the decision: "Appropriate choices among alternative therapies and the use of clinical resources depend on an estimate of the patient's risk" (abstract, Background), from "clinical descriptors routinely collected at initial presentation" (Methods); fit direct for the moment and the inputs (`tx` is the randomised arm, known at admission), approximate for today's care (primary PCI replaced thrombolysis as the first choice: an `Outdated` note under SEL-18, the task itself is still made today). Collection: `Samples: Over Time` (each patient enrolled at their own admission, 1990-1993), `Time: Lost` (no date or enrolment order in the file; the rows are sorted by age), `Target: Fixed Delay` (day 30 after enrolment); entities do not recur. Type `Clinical Study` (a randomised trial's patients with their dates lost, SPLIT-34).
- Split: leaf L-PLACE.groups (Grouped, `UnseenGroup` by groups) because the use case meets patients of other hospitals (CLI.meets: another site) and the file holds three nested place codes (`regl` 16 regions of 1,231-4,352 patients and 95-294 deaths each, `grpl` 48, `grps` 121 site groups; PLACE.several: yes); open: what the codes are (no codebook; Steyerberg's external validation splits US 23,034 / non-US 17,796, which `regl` codes would give it), and whether the curator reads the use case as later patients at the same hospital (then the order step, with no order to rebuild). Measured: grouping by `grps` changes no score (LR all features 0.826 random and grouped).
- Siblings and duplicates: `mic` (`Yes`, 1,700 Krasnoyarsk patients 1992-1995, 8-class lethal outcome; another source, so its own record, PROV-4; its better-data item of 2026-11-25 recommends adding this record next to it, not instead of it); `crash2_trauma_early_death` (another trial on hbiostat, a different task, same precedent for a trial as a clinical study); `smart_vascular_events` (another Steyerberg case study, different task). No other GUSTO record (grep gusto, predtools, hbiostat). External collections: hbiostat.org, predtools; the mice-ext-val package ships a 2,188-patient region subset with values removed (not the full file).
- Better data: found as better data for `mic`. Nothing better for this task found: the 2026-11-11 search for `mic` (MIMIC-IV and eICU AMI cohorts: credentialed, no redistribution; WHAS500, Vellore NSTEMI, Alkmaar and national registries: smaller, unreleased or on application) ; no new search today (no scout runs for a scouting hit), and the open patient-level files of thrombolysis or PCI trials known to us are smaller or not open.
- Papers and pages: GUSTO 1993 NEJM (trial); Lee et al. 1995 (model: logistic regression, "validated with bootstrapping techniques"; "these five characteristics contained 90% of the prognostic information in the baseline clinical data"; abstract read on Europe PMC, full text not reachable, publisher 403); Steyerberg and Vergouwe 2014 (case study on this file: c statistic 0.813 internal, 0.812 at US-to-non-US validation for the full model, 0.75 for age alone); Steyerberg, Clinical Prediction Models, chapter 22 page (subsamples only).
- Metric: Lee et al. report chi-square per predictor and "accurately estimated the likelihood of death" (abstract; whether the full text gives a c index is unchecked); Steyerberg and Vergouwe score this file by the c statistic and calibration: one of several, so `roc_auc` (the c statistic, the field's measure of discrimination) with log loss as the calibration-aware alternative (MET-5, MET-8); inputs none.
- Risks for /add-dataset: no method spread (measured, 5-fold x 3, random and grouped by `grps`: ROC AUC LR five predictors 0.810, LR all 0.826, LightGBM all 0.826 to 0.827, LR all with splines 0.830 and best on 15 of 15 folds; log loss 0.1996 LR, 0.2010 LightGBM, 0.1985 splines): untuned, so a `no_spread` flag for tuned methods (TP-1); no rule rejects for it (TP-3 keeps on spread, it does not drop for none), and a large, low-noise task where strong methods converge is the amex pattern; it lowers the dataset's value for ranking methods, the curator's weighing. Trivial (TP-4 step 1) ruled out for a published score not fitted on these data: the TIMI risk score for STEMI (Morrow 2000; age, diabetes/hypertension/angina, SBP < 100, HR > 100, Killip II-IV, weight < 67 kg, anterior site; time to treatment left out as `ttr`'s meaning is unknown) scores ROC AUC 0.794 on the whole file against 0.826 for the methods; Lee et al.'s own model is fitted on these data, so it is no TP-4 rule. Derived flags of the Lee/Steyerberg model next to their sources (measured: `sho` = Killip III or IV, `hyp` = systolic BP < 100 (5 exceptions), `hrt` = pulse > 80 (8 exceptions), `hig` = anterior site or previous MI, `ant` = `miloc` Anterior): redundant, drop or keep one form; `ttr` (yes for 26,494) is undocumented (time to treatment or to relief?), check before keeping (it may be after presentation, USE-3). `tpa` blank by arm: drop, keep `tx`. 4 duplicate rows (LEAK-19 check). The single imputation of missing predictors by the case-study authors (the file cannot show which values were imputed). Thrombolysis-era cohort (`Outdated`, SEL-18, a note). Age 19 to 110 (check the top).
- Priority: gap 0 (medical, binary and grouped are not thin), use case + (the source names the decision and the moment, fit direct), source + (trial and model papers in NEJM and Circulation, a university repository with a permission text), shape + (40,830 patients, 28 mixed inputs, 16 regions); risk 0: no leak, join or unclear target, and no better data for the task; the missing spread and the `Outdated` question are no factor of the table, so they take no point, but they are the first things to weigh.
- Corrected from the screening of 2026-10-31: use case 0 -> + (the abstract names the decision); metric "none found" -> the c statistic of the case study; the arm is in the file (`tx`, three levels, the SK arms merged); deaths 2,851 measured (not about 2,860); regime IID -> grouped by place (leaf above); the derived flags mapped; the hbiostat release, its permission text and the NEJM trial paper added to source_links; priority 3 -> 4.

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 3: patient data of the GUSTO-I trial (40,830 patients with acute MI, enrolled 1990-1993) with death by day 30 and the admission predictors of the published Lee et al. model; a large, real clinical prediction task, with an unclear release path of the patient file (predtools gives "Internet" as its source).
- Source: the GUSTO-I trial and its 30-day mortality model: Lee, Woodlief, Topol, Weaver, Betriu, Col, Simoons, Aylward, Van de Werf, Califf, "Predictors of 30-day mortality in the era of reperfusion for acute myocardial infarction. Results from an international trial of 41,021 patients", Circulation 91(6):1659-1668 (1995, https://doi.org/10.1161/01.cir.91.6.1659). The patient file ships in the R package predtools (resplab, UBC; https://cran.r-project.org/package=predtools): "Anonymized data from the gusto trial", "A data frame with 40830 rows and 29 variables", documenting only `day30`, `sho`, `hig`, `dia` and `hrt`, with "@source Internet" (https://github.com/resplab/predtools/blob/master/R/gusto.R).
- Use case: at admission for an acute MI the cardiologist estimates the risk of death from age, systolic blood pressure, Killip class, heart rate and infarct location (together "about 90% of the prognostic information" in the abstract) and history; the paper's model "accurately estimated the likelihood of death" and names no decision; fit direct for a risk estimate at admission, though care has moved from thrombolysis to primary PCI since (`Outdated` to weigh); regime IID (a trial cohort of 15 countries; region could group).
- Siblings and duplicates: `mic` (`Yes`, 1,700 Krasnoyarsk patients with complications and the lethal outcome: the same quantity among others, another source, PROV-4); `smart_vascular_events` (another Steyerberg case-study cohort, a different task). No other GUSTO record (searched gusto, predtools, clinicalpredictionmodels). External collections: none known.
- Better data: no new search; found as better data for `mic`.
- Papers and pages: Lee et al. 1995 (abstract read on Europe PMC); Steyerberg, Clinical Prediction Models, the chapter 22 page (https://www.clinicalpredictionmodels.org/extra-material/chapter-22, moved here from source_links as related work, PROV-12: "The GUSTO-I trial provided data for a prediction model developed by Kerry Lee et al at Duke Clinical Research Institute"; it offers the subsamples sample2, sample4 and sample5, not the full file); the predtools documentation.
- Metric: none found as one criterion (the abstract reports chi-square statistics per predictor and no c-index; the full text not read); fallback `roc_auc` (MET-5, MET-8). Inputs: none.
- Risks for /add-dataset: the file's provenance (PROV-2: who released the patient-level data, Duke or the Steyerberg book, is unconfirmed; 40,830 rows against 41,021 enrolled needs a note); 24 of the 29 columns are undocumented in predtools (map them to the paper's predictors); the thrombolytic arm, if the file holds it, is randomised and known at admission; 30-day death about 7%, so about 2,860 deaths.
- Priority: gap 0 (medical, binary and IID are not thin), use case 0 (the paper names the estimate, not the decision), source + (Circulation paper of a documented trial), shape + (40,830 patients, mixed types), risk 0 (the file's release path is a PROV-2 note, not a leak or an unclear target).

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `mic`.
- as published: 40,830 patients, 29 variables (predtools documentation); trial enrolment 1990-1993 in 15 countries; target: day30: death within 30 days (binary); access: open.
- Why: The same quantity as mic's lethal outcome (death after an MI, predicted from admission data: history, examination, ECG location), with features of the same kind.
- Adds: 24 times the patients (40,830 against 1,700) from many countries instead of one Krasnoyarsk hospital. Not newer (1990-1993 against 1992-1995), binary death instead of mic's cause of death and complications. Provenance caveat (PROV-2): the trial is well traced, but predtools gives the file's source as 'Internet'; who ...

**Assessment (AI, 2026-11-25):** corrected from today's screening: `ttr` is not undocumented. The R file's variable labels, which pyreadr drops, call it "Time to Relief of Chest Pain > 1h"; the randomised arm changes it (66.3% under streptokinase, 64.6% under the combination, 62.3% under accelerated tPA, p = 3e-11, while every baseline column is balanced), so it is recorded after treatment and dropped. Also corrected: "no leak" under risk no longer holds as screened, since the heights the source's single imputation filled in mark patients who died (adjusted odds ratio 2.65, 15 of 16 regions), so `height` is dropped; and the five derived flags are recodes, not copies, so they stay as released.

**Assessment (AI, 2026-11-25):** review panel (full): ship after changes; disputed: SPLIT-33 (3 repeats of 3 folds or 8 folds over the 16 regions), MET-8 and MET-11 (`roc_auc` or `log_loss`), PROV-4 (next to `mic` or in its place), CLEAN-11 (the ages 108 to 110); for the curator: issues 1-4. Applied: `height` dropped (LEAK-10 through LEAK-38), the five flags kept (CLEAN-22), 7 impossible pulse and pressure values set to missing, `groups_test_groups_few` accepted with its reason, wording; markers `Outdated` and `Class-dependent Recording` added for the curator to confirm. Priority 4: gap 0, use case +, source +, shape +, risk 0 (the leak is fixed and the open calls are protocol and metric choices; the small spread between methods is weighed, not a factor).

CC (2026-11-25, Andrej): review issue 1, B: "Option B: 1 round of 8 folds." Whole regions in one round of 8-fold grouped cross-validation, two of the 16 regions per test fold, each region tested once (the layout of economic_well_being_prediction_challenge); `splits_dimensions_off_protocol` and `groups_test_groups_few` accepted with their reasons.

CC (2026-11-25, Andrej): review issue 4, A (ok, as implemented): the ages 108, 108 and 110 stay as recorded, with the note.

**Assessment (AI, 2026-11-25):** marks applied. Issue 1: `_make_splits` builds 1 x 8 region folds (2 regions each), test folds of 4,161 to 7,789 patients and 256 to 554 deaths; check 0 errors, 0 warnings (2 accepted), 3 info; group probe ROC AUC 0.824 (logistic regression), 0.814 (random forest), 0.821 (LightGBM) on held-out regions, LightGBM 0.821 grouped against 0.819 random; task probe no flag. Issue 3 (discuss) answered in the review and left open: Steyerberg and Vergouwe 2014 compare an age-only model with a four-predictor model fitted on 259 or 23,034 US patients, on the 17,796 non-US patients, by calibration-in-the-large, calibration slope, c statistic and net benefit, and say the c statistic "is insensitive to systematic errors in calibration"; on the 8 folds log loss separates splines from logistic regression on 7 of 8 folds as ROC AUC does; log loss from context recommended.

**Assessment (AI, 2026-11-25):** Andrej's second question on issue 3 (discuss, the heart_disease precedent) answered in the review and left open. Detrano et al. 1989 scored reliability (mean predicted against observed, overall and by quintiles) and the percent correctly classified over thresholds 0.2 to 0.8, with no ROC analysis; heart_disease's `roc_auc` is the binary fallback, and its own reason says ROC AUC does not score reliability. On heart_disease's three held-out hospitals logistic regression is third of four models by ROC AUC (0.824) but last by log loss (0.711) and Brier (0.209), since it misjudges each hospital's disease rate. Recommended: log loss for GUSTO-I now; heart_disease's metric raised as a separate decision (not changed here).

CC (2026-11-25, Andrej): review issue 3, b: "Reply (b): Log loss for both, decided together". The metric is log loss for GUSTO-I and for heart_disease, one reading of the metric rules for two sources that score calibration.
- **Why not ROC AUC:** the case study on this file scores calibration next to the c statistic (ROC AUC) and says "the c statistic is insensitive to systematic errors in calibration"; the choice of clot-dissolving drug acts on the absolute risk, and the regions' death rates run from 5.3% to 8.4%.
- **Original named:** the case study's c statistic (0.813 internal, 0.812 US to non-US) stays in the metric reason as the original; log loss is declared from context.
- **heart_disease:** moved to log loss in the same round (its source, Detrano et al. 1989, scored reliability and accuracy over thresholds, never ROC AUC).

CC (2026-11-25, Andrej): the declared metric (log loss, from context; the case study's c statistic named as the original) is checked: the source scores calibration next to the c statistic and argues the c statistic misses it, the treatment decision acts on the absolute risk, and log loss separates a logistic regression with splines from a plain one on 7 of 8 region folds, as ROC AUC does.

CC (2026-11-26, Andrej): the declared split (whole regions in one round of 8-fold grouped cross-validation, two of the 16 regions per test fold) is checked, as implemented.

CC (2026-11-26, Andrej): verdict ship. Open in the review: issue 2, whether the dataset joins next to `mic` or takes its place (one call with `mic`'s issue 5); the verdict leaves out only issue 2's option C. The build is stale until rebuilt. Issue 2 was decided the same day (B, in place of `mic`; CC line below), so nothing stays open in the review.

CC (2026-11-26, Andrej): review issue 2, B: "Option B: In place of mic." This dataset ships in `mic`'s place: one heart-attack death task, the GUSTO-I trial's 40,826 patients from 15 countries, against mic's 1,700 Krasnoyarsk patients whose blank fields follow the outcome. `mic` is retired the same day (`No (Retired)`, `Class-dependent Recording`, its issues 5, C, and 6, A), and its multiclass outcome (causes of death and complications) leaves the benchmark. The suggestion stays `Yes` (verdict ship).

**Assessment (AI, 2026-11-25):** issue 3 (b) applied. `dataset.py`: `Metric.from_context("log_loss", ...)` replaces the roc_auc fallback; the reason quotes the case study's sentence on the c statistic, names the c statistic as the original, and gives the absolute-risk decision and the regions' death rates (5.3% to 8.4%); the probe note gives the log-loss figures. Check: 0 errors, 0 warnings (2 accepted), 3 info; metric `log_loss` (origin context). Task probe on the 8 region folds, log loss: linear 0.2006, random forest 0.2039, LightGBM 0.2044, age alone 0.2322, class shares 0.2547 (linear beats the class shares on every split, by 21.2% of their loss); no flag. heart_disease changed in the same round (its own record).

## Review

**Outcome:** added; the curator's verdict is ship (2026-11-26), in place of `mic` (issue 2, B), nothing open. The GUSTO-I trial's 40,826 patients with an ST-elevation heart attack, death by day 30 from what is known at presentation, held out by whole region (16 regions, two per test fold in one round of 8 folds, Andrej 2026-11-25); the review panel recommends shipping after changes, which are applied; the three ages of 108 to 110 stay with a note, and the task is scored by log loss (Andrej). Judgment record:

```text
Verdict: ship after changes (applied).
Validity: open permission text; the use case is real and the fit direct (the thrombolysis era is an `Outdated`
  note; the source's time to treatment is not in the file, noted). `ttr` ("Time to Relief of Chest Pain > 1h" in the
  R file's labels) is the one column the randomised arm changes (p = 3e-11, every other p >= 0.087): recorded after
  treatment, dropped. `height`: its filled-in values mark patients who died (adjusted odds ratio 2.65, 15 of 16
  regions); setting them to missing or rounding them keeps the signal: dropped. 4 exact copies dropped, the 28-row
  fill pattern kept with a note. Split: whole regions, leaf L-PLACE.groups, 1 x 8 folds of 2 regions; the regions
  rebuild the source's US and non-US cohorts exactly; grouped and random folds score alike.
Value: tuned methods separate (+0.003 to +0.004 ROC AUC over a plain logistic regression, 7 of 8 region
  folds; by log loss, the declared metric, 0.1997 and 0.1996 against 0.2008); the untuned task probe on the
  shipped inputs raises no flag; not Trivial (the TIMI score, not fitted on these data, 0.794 against about
  0.827 ROC AUC).
Quality: the five flags of the source's simplified models kept as released (none is an exact copy); 7 impossible
  pulse and pressure values set to missing.
Weighed: size +, source +, era -, small spread -.
Decided: issue 1 (1 x 8 folds), issue 3 (log loss, from context, with heart_disease), issue 4 (ages kept),
  issue 2 (in place of mic, which is retired). Verdict ship (2026-11-26). Nothing open.
```

**Main points:** Andrej chose one round of 8 folds of 2 regions (issue 1) and kept the three ages of 108 to 110 with a note (issue 4), and chose log loss from context for this dataset and heart_disease together (issue 3: the source scores calibration next to the c statistic and argues the c statistic misses it; heart_disease's source scored calibration and accuracy, never ROC AUC). Verdict ship and the split checked (2026-11-26). It ships in place of `mic` (issue 2, B, 2026-11-26), which is retired the same day with `Class-dependent Recording`; nothing stays open. Applied without a decision: `height` dropped (its fills leak the outcome), the five flags kept as released (the builder had dropped them), impossible pulse and pressure values set to missing, `groups_test_groups_few` accepted with its reason, and the wording of the use case, fit and split. The record now carries `Outdated` and `Class-dependent Recording` (the height fills), both for the curator to confirm.

**Issues for the curator:**

1. **Hold out the 16 regions in 3 repeats of 3 folds, or in 8 folds of 2 regions each?**

   * **Problem:**
     - The shipped 3 repeats of 3 folds shrink the gap between tuned LightGBM and logistic regression by 0.001 against holding out each region alone, while 8 folds of 2 regions keep it.
     - The 3 by 3 layout is the default grouped protocol, with 5 or 6 regions per test fold, and accepts the warning that a test fold holds few groups[^1a].
     - For economic_well_being_prediction_challenge (25 countries) the curator chose one round of 9 folds over 3 by 3, because 3 by 3 trained on fewer groups and shrank the gaps between methods[^1b].
   * **Background:** the 16 regions hold 1,231 to 4,352 patients and 95 to 294 deaths each and are alike (death rates 5.3% to 8.4%); grouped and random folds score the same. Folds of 5 or 6 regions train on 10 or 11 regions, folds of 2 regions on 14.
   * **Experiments:** with `height` dropped, 6 draws of each design, mean ROC AUC over the folds; the reference holds out each region alone. The SD is that of the design's mean score over the draws.

     | Design | Logistic regression | Logistic regression with splines | LightGBM, lightly tuned | Gap LightGBM - logistic regression | SD over draws (LightGBM) |
     |---|---|---|---|---|---|
     | Each region alone, 16 folds (reference) | 0.8189 | 0.8248 | 0.8256 | 0.0067 | 0 |
     | 1 round of 8 folds, 2 regions each | 0.8202 | 0.8263 | 0.8269 | 0.0067 | 0.0010 |
     | 3 rounds of 3 folds (implemented) | 0.8208 | 0.8266 | 0.8264 | 0.0056 | 0.0003 |

   * **Consistency:** sat11_hand_algo_runtime (32 families) and huesken_sirna_efficacy (30 genes) were accepted at 3 by 3; economic_well_being_prediction_challenge (25 countries) went to one round of 9 folds on a measurement like the one above. With 16 groups this dataset sits nearer the latter.
   * **Panel:** the advocate argues for 3 by 3 (the protocol default, stable test folds of 793 to 1,119 deaths); the critic for 8 folds, after the economic_well_being reasoning; the mediator leans to 8 folds, weakly. 3 by 3 is no farther from the reference in level here, because the regions are large and alike; it swaps the order of the two best models by 0.0002, within noise.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 3 rounds of 3 folds (implemented) | 5 or 6 whole regions per test fold, every region tested three times | the protocol default, no departure to accept; the steadiest score (SD 0.0003); test folds of 11,215 to 15,610 patients | trains on 10 or 11 of 16 regions; shrinks the LightGBM gap by 0.001 against the reference; the repeats share most of their training regions |
     | B | 1 round of 8 folds | 2 whole regions per test fold, each region tested once | the reference's gap and model order; trains on 14 regions; follows the economic_well_being call | a protocol departure to accept; a noisier mean score (SD 0.0010); test folds of about 190 to 590 deaths, two regions' counts |
     | C | Each region alone, 16 folds | one region per test fold | the reference itself | the noisiest folds (95 to 294 deaths each); the same departure as B, with twice the fitting |

   * **Recommendation:** B, weakly: it keeps the method gap the reference shows, which matters on a task whose methods differ by 0.006, and follows the curator's reasoning for economic_well_being; A is defensible if the stability of the large, alike regions counts as the fact that sets this case apart. **Decision:** 3 rounds of 3 folds (A), 8 folds of 2 regions (B), or each region alone (C)?

   **Notes for the AI:** on B, set the grouped splits to 1 repeat of 8 folds in `dataset.py` (the definition's split settings, as in economic_well_being_prediction_challenge), accept `splits_dimensions_off_protocol` with the table above as the reason, reword the `groups_test_groups_few` reason (2 regions per test fold, with the measured patient and death counts per fold) and the splits comment, and add a row to "Definitions that ship another split" in split_tree.md (leaf L-PLACE.groups, the shipped layout, the reviewer, the date, the reason). On C the same with 16 folds. Re-run `dataset check` and the group probe.

   [^1a]: **SPLIT-33** (Should): an IID or grouped task gets repeated 3-fold cross-validation, with 20, 10, 3 or 1 repeats as its train side holds fewer than 500, 2,500 or 250,000 units, or more. The warning `groups_test_groups_few` is accepted with the group probe's reason (the house rule on check warnings).
   [^1b]: economic_well_being_prediction_challenge (Andrej, 2026-11-24 and 2026-11-25): one round of 9 folds over 25 countries, chosen over 3 by 3 because 3 by 3 "trains on a third fewer countries, so it sits about twice as far from the reference", shrank the gap between the two best models and its repeats "share most of their training countries".

   **Andrej (2026-11-25, change):** "Option B: 1 round of 8 folds."

   **Resolved (2026-11-25, Andrej):** B: one round of 8-fold grouped cross-validation over the 16 regions, two whole regions per test fold, each region tested once, stratified by the outcome with the framework's fixed seed; each split trains on 14 regions. `dataset.py` builds the folds in `_make_splits` (and asserts 2 regions per fold, 16 in all), accepts `splits_dimensions_off_protocol` with the table above as the reason, rewords the `groups_test_groups_few` reason and the splits comment, and updates the task summary's split, the grouping definition and the figures measured on the earlier folds. The test folds hold 4,161 to 7,789 patients and 256 to 554 deaths. Check: 0 errors, 0 warnings (2 accepted), 3 info. Group probe on the new folds: ROC AUC 0.824 (logistic regression), 0.814 (random forest), 0.821 (LightGBM) on held-out regions; LightGBM 0.821 grouped against 0.819 random. Task probe: no flag (linear 0.829, random forest 0.823, LightGBM 0.823, age alone 0.733). The same layout as economic_well_being_prediction_challenge (whole countries in 9 folds, one repeat).

2. **Ship next to `mic`, or in its place?**

   * **Problem:**
     - This dataset was found as better data for `mic`, and `mic`'s issue 5 still asks whether GUSTO-I joins next to `mic` (its option B) or replaces it (its option C).
     - Both options add this dataset, so its folder and review stand either way; they differ on whether `mic` stays, which `mic`'s issue 6 also bears on.
     - This record has no CC line yet, and its `suggestion` is still the screening's `TBD -> Yes`.
   * **Background:** `mic` holds 1,700 Krasnoyarsk patients (1992-1995) with a multiclass outcome (the cause of death and complications) that only it has; GUSTO-I is the clean, 24 times larger binary death task from 15 countries. The two are different sources, so each has its own record[^2a].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Next to `mic` (implemented) | this dataset ships; `mic` stays or goes on its own merits (its issue 6) | keeps `mic`'s multiclass outcome; the large, open death task joins | two heart-attack death tasks if `mic` stays |
     | B | In place of `mic` | this dataset ships; `mic` is retired through its issues 5 and 6 | one heart-attack death task, the clean and large one | loses the only multiclass outcome of the two |
     | C | Leave it out | the folder is removed | none found | drops the largest open heart-attack death task the screening found |

   * **Recommendation:** A, as `mic`'s issue 5 recommends; whether `mic` stays is its issue 6's call. **Decision:** next to `mic` (A), in its place (B), or left out (C)?

   **Notes for the AI:** whatever is decided, record it in `mic`'s issue 5 as well (a `Resolved` turn there) and add the CC line to both records; on A or B set this record's `suggestion` to `Yes` with Andrej in `checked_by`; on B retire `mic` as its issue 5 option C says; on C remove the folder and set `No` with the reason.

   [^2a]: **PROV-4** (Must): a dataset enters once; two records that end at the same original source are duplicates. `mic` and GUSTO-I end at different sources.

   **Andrej (2026-11-26, change):** Option B: In place of mic.

   **Resolved (2026-11-26, Andrej):** B: this dataset ships in `mic`'s place (`suggestion` `Yes`, verdict ship); `mic` is retired through its issues 5 (C) and 6 (A), `No (Retired)` with `Class-dependent Recording`, its folder removed. The CC line is in both records. This folder is unchanged.

3. **Score by ROC AUC or by log loss?**

   * **Problem:**
     - The case study on this file scores its models by the c statistic together with calibration in the large and the calibration slope, so the source has no single metric and the definition declares the binary fallback, ROC AUC[^3a].
     - The clinician acts on the absolute risk (the benefit of the stronger thrombolytic scales with it), and the regions' death rates run from 5.3% to 8.4%, which ROC AUC does not see.
     - heart_disease, a source that also scores calibration next to another measure, went to ROC AUC, so log loss needs a fact that sets this case apart[^3b].
   * **Background:** the rule on probabilities names ROC AUC as the binary fallback; its clause on calibration contrasts probabilities with a hard-label accuracy, not ROC AUC with log loss. Log loss would be a metric chosen for this task's context, with the reason named in the notes[^3c].
   * **Experiments:** with `height` and the five flags dropped, on the 9 folds by region; "better" counts the folds on which the model beats a plain logistic regression.

     | Model | ROC AUC | Better on | Log loss | Better on |
     |---|---|---|---|---|
     | Logistic regression | 0.8202 | - | 0.2023 | - |
     | Logistic regression with splines | 0.8262 | 9 of 9 | 0.2002 | 9 of 9 |
     | LightGBM, lightly tuned | 0.8262 | 9 of 9 | 0.2006 | 9 of 9 |
     | LightGBM, defaults | 0.8187 | 1 of 9 | 0.2045 | 0 of 9 |

   * **Effect on the task:** both metrics separate the methods on 9 of 9 folds, so neither is chosen for resolution; the choice is between consistency with the precedent and scoring the risk level the decision acts on.
   * **Panel:** the critic and the domain practitioner ask for log loss (fidelity to the source's calibration and to the decision); the advocate holds ROC AUC by precedent and would not oppose log loss; the mediator finds that the rule does not require log loss, so ROC AUC holds by default.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | ROC AUC (implemented) | the fallback, the c statistic the case study reports (0.813 internal, 0.812 US to non-US) | follows heart_disease and gallstone_disease; comparable with the published c statistics | blind to whether a model carries the risk level to an unseen region |
     | B | Log loss | a strictly proper rule on the predicted risk, with the absolute-risk fact recorded as the reason | scores the calibration the source weighs and the decision runs on | a departure from heart_disease that rests on a fact a curator must accept; no published log loss to compare with |

   * **Recommendation:** A, by the rule's default and the heart_disease precedent; B if the curator takes the absolute-risk decision and the regional spread of death rates as the fact that sets this case apart. **Decision:** ROC AUC (A) or log loss (B)?

   **Notes for the AI:** on B, declare `Metric.context("log_loss", ...)` (the context origin) with the reason: the source scores calibration next to the c statistic, the thrombolytic choice acts on the absolute risk, and the regions' death rates run from 5.3% to 8.4%; name ROC AUC as the original measure the case study reports; re-run `dataset check` and the task probe.

   [^3a]: **MET-5** (Should): a paper's metric is the source's only when it is one deliberate choice; a paper that reports several side by side has no unique original, and the fallback is declared. **MET-8** (Should): with no unique metric, score classification by a strictly proper scoring rule or a ranking metric, the fallback, `roc_auc` for binary tasks.
   [^3b]: heart_disease (Lennart, 2026-10-21): `roc_auc`, not `log_loss`, for a source that scores calibration next to another measure; gallstone_disease (Lennart, 2026-10-21): papers that report several metrics go to the fallback.
   [^3c]: **MET-11** (Must): every metric has one origin, and the notes name the original whenever the declared metric is not exactly it. **MET-10** (Weigh): the factors on a borderline call between the source's metric and the fallback, among them the resolution on our folds.

   **Andrej (2026-11-25, discuss):** "Why don't we use the same metric as the domain practitioner? Give more details on what the source compared exactly?"

   **Answer (AI, 2026-11-25):** the source scores four measures side by side and names none as deciding, so the rules give the fallback (ROC AUC); the domain practitioner's log loss is a metric chosen from the decision, which needs a fact that sets this case apart from heart_disease, and one exists: the source itself argues that the c statistic misses the calibration it scores.

   * **Problem:**
     - The case study on this file (Steyerberg and Vergouwe 2014) proposes "four key measures in the assessment of the validation of prediction models" (section "An ABCD for model validation") and reports all four for each model, without ranking or selecting by one; this is the several-metrics case, which goes to the fallback[^3d].
     - In the same paper it states why the c statistic alone is not enough: "We note that the c statistic is insensitive to systematic errors in calibration, and considers the rather artificial situation of classification in a pair of patients with and without the endpoint" (section "C, Concordance statistic: discrimination"). The heart_disease precedent rests on Detrano 1989's calibration next to the percent correctly classified over thresholds 0.2 to 0.8, as the metric rules record it, with no argument against a ranking measure on record. This is the fact that could set the case apart[^3e].
     - The domain practitioner would choose log loss (Brier as the more readable alternative) because the thrombolytic choice acts on the absolute risk, and the absolute benefit of the stronger drug scales with the baseline risk; the regions' death rates run from 5.3% to 8.4%. The panel's mediator held ROC AUC because the rules require no context metric; that is why the definition did not follow the practitioner.
   * **What the source compared, exactly:**
     - Steyerberg and Vergouwe 2014, section "Case study": "We consider the development of prediction models in patients enrolled in the US (N= 23,034, 1,565 deaths, and a small subset with N=259, 20 deaths). We validate these models in patients enrolled outside of the US (N=17,796, 1,286 deaths). The first model only includes age as a continuous, linear term in a logistic regression analysis, while a slightly more complex model includes age, Killip class, systolic blood pressure and heart rate." Three logistic regressions in all: age only, and the four-predictor model fitted on 259 or on 23,034 US patients. The introduction states the aim: "We compare the performance of a simple model (including age only) to a more complex model (including age and other key predictors), which are developed either in a small or a large data set." No machine-learning model and no `tx`, `ttr` or other GUSTO-I predictor is in these models.
     - Every score is from the external validation on the 17,796 non-US patients, except where marked:

       | Model | A: calibration-in-the-large | B: calibration slope | C: c statistic | D: net benefit, threshold 2% |
       |---|---|---|---|---|
       | Age only | not reported | not reported | 0.75 | 0.04% |
       | Age, Killip, blood pressure, pulse; 259 US patients | not reported | 0.70 (internal shrinkage 0.82) | 0.80 [0.79-0.82] (apparent 0.82, internal 0.78) | 0.2% |
       | Age, Killip, blood pressure, pulse; 23,034 US patients | 0.07, p = 0.38 | 0.99, p = 0.55 | 0.812 [0.800-0.824] (internal 0.813) | 5.6% (treat all 5.3%); at 5%, 19 extra net true positives per 1,000 |

       Sources: sections "A, Alpha", "B, Beta", "C, Concordance statistic" and "D: Decision curve analysis", and Figures 1 and 2. The paper reports no Brier score, no R², no log likelihood or deviance as a performance score (a likelihood ratio test appears once, to choose the coding of infarct location, section "Seven steps", step 2) and gives no rule for combining A to D: "At model validation, calibration, discrimination and clinical usefulness should be considered" (section "Concluding remarks").
     - The net benefit is scored over a range of thresholds, not at one: "It is therefore advised to consider a range of thresholds when quantifying the clinical usefulness of a prediction model" (section "D: Decision curve analysis"); the 2% threshold is "for example". So the source fixes no single cost.
     - Lee et al. 1995 (the trial's own 30-day model, 14 predictors, 40,830 patients): the publisher's full text could not be reached (it refuses automated access), so only the abstract was read. It reports chi-square statistics per predictor ("age ... adjusted chi 2 = 717"; "these five characteristics contained 90% of the prognostic information"), "Risk modeling was performed with logistic multiple regression and validated with bootstrapping techniques", and "a validated model that stratified patient risk and accurately estimated the likelihood of death". Steyerberg and Vergouwe's Table 1 describes that model's evaluation as "Calibration and discrimination, but no indicators of clinical usefulness", validated by "Bootstrap and 10 fold cross-validation". Neither names one deciding metric.
   * **Experiments:** the shipped inputs on the 8 region folds; A and B as the case study defines them (the intercept with the linear predictor as offset, and the slope of the linear predictor); "better" counts the folds on which a model beats a plain logistic regression.

     | Model | ROC AUC | Better on | Log loss | Better on | Brier | Better on | A (fold range) | B (fold range) | Net benefit at 5% | Better on |
     |---|---|---|---|---|---|---|---|---|---|---|
     | Logistic regression | 0.8234 | - | 0.2008 | - | 0.05482 | - | -0.087 to 0.080 | 0.91 to 1.20 | 4.045% | - |
     | Logistic regression with splines | 0.8264 | 7 of 8 | 0.1997 | 7 of 8 | 0.05458 | 7 of 8 | -0.080 to 0.086 | 0.93 to 1.21 | 4.065% | 5 of 8 |
     | LightGBM, lightly tuned | 0.8272 | 7 of 8 | 0.1996 | 5 of 8 | 0.05468 | 5 of 8 | -0.105 to 0.088 | 0.94 to 1.20 | 4.126% | 7 of 8 |
     | LightGBM, defaults | 0.8200 | 3 of 8 | 0.2032 | 2 of 8 | 0.05560 | 1 of 8 | -0.080 to 0.111 | 0.83 to 1.03 | 4.018% | 3 of 8 |

     Mean B over the folds: 1.00 (logistic regression), 1.01 (splines), 1.03 (tuned LightGBM), 0.90 (default LightGBM, risks too extreme). Paired differences against logistic regression, in standard errors: splines 4.0 (ROC AUC), 4.4 (log loss), 2.7 (Brier); tuned LightGBM 2.6, 2.2, 1.0. Treating everyone gives a net benefit of 2.07% at 5%.
   * **Effect on the task:** all three threshold-free metrics put the same two models on top and default LightGBM last. They differ on the top pair: ROC AUC ranks tuned LightGBM first by 0.0008, log loss ties the two (0.19960 against 0.19965), and Brier ranks splines first. Log loss separates splines from logistic regression as sharply as ROC AUC does, and it penalises default LightGBM's too-extreme risks (slope 0.90) more (2 of 8 folds against 3 of 8).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | ROC AUC, the fallback (implemented) | scores ranking only; the source's C | the rule's default; follows heart_disease and gallstone_disease; comparable with the published 0.812 | blind to A and B, which the source scores and calls the c statistic blind to; with 73 of the collection's 83 binary tasks already scoring it, it adds no diversity |
     | b | Log loss, from context | a strictly proper rule on the predicted risk; ROC AUC named as the original c statistic | scores what A, B and C score together, as the domain practitioner asks; the source's own argument against C alone is the distinguishing fact; adds diversity (2 of 83 binary tasks score it, both from a competition) | a context metric the curator must accept against the heart_disease precedent; no published log loss to compare with |
     | c | Brier score, from context | the mean squared error of the predicted risk | the practitioner's readable alternative; also strictly proper | the framework has no `brier` metric, so a local metric is needed; it separates tuned LightGBM from logistic regression least (1.0 standard error) |
     | d | Net benefit at one threshold | the source's D as a cost | the source's usefulness measure | the source gives a range of thresholds (2%, 5%), so no single cost is fixed; ruled out[^3f] |

   * **Recommendation:** b: the source argues in its own words that the c statistic misses calibration, which the heart_disease case does not record of its source, so the absolute-risk decision the domain practitioner describes is a fact this case has and the precedent lacks; log loss resolves the methods as well as ROC AUC on the 8 folds and adds diversity. a stays defensible if the curator reads the four measures side by side as the precedent's case, since the source still names no single one. **Decision:** ROC AUC (a), log loss (b), or Brier (c)?

   **Notes for the AI:** on b, declare `Metric.from_context("log_loss", ...)` with the reason (the source's sentence on the c statistic, its A and B, the absolute-risk decision, the regions' death rates of 5.3% to 8.4%), name the case study's c statistic as the original, and re-run `dataset check` and the task probe. On c, the same with a local Brier metric.

   [^3d]: **MET-5** (Should): a paper that reports several metrics side by side without naming the one that decides has no unique original; declare the fallback. **MET-8** (Should): the fallback is `roc_auc` for binary tasks.
   [^3e]: **MET-11** (Must), its context origin: the source defines no metric, but the task makes one obvious, so the default would score the wrong thing; only when the context is clear. **MET-10** (Weigh): when the call stays in doubt, the metric that adds diversity to the collection wins (Andrej, 2026-11-02).
   [^3f]: **MET-7** (Should): a source that gives a range of costs or thresholds (a decision curve) fixes no single one, so its task is scored by a threshold-free metric.

   **Andrej (2026-11-25, discuss):** I am leaning towards log loss. But you name as a con: 'a context metric the curator must accept against the heart_disease precedent' - what is the actually right metric for this heart_disease dataset judging from the source?

   **Answer (AI, 2026-11-25):** judged from its source, heart_disease's right metric is a probability metric (log loss), not ROC AUC: Detrano et al. 1989 scored calibration and accuracy over thresholds and no ROC at all, so the precedent is a default and does not stand against log loss here; if anything it points the same way.

   * **Problem:**
     - Detrano et al. 1989 tested a probability model for "reliability and clinical utility" and nothing else: "A new discriminant function model for estimating probabilities of angiographic coronary disease was tested for reliability and clinical utility in 3 patient test groups" (abstract). Reliability is the mean predicted probability against the disease rate, overall and by quintiles (p. 306); clinical utility is "the percentage of patients correctly classified" (abstract), over the thresholds 0.2 to 0.8 (p. 307). The paper has no ROC curve, no c statistic and no ranking claim (heart_disease's record, full text read 2026-10-27).
     - Its main finding is a calibration finding, which ROC AUC cannot see: "Both algorithms overpredicted the probability of disease at the Hungarian and American centers. Overprediction was more pronounced with the use of CADENZA (average overestimation 16 vs 10% and 11 vs 5%, p less than 0.001). In the Swiss group, the discriminant function underestimated (by 7%) and CADENZA slightly overestimated (by 2%) disease probability" (abstract). Its conclusion is about probabilities too: "coronary disease probabilities derived from discriminant functions are reliable and clinically useful when applied to patients with chest pain syndromes and intermediate disease prevalence".
     - heart_disease declares ROC AUC as the binary fallback, not as the source's measure, and its own metric reason says so: "ROC AUC per held-out hospital does not score reliability". The "not log_loss" part is one line on the three single-hospital records, before the merge and the split by hospital: "proposal accepted: roc_auc (fallback) for the heart_disease_* datasets, not log_loss" (Lennart, 2026-10-21), with no reason recorded; the merged record kept "Metric `roc_auc` (fallback) as declared" (Lennart, 2026-10-27). The rule on probabilities cites the same paper as a source that "asked for probabilities"[^3g].
     - So the precedent says only that the fallback was taken when a source scores two things side by side; it records no argument for ranking over probabilities. GUSTO-I's source scores calibration too and says in its own words that the c statistic misses it, so the two cases agree on the facts, and both point to a probability metric.
   * **Experiments:** heart_disease as shipped (796 patients, 13 inputs, the hospital held out, train on the other two), four models and the training disease rate as a constant; the means over the three hospitals:

     | Model | ROC AUC | Log loss | Brier | Correctly classified, mean over 0.2 to 0.8 |
     |---|---|---|---|---|
     | Training disease rate | 0.500 | 0.746 | 0.276 | 0.470 |
     | Logistic regression | 0.824 | 0.711 | 0.209 | 0.702 |
     | Random forest | 0.835 | 0.539 | 0.180 | 0.679 |
     | LightGBM, lightly tuned | 0.827 | 0.545 | 0.183 | 0.703 |
     | LightGBM, defaults | 0.795 | 0.661 | 0.207 | 0.705 |

     Detrano's reliability per held-out hospital (mean predicted against observed disease rate), with the two threshold-free scores:

     | Held-out hospital | Observed | Logistic regression: predicted, ROC AUC, log loss | LightGBM, lightly tuned: predicted, ROC AUC, log loss |
     |---|---|---|---|
     | Cleveland | 0.459 | 0.259, 0.877, 0.617 | 0.497, 0.865, 0.465 |
     | Hungary | 0.361 | 0.462, 0.901, 0.414 | 0.520, 0.896, 0.482 |
     | VA Long Beach | 0.744 | 0.454, 0.694, 1.103 | 0.518, 0.721, 0.687 |

   * **Effect on the task:** on heart_disease the metrics disagree where the source's question lies. Logistic regression is third of the four models by ROC AUC (0.824, within 0.011 of the best and ahead of default LightGBM) but last by log loss and Brier, because it misjudges the disease rate of a new hospital (0.26 predicted against 0.46 observed in Cleveland, 0.45 against 0.74 in Long Beach, where its log loss of 1.10 is worse than the constant's 0.80). That misjudgement is what Detrano measured and ROC AUC ignores. On GUSTO-I's 8 folds the metrics agree (the earlier table), so log loss there costs no resolution.
   * **Separate fact, for a decision of its own (heart_disease is not changed here):** heart_disease's `roc_auc` looks mis-specified against its source. The source scores reliability and accuracy over thresholds, its finding is the miscalibration at new hospitals, its split holds out whole hospitals to pose exactly that question, and the definition's own reason says ROC AUC does not score it. Since the binary fallback is ROC AUC, moving it to log loss would be a context metric there too, with this reason[^3h]. The merged record's Comments also say the study "found that the model ranks patients well", which the full-text read of 2026-10-27 does not support (no ROC analysis in the paper).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Log loss for GUSTO-I now; heart_disease raised as its own item | b of the earlier answer: `Metric.from_context("log_loss", ...)`, with the c statistic named as the original; heart_disease's metric goes to its own review | both sources score calibration and GUSTO-I's argues against the c statistic alone; the heart_disease precedent is a fallback with no argument against probabilities; adds diversity | the two datasets differ until heart_disease is decided |
     | b | Log loss for both, decided together | a, and heart_disease moves to log loss in the same round | one reading of one rule for both calibration sources | changes a shipped definition reviewed twice (2026-10-21, 2026-10-27) by Lennart, whose call it was |
     | c | ROC AUC for both | GUSTO-I keeps the fallback, as heart_disease | consistent with the two decisions as they stand | scores neither source's calibration, which both sources measure and GUSTO-I's calls the c statistic blind to |

   * **Recommendation:** a: the precedent does not stand against log loss, because heart_disease's source never scored ranking, so GUSTO-I can move now on its own facts; heart_disease's metric is a separate call for Lennart, who made it. **Decision:** a, b or c?

   [^3g]: **MET-8** (Should): with no fixed threshold metric or no unique metric, score by a strictly proper rule or a ranking metric, the fallback `roc_auc` for binary tasks; "A source that scores calibration together with hard-label accuracy (Detrano 1989's reliability and percent correctly classified) asked for probabilities."
   [^3h]: **MET-11** (Must), its context origin: the source defines no metric, but the task makes one obvious, so the default would score the wrong thing; the reason says why. **MET-5** (Should): a paper that reports several metrics side by side has no unique original.

   **Andrej (2026-11-25, discuss):** "Reply (b): Log loss for both, decided together"

   **Resolved (2026-11-25, Andrej):** b: log loss for GUSTO-I and for heart_disease, decided together. `dataset.py` declares `Metric.from_context("log_loss", ...)` in place of the roc_auc fallback; the reason quotes the case study's sentence that the c statistic "is insensitive to systematic errors in calibration", gives the absolute-risk decision and the regions' death rates of 5.3% to 8.4%, and names the case study's c statistic (0.813 internal, 0.812 US to non-US) as the original; the probe note gives the log-loss figures. Check: 0 errors, 0 warnings (2 accepted), 3 info. Task probe by log loss: linear 0.2006, random forest 0.2039, LightGBM 0.2044, age alone 0.2322, class shares 0.2547; no flag. heart_disease moves to log loss from context in its own definition and record, on Detrano et al. 1989's reliability and accuracy over thresholds; this reverses its roc_auc fallback of 2026-10-21.

4. **Keep the ages 108, 108 and 110, or set them to missing?**

   * **Problem:**
     - Three patients are recorded as 108, 108 and 110 years old, in whole numbers, while 98.8% of the ages carry a fraction.
     - They are likely entry errors, but an age over 100 is unusual, not impossible, and only impossible values become missing[^4a].
   * **Effect on the task:** none measurable: three of 40,826 rows.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with a note (implemented) | the three ages stay as recorded; the notes name them | the cleaning rule as written; no guess about the true age | three likely errors stay in the inputs |
     | B | Set them to missing | the three ages become blank | removes three likely errors | treats unusual values as impossible, against the rule's text |

   * **Recommendation:** A: the rule keeps values that are only unusual, and three rows cannot move a score. **Decision:** keep (A) or set to missing (B)?

   **Notes for the AI:** on B, in `_clean` mask `age` where it is 108 or above and a whole number (3 rows), assert the count, and change the notes' bullet on impossible values.

   [^4a]: **CLEAN-11** (Should): impossible values become missing, and the row stays; values that are only unusual stay.

   **Andrej (2026-11-25, ok):** As implemented (A).

   **Resolved (2026-11-25, Andrej):** A: the ages 108, 108 and 110 stay as recorded, and the notes' bullet on impossible values names them. `dataset.py` is unchanged for this issue.

**Review panel:** ship after changes (mediator). Claim audit: about 30 claims, none that bears on validity or value refuted; 3 small ones refuted (the 40,830 count, the "mostly Killip IV" note, the warning not accepted in the definition), all fixed. Column audit: a new leak, the filled-in heights mark patients who died (fixed by dropping `height`). Split audit: right, with notes (leaf confirmed; accept the warning; name the US to non-US transfer). Blind review: would include; main concern the small spread between methods. Task gamer: the height-fill flag worth +0.007, no other exploit. Debate: agreed on `ttr`, `height`, the five flags, the split leaf and the wording; disputed: the fold layout (issue 1), the metric (issue 3), the mic option (issue 2) and the ages (issue 4).

<details><summary>Mediator</summary>

I recommend shipping `gusto_i_mi_mortality` after the changes below. One is required by a Must rule: drop `height`. Four calls go to Andrej. I ran two experiments to settle disputed facts.

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds (open permission text); USE-1, USE-5 hold; USE-8 holds (direct fit; the thrombolysis era is an
  `Outdated` note, SEL-18; the source's time to treatment is missing from the file, noted); USE-3/LEAK-1 triggered by
  `ttr`, fixed (dropped); LEAK-10 (through LEAK-38's conditional-test clause) triggered by the filled-in heights, fixed
  by dropping `height`; LEAK-19 holds (4 copies dropped, the 28-row template kept with a note); SPLIT L-PLACE.groups
  holds, `groups_test_groups_few` to be accepted; PROV holds (the US cohort and the death rates by arm reproduce).
Value: TP-2, a large signal; TP-3, tuned methods spread (+0.006 AUC, SE 0.0009, 9 of 9 folds): keep; TP-4, not
  Trivial (TIMI 0.794); MET-5/MET-8: the `roc_auc` fallback holds.
Quality: CLEAN-5/CLEAN-22, the drop of the five flags departs from the rule's text and from precedent: keep them;
  CLEAN-11, impossible pulse and pressure values set to missing.
Weighed: size +, source +, era -, small spread -.
For the curator: issue 1 (fold layout), 2 (mic option B or C), 3 (metric), 4 (three ages).
```

**Changes to make now (no decision needed)**

1. **Drop `height` (LEAK-10 Must, through LEAK-38).** The conditional test measures the mechanism: odds ratio 2.65, p = 2e-54, and it holds in 15 of 16 regions. The milder fixes fail:
   - setting the fills to missing keeps the signal (LEAK-40);
   - rounding to whole centimetres still lets a model find the filled rows at AUC 0.82 (LEAK-13; the critic's rounding test).

   My run shows the drop removes the leak completely:
   - without `height`, the filled-height rows cannot be found from the other columns (AUC 0.535);
   - the fill-looking weights carry no signal (adjusted OR 1.01, p = 0.91), and a weight-fill flag adds +0.0000 AUC, better on 1 of 9 folds;
   - for comparison, the height-fill flag adds +0.0068, better on 9 of 9.

   Write the mechanism into the notes as LEAK-40's marker paragraph asks: what was recorded differently by class, how much it gives away, what was done. Suggest the `Class-dependent Recording` marker to the curator.
2. **Keep `sho`, `hig`, `ant`, `hyp` and `hrt` as released (CLEAN-22 Must, CLEAN-5).** None of them is an exact copy. The curators kept columns of the same kind in expresso_churn_prediction (`ARPU_SEGMENT`) and 2_month_survival_rate_prediction (`dzclass`). Both sides agree. The curator can still record the drop as an exception, but the fact it would rest on (cut points chosen on this cohort) is unverified. The `tpa` drop stands (kdd_cup_09_appetency).
3. **Set impossible values to missing (CLEAN-11, ≤ 8 cells):** pulse of 1 to 9, and a pulse or systolic pressure of 0 in Killip I patients. Fix the "mostly Killip IV" note: 3 of the 8 patients are Killip I.
4. **Record `groups_test_groups_few` in `accepted_check_warnings` (house rule).** Reason: LR 0.820, RF 0.815, LightGBM 0.821 across regions; 11,215 to 15,610 patients and 793 to 1,119 deaths per test fold. Under 1×8 (issue 1), reword it and also accept `splits_dimensions_off_protocol`.
5. **Wording (USE-8, USE-1, writing):**
   - `row`: 40,826 patients;
   - name the population in `use_case` and `fit_reason`: STEMI patients eligible for thrombolysis, within 6 h;
   - replace "as in the source's model" with a note that the source's time to treatment is not in the file;
   - take the split sentence out of `use_case`;
   - remove height from `known`, and update `changes` (height dropped, flags kept);
   - `splits_comment`: the US → non-US transfer scores 0.815 to 0.820, inside the range of the region folds;
   - `time_basis`: say that later patients are untested;
   - replace the `no_spread` note with the tuned numbers below.
6. **Add the `Outdated` note to the record (SEL-18).** The screening, the mic item and the precedents (cirrhosis, 2_month_survival, protein_model_quality) all carry it. The fit stays `direct`, per the written USE-8 case row.

**Issues for the curator, ranked**

**1. Fold layout: 3×3 or 1×8 (P4, SPLIT protocol, Should).**

- **Precedent fact the precedent checker had out of date:** economic_well_being now ships 1×9 over 25 countries (Andrej, 2026-11-25). It was chosen over 3×3 because 3×3 sat farther from leave-one-out and shrank the method gaps. Leave one country out on 10 or 16 countries was an earlier stage. The critic has this right; the advocate's rebuttal rests on the old reading.
- **My measurement** (without `height`; 6 draws per design; mean AUC over folds; reference is leave one region out):

  | Design | LR | LR splines | LightGBM tuned | Gap LightGBM − LR |
  |---|---|---|---|---|
  | Leave one region out, 16 | 0.8189 | 0.8248 | 0.8256 | 0.0067 |
  | 1×8 | 0.8202 | 0.8263 | 0.8269 | 0.0067 |
  | 3×3 | 0.8208 | 0.8266 | 0.8264 | 0.0056 |

- **What sets this case apart only in part:** 3×3 is not farther from the reference in level here, because the regions are large and alike. But it does shrink the gap by 0.001 and swaps the order of the top two models by 0.0002, within noise. 1×8 matches the reference's order and gap, at a noisier score per fold (SD over draws 0.0010 against 0.0003).
- **Advocate:** 3×3 is the protocol default, test folds are stable (793 to 1,119 deaths), and sat11 and huesken were accepted at 3×3.
- **Critic:** the economic_well_being measurement applies to 16 groups.
- **Lean:** 1×8, weakly, to follow the economic_well_being reasoning. **Decision:** 3×3 or 1×8?

**2. mic option B or C is not decided (P5, PROV-4; who decides).** issues/mic.md still ends "Decision: A, B, C or D?". This record has no CC line, `suggestion: TBD -> Yes` and `checked_by: AI (UNVERIFIED)`. The review must not say "joins next to mic" as settled. Both mic options B and C add this dataset; they differ on whether mic stays. **Decision:** the mic item's option, and a CC line moving this record to `Yes`.

**3. Metric: `roc_auc` or `log_loss` (P6; MET-8 Should, MET-11, MET-10 Weigh).**

- **Settled by rule:** MET-8 does not require log loss. It names `roc_auc` as the binary fallback. Its calibration clause contrasts probabilities with hard-label accuracy, not ROC AUC with log loss. heart_disease is the MET-8 case with the same fact pattern (a source scoring calibration plus another measure) and went `roc_auc` (Lennart, 2026-10-21). So the critic's "MET-8 decides" fails, and `roc_auc` holds by default.
- **What is open:** log loss would be a MET-11 `context` choice, which needs a fact that sets this case apart from heart_disease.
  - Critic and domain practitioner: the thrombolytic choice acts on the absolute risk, and regional death rates run from 5.3% to 8.4%.
  - Advocate: precedent and consistency.
- Both metrics separate methods on 9 of 9 folds, so separation does not favour either. If the call stays in doubt, MET-10's diversity factor applies.
- **Decision:** `roc_auc`, or `log_loss` with the absolute-risk fact recorded.

**4. Ages 108, 108 and 110 (P7, CLEAN-11).** They are whole numbers, while 98.8% of ages are fractional. They are likely entry errors, but they are not impossible, and three rows cannot move a score. **Decision:** keep with a note, or set to missing.

**Not for the curator:**

- **`no_spread` / TP-3:** tuned LightGBM and spline LR beat plain LR by about 0.006 AUC with SE 0.0009, on 9 of 9 folds. That is spread under the flag's 2×SE criterion. No rule retires a task on this flag (amex). The critic conceded.
- **Fit:** `direct` (USE-8 case row).

**Agreed facts**

- **`ttr`:** the only column unbalanced across the randomised arms (p = 2.7e-11, all others p ≥ 0.087), so it is recorded after treatment and is dropped.
- **Filled heights:**
  - 2,132 filled heights (5.2% of rows), 19.9% of them died against about 6% of the rest;
  - adjusted OR 2.65, holding in 15 of 16 regions;
  - worth +0.0045 to +0.007 AUC to a model that spots them;
  - dropping `height` costs logistic regression +0.0001 (nothing) and tuned LightGBM −0.0009 to −0.002, which is the leak itself.
- **Splits and regions:**
  - the 16 regions reproduce the US cohort exactly (23,034 patients, 1,565 deaths) and the West region;
  - grouped and random folds score alike (0.820 against 0.821);
  - the US → non-US transfer scores 0.815 to 0.820;
  - test folds hold 5 or 6 regions and 793 to 1,119 deaths.
- **Not Trivial:** TIMI reaches 0.794 against about 0.826 for the methods.
- **Duplicates and template rows:** 4 exact copies dropped. The 28 template rows (0.07%) do not carry their labels across the split (nearest-copy AUC 0.56 to 0.58).
- **Data checks:** death rates by arm match NEJM 1993; the code "2 = yes" holds for `prevcvd` and `prevcabg`.
- **Wording:** the "40,830" count and the "mostly Killip IV" note are wrong.
- **The task:** the use case is real and the fit direct; the era is a note, not an exclusion.

**Task-gamer exploits**

The definition has no `Potential leak, kept on purpose:` notes and no accepted warnings, so none of these exploits was known in advance.

| # | Exploit | Rule | New or known | Outcome |
|---|---|---|---|---|
| 1 | Flag for filled height or weight, +0.007 | LEAK-10 via LEAK-38 (Must); LEAK-13 and LEAK-40 tested as fixes | **New.** The number-format probe (0.546) missed it | Fixed by the `height` drop; the weight part measures +0.0000 |
| 2 | How often each height value occurs, +0.008 | Same mechanism (LEAK-10); counting over test rows adds nothing (LEAK-30 not triggered) | New | Same fix |
| 3 | Unit format (cm or converted inches), +0.0014 | Not LEAK-13: it follows the site's units, not the outcome (equal death rates within a region); a deployed model knows its own site's units | New, no violation | Keep; optionally one note line |
| – | Template rows and near copies | LEAK-19 | Known, documented | Measured no gain, as the note says |
| – | Sentinel zeros | CLEAN-11 | Known; its note is reworded | Change 3 |

**Consistency with precedent**

- **Follows precedent:**
  - `ttr` dropped (kickstarter `staff_pick`);
  - `tx` kept (cirrhosis `Drug`);
  - `tpa` dropped (kdd_cup_09_appetency);
  - `height` dropped (expresso REGION, kick WheelType: the LEAK-38 conditional test);
  - the five flags kept (expresso `ARPU_SEGMENT`, 2_month_survival `dzclass`);
  - `Outdated` with fit `direct` (2_month_survival, the USE-8 row);
  - `roc_auc` (heart_disease, gallstone_disease);
  - TP-3 keep (amex).
- **Departure without a distinguishing fact, if taken:**
  - 3×3 against economic_well_being's 1×9, unless the curator takes "no bias in level" as the fact that sets this case apart (issue 1);
  - `log_loss` against heart_disease, unless the absolute-risk fact is recorded (issue 3).
- **Precedent checker's error:** it cited economic_well_being as leave one country out on 18 or 10 countries. Its final state (2026-11-25) is 1×9 over 25 countries, chosen on a measurement.
- **Outside this dataset:** the precedent checker flagged an inconsistency between cirrhosis (`approximate`) and 2_month_survival (`direct`) on the fit of a dated treatment era. It belongs in a separate cross-dataset item, not here.

</details>

<details><summary>Claim audit</summary>

**Claim audit: `gusto_i_mi_mortality`**

No claim that affects validity or value was refuted. I tested about 30 claims against the raw file, the definition's frame and splits, and the Steyerberg and Vergouwe 2014 text, and the definition's numbers reproduce exactly. Two small claims are refuted, both wording or quality fixes. One step the builder only proposed is missing from the definition.

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | `ttr` is recorded after treatment, because the randomised arm changes it | curation_comments; the Decision; record | Chi-square of every raw column against `tx`; check the variable label on the web | **holds** | `ttr` p = 2.7e-11; all 25 other columns p 0.087–0.98. By arm: SK 66.3%, SK+tPA 64.6%, tPA 62.3%, in the order of reperfusion speed. Label confirmed: arXiv 2112.02524 and mice-ext-val both define it as "time to relief of chest pain > 1 h". Lee et al.'s "time to treatment" is a different variable and is not in the file. | USE-3, LEAK-1 |
| 2 | `sho`, `hig` and `ant` are exact recodes; `hyp` and `hrt` are thresholds with 5 and 8 exceptions at the cut | curation_comments | Crosstabs | **holds** | sho = Killip III/IV, ant = miloc Anterior, hig = Anterior or pmi: all exact. The `hyp` exceptions are 5 rows at sysbp exactly 100; the `hrt` exceptions are 8 rows at pulse exactly 80. | CLEAN-5 |
| 3 | `tpa` repeats `tx`, blank for the combination arm | curation_comments | Value counts | **holds** | 20,162 / 10,348 / 10,320 NaN, matching `tx` | CLEAN-5 |
| 4 | Regions 1, 7, 9, 10, 11, 12, 14, 15 are the US cohort (23,034 patients, 1,565 deaths) and the other eight are non-US | curation_comments; grouping; task_summary.split | Search all 12,870 sets of 8 regions for that n and death count; check against the paper | **holds** | That set is the only 8-region match on both n and deaths. Four region sets of any size match n alone, so the death count is what decides it. The paper gives "n = 23 034, 1565 deaths … outside of the USA (n = 17 796, 1286 deaths)". | SPLIT (L-PLACE) |
| 5 | Region 1 is the West-region subsample (2,188 patients; hypertension 40.4%, angina 34.0%, family history 47.6%) | module comment | Region-1 share of code 2 | **holds** | n = 2,188; shares 0.404, 0.340, 0.476 | CLEAN-12 |
| 6 | Code 2 means "yes" for `prevcvd` and `prevcabg` (stated as inferred) | module comment | Decisive test: compare patients with code 2 on the history columns that should go with it | **holds** | prevcabg = 2: previous MI 65.7% against 14.2%, angina 78.4% against 35.0%. prevcvd = 2: age 68.7 against 60.7, hypertension 59.1% against 37.6%, death 15.7% against 6.8%. | CLEAN-12 |
| 7 | `grpl` and `grps` nest in the regions; every `grps` group has ≥ 20 deaths and every `grpl` group ≥ 47 | curation_comments | Groupby | **holds** for the facts | 0 groups cross a region; minimum deaths 20 and 47. Reading these groups as "cut to an event minimum, not places" is plausible but **untested**: there is no codebook. | SPLIT |
| 8 | 4 exact duplicate rows, all survivors, all in region 4 and in the template pattern; 8 more feature copies after the drops | curation_comments; `_clean` assertion | `raw.duplicated()`; feature-key copies across the shipped folds | **holds** | 4 duplicates, region {4}, day30 {0}. After the drops, 24 rows sit in feature-copy sets. Summed over the 9 folds, 41 test rows have an exact feature copy in train (0.01%). | LEAK-19 |
| 9 | 28 template rows from 7 regions and 3 arms, 7 deaths, likely imputation fills | curation_comments | Filter on the template values | **holds** | 28 rows, 7 died, 7 regions, 3 arms, `ttr` = 1. They are stranger than the comment says: identical age to three decimals (31.102, 40.664, …) across different regions and arms, which no set of independent patients would show. This supports "not real values"; at 0.07% of rows it changes no score. | PROV |
| 10 | Systolic pressure 0 in 6 patients and pulse 0 in 4 (8 patients, 7 died), "mostly Killip IV, unmeasurable pressure in shock" | curation_comments | Crosstab | **refuted (wording)** | Of the 8: Killip IV 3, III 2, **I 3**. Row 37544 (Killip I, sysbp 0) and rows 13866 and 16407 (Killip I, pulse 0, one of them with sysbp 110) are not shock; they look like missing values coded as 0. | CLEAN (P7) |
| 11 | Age over 100 in 3 patients (108, 108, 110); 26 under 25 | curation_comments | Count | **holds** (counts); plausibility not settled | Ages 108, 108, 110 are almost certainly entry errors. They are kept as recorded and documented. | CLEAN |
| 12 | `tx` is known at enrolment; Lee et al. include the thrombolytic; dropping it costs 0.000 to 0.002 AUC | curation_comments | Builder's experiments.out; web | **holds** | Region split, without `tx`: LR −0.0002, LGBM −0.0020. The Lee abstract lists "type of thrombolytic therapy" among the significant factors. | USE-3 |
| 13 | 191 of the 41,021 enrolled are missing; death rates by arm match the trial | curation_comments | Rates by arm | **holds** | 7.32% SK (merged), 6.31% tPA, 7.01% SK+tPA | PROV |
| 14 | "40,826 patients, 2,851 deaths (7.0%)" after cleaning | task_summary.predicted; builder | Frame from `from_definition` | **holds** | 40,826 × 20; 2,851 Yes (6.98%) | — |
| 15 | task_summary.row says "One of 40,830 patients" | task_summary.row | — | **refuted (minor)** | The shipped table holds 40,826 patients (4 copies dropped). | writing |
| 16 | Split: whole regions held out, 5–6 per test fold, with no overlap | splits_comment; time_basis | Regions of each fold's train and test sets | **holds** | 9 folds; train/test region overlap 0 in every fold; 5–6 test regions per fold; 11,215–15,610 test rows | SPLIT |
| 17 | Grouped and IID score alike (no cluster effect) | curation_comments; groups_not_clustered info | Builder experiments.out | **holds** | LR 0.8203 by region against 0.8211 random; LGBM 0.8238 against 0.8238 | SPLIT |
| 18 | Accepted warning `groups_test_groups_few` | builder report ("proposed for acceptance") | Look for `accepted_check_warnings` in dataset.py; README `accepted: {}` | **refuted (process)** | The definition has no `accepted_check_warnings`, so the warning stands unaccepted and its reason (group probe LR 0.820 / LGBM 0.821) is not recorded. | house rule (check warnings) |
| 19 | Not Trivial: the TIMI STEMI score (not fitted on these data) reaches 0.794, against about 0.82 for the methods | curation_comments | Recompute TIMI on the whole raw file | **holds** | 0.7941. Age alone scores 0.745 on the whole file; the README's 0.729 is the probe's cross-validated number, and the paper gives 0.75. | TP-4 |
| 20 | `no_spread`: LR, RF and LightGBM all ≈ 0.82 | Note; probes | task.out; experiments.out | **holds** | LGBM − LR = +0.0035 by region, LGBM ahead on 11 of 15 folds. This is a value risk, not a refutation. | TP-3 |
| 21 | Metric is the `roc_auc` fallback because the source has no single deliberate metric | `Metric.fallback` reason | Read Steyerberg and Vergouwe 2014; search for a c index in Lee et al. 1995 | **holds** | The paper names four measures as a set: "calibration-in-the-large … calibration slope … concordance statistic … decision-curve analysis", with no single criterion. It reports c of 0.813 internal and 0.812 external, and 0.75 for age alone. No c index for Lee et al. 1995 was found (full text still unread). | MET-5, MET-8 |
| 22 | Metric is computable on every fold; no scoring columns are needed | Metric (inputs {}) | Dummy (prior) and random predictions on each fold | **holds** | Positives per test fold: 793–1,119. Dummy AUC 0.5 and random 0.49–0.51 on all 9 folds. The unit is the row, and nothing is needed outside the features. | MET-2 |
| 23 | Missing predictor values were filled by single imputation using correlations between predictors | curation_comments | Steyerberg and Vergouwe text | **holds** (quote verified) | Whether the outcome entered the imputation model, which would be a leak path, is **untested**: the paper says "between predictor variables" only. | LEAK |
| 24 | (Implied) every kept input is known at presentation | fit_reason | Balance against the randomised arm, used as a test for being measured after treatment | **holds** | Every kept column is balanced across arms (p ≥ 0.087); only `ttr` fails. | USE-3 |
| 25 | (Implied) the target is the real one | predicted | Death rate by arm against the trial's | **holds** | Matches the NEJM 1993 rates | USE |

**Refuted claims, ranked**

1. **The accepted warning (#18), house rule, low.** The builder reports the warning as accepted, but `dataset.py` has no `accepted_check_warnings` entry. `dataset check` will keep raising `groups_test_groups_few` with no recorded reason.
   - **Mildest remedy:** add `accepted_check_warnings = {"groups_test_groups_few": "<the group probe's real signal across regions: LR 0.820, RF 0.815, LightGBM 0.821; each test fold holds 11,215 to 15,610 patients and 793 to 1,119 deaths>"}`.
2. **Zero blood pressure and pulse (#10), P7 quality, low.** "Mostly Killip IV, unmeasurable pressure in shock" is wrong: 3 of the 8 patients are Killip I, which rules out cardiogenic shock. Their zeros look like missing values coded as 0.
   - **Mildest remedy:** reword the bullet. Optionally, and as the curator's call, set the zeros of the Killip I patients to missing. That touches 3 rows, so no score moves.
3. **"One of 40,830 patients" (#15), writing, trivial.** The shipped table holds 40,826.
   - **Mildest remedy:** say 40,826 in `task_summary.row`, or "the 40,830 of the file, 4 copies dropped".

**Untested claims, ranked**

1. **Imputation used only the predictors (#23), validity (LEAK), weak suspicion only.** If the case-study authors' single imputation used `day30`, the filled values would carry the label. The file cannot show which values were imputed.
   - The 28 template rows (25% died, identical ages across regions) are the visible trace, and they are too few to move a score.
   - The leak probe shows no format signal (number format alone 0.546).
   - **Remedy:** none needed beyond the existing note. One could add that the imputation model's inputs are unknown.
2. **`grpl` and `grps` are event-minimum hospital groups, not places (#7).** The facts hold, but the meaning has no codebook behind it. It does not change the split: finer groupings score the same, 0.821 to 0.825.
3. **Lee et al. 1995 full text (#21).** A c index there would not change MET-5, since Steyerberg and Vergouwe still report four measures. It would only refine the fallback's reason.

Everything else that carries weight reproduces exactly. That includes dropping `ttr` (the decisive balance test across arms), the US/non-US mapping of the regions (the only 8-region set that matches both counts), the coding of the history columns, the split, and the metric's fallback and computability. Nothing here argues against shipping. The open weighing question remains `no_spread`, which the builder has already raised.

Sources:
- [Steyerberg & Vergouwe 2014, PMC4155437](https://pmc.ncbi.nlm.nih.gov/articles/PMC4155437/)
- [Lee et al. 1995, PubMed 7882472](https://pubmed.ncbi.nlm.nih.gov/7882472/)
- [arXiv 2112.02524 (GUSTO-I variable table)](https://arxiv.org/pdf/2112.02524)
- [mice-ext-val gusto reference](https://metodologianavarrabiomed.github.io/mice-ext-val/reference/gusto.html)

</details>

<details><summary>Column audit</summary>

I audited all 20 columns. One problem matters: the file's filled-in heights are tied to death, and that link cannot exist at presentation. It is a leak that the probes and the builder did not find. The other columns are fine, apart from a few tiny cleaning questions.

**Column audit: gusto_i_mi_mortality**

**Files.** The release has one table: `gusto.rda` on hbiostat, the same 40,830 × 29 table that R's predtools ships. `_load_raw` reads its CSV export, so no file was left out. I could not open the hbiostat `/data/repo/` index (it returns 404), so I am relying on the builder's statement that nothing else is listed there.

**Columns.** The cleaned frame has 40,826 rows and 20 columns: 18 inputs, the target and `region`.

| column | meaning (source) | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| death_by_day_30 | death within 30 days of enrolment (`day30`) | target | category No/Yes | fine | CLEAN-25 |
| age | age in years, to the day | yes | float; min 19.0; 3 patients at 108, 108 and 110 (whole numbers, while 98.8% of ages are fractional) | fine; 108–110 is a minor question | CLEAN-11 |
| sex | sex | yes | category | fine | |
| Killip | Killip class I–IV at presentation | yes | ordinal I<II<III<IV, the correct order; death rate rises 5.1 → 13.9 → 32.8 → 57.8% | fine | CLEAN-14 |
| ste | number of ECG leads with ST elevation | yes, from the enrolment ECG | int 0–11, a count; 2,309 patients have 0 or 1 lead although the trial enrolled on ST elevation in ≥2 leads (as published) | fine | |
| pulse | heart rate at presentation | yes | int 0–246; 0 in 4 patients; 1, 6, 8 and 9 in four Killip I patients, three of them survivors, one with SBP 180 | **minor cleaning**: values below 20 with a measured pressure are impossible and should be missing | CLEAN-11 |
| sysbp | systolic blood pressure | yes | int 0–280; 0 in 6 patients, mostly Killip III/IV and dead (unmeasurable in shock) | fine; keeping 0 as a meaningful code is defensible | CLEAN-10 |
| miloc | infarct location (Anterior / Inferior / Other) | yes (ECG) | category | fine | |
| height | height in cm | the value is known at presentation, **but its fills are not** | float 140–212.5 | **leak** (finding 1) | LEAK-1/USE-3, SPLIT-32 "values fitted over the whole release", outcome-caused missingness |
| weight | weight in kg | yes | float 36–213; the fill-looking weights (1,028) carry no outcome signal (adjusted coefficient −0.001, p = 0.99) | fine | |
| pmi | previous MI | yes | category | fine | |
| htn | history of hypertension (1/2 → no/yes) | yes | category; "yes" share matches the published West-region table | fine | CLEAN-12 |
| smk | smoking: never / quit / current | yes | nominal category; the codebook gives no order | fine | |
| pan | previous angina (unlabelled in the file) | yes | category; matches the published share 34.0% vs 34.1% | fine | |
| fam | family history of MI | yes | category; "yes" has *lower* death (5.3% vs 8.2%), but the code is confirmed by the West-region share and the pattern fits a younger group | fine | |
| prevcvd | previous cerebrovascular disease | yes | category; 2 = yes is inferred (2.0%, 15.7% died) | fine (inferred) | |
| prevcabg | previous bypass surgery | yes | category; 2 = yes is inferred (4.4%) | fine (inferred) | |
| dia | diabetes (0/1) | yes | category; 14.7% matches the trial | fine | |
| tx | randomised arm (SK / tPA / SK+tPA) | yes, randomised at enrolment | category | fine; the use case gives the risk under each regimen | |
| region | 16 regions | not a feature | group column only | fine | |

**Dropped columns.** I agree with every drop:
- `ttr` is after treatment (the arms differ, p = 3e-11).
- `sho`, `hig` and `ant` are exact recodes of other columns.
- `hyp` and `hrt` are threshold recodes.
- `tpa` repeats `tx`.
- `grpl` and `grps` are groups of hospitals cut to a minimum number of deaths.

The dtype probe flagged none of the 18 columns. Missing share by period does not apply: the task is grouped and the file has no dates.

**Problems, ranked**

**1. Leak: the filled-in heights mark patients who died (Must, LEAK-1 / USE-3; strength moderate, the largest gain from any input decision in this dataset)**

The source says missing predictor values "were filled in with a single imputation procedure considering correlations between predictor variables" (Steyerberg and Vergouwe 2014). It does not say whether the outcome entered that imputation.

**What the heights look like.** 2,132 heights (5.2%) are neither a whole or half centimetre nor an inch conversion, leaving aside one spike at 177.3. For example: 171.8, 171.3, 170.3. They spread less than measured heights (male SD 5.9 vs 7.3), which is how regression fills look.

**How they relate to death.**

- 19.9% of these patients died, against about 6% of the rest.
- The pattern holds in 15 of 16 regions (14.8–26.7% against 4.5–7.8%) and in both the US and non-US regions.
- After adjusting for age, sex, Killip class, blood pressure, pulse, location, ST leads, previous MI and region, the odds ratio is 2.65 (p = 2e-54).
- Killip class differs only a little between the two groups, so how sick a patient was at presentation does not explain it.

**Why it is a leak.** Either the height was never recorded because the patient died early, or the outcome was used to fill it. In both cases the signal arises after the prediction point. A deployed model would get a measured or estimated height, not a fill.

**Measured on the shipped splits** (9 folds, by region):

| change to height | LightGBM ROC AUC | spline logistic regression ROC AUC |
|---|---|---|
| as shipped | 0.8272 | 0.8261 |
| dropped | −0.0020 (worse on 8 of 9 folds) | +0.0001 |
| fills set to missing | +0.0045 (better on 9 of 9) | +0.0004 |
| a "fill" flag added | +0.0045 (better on 9 of 9) | +0.0066 (better on 9 of 9) |

**What this means.**

- Height adds nothing to a logistic regression. The 0.002 LightGBM gets from it is most likely the fill pattern, found from the fine-grained values.
- A participant who spots the decimals can gain 0.005–0.007.
- That is larger than the 0.003 for which `ttr` was dropped under LEAK-1.
- It matters more because this task otherwise flags `no_spread`: the artefact is a large share of what separates the models.

**Remedies, mildest first:**

- (a) Drop `height` (implemented in neither case). It costs a regression nothing and LightGBM only the leaked 0.002. The curation note should say why, and that Lee et al.'s height effect may partly reflect the same fills.
- (b) Keep it and record the leak as accepted.
- Setting the fills to missing does **not** fix it: the missingness carries the same signal (0.8317).

Undetectable fills in the categorical columns may carry the same bias, but the file cannot show them. The 28-row template the builder documented (25% died) fits this mechanism.

**2. Minor cleaning (Should, CLEAN-11)**

- **Pulse.** Pulse values of 1, 6, 8 and 9 in four Killip I patients, three of whom survived (one with SBP 180), are impossible; they could become missing. Pulse 0 with a measured pressure (2 patients, one died) is in the same class. The effect is negligible (≤ 8 cells).
- **Age.** Ages 108, 108 and 110 are entered as whole numbers, unlike the rest of the column. This is a question, not a fix: they are unusual rather than impossible.

**3. Question for the curator, no change**

The file gives no ground truth for `prevcvd` and `prevcabg` being 2 = yes. The rarer level having the higher death rate is consistent with that reading.

Nothing else: every other input is recorded at presentation and is coded as its codebook says.

</details>

<details><summary>Split audit</summary>

**Split audit: gusto_i_mi_mortality. Verdict: right, with notes.**

The split is grouped by region (16 regions, 3 repeats × 3 folds), tagged `UnseenGroup`, at leaf `L-PLACE.groups`. When I walk the tree myself I reach the same leaf, and the folds pass every check I ran. Nothing here needs a re-split. The four points below are notes for the curator, ranked by weight.

**Walking the tree (SPLIT-36)**

- The collection type is `Clinical Study`, per the record and SPLIT-34: trial patients, no date per row, `Time: Lost`.
- **[CLI.meets]:** the answer is "at another hospital or site", so the walk goes to the place step.
  - Lee et al. offer a risk model for patients at presentation, not one tied to the trial's own sites.
  - The only external validation on this file (Steyerberg and Vergouwe 2014) builds on the US patients and tests on the patients outside the US.
  - The rule "meets both another place and a later time → place step, the later time named untested" applies here.
- **[PLACE.several]:** yes.
  - `regl` holds 16 regions. I checked in the raw file that `grps` and `grpl` each nest inside exactly one region.
  - The enough-groups check passes: every test fold holds 5 or 6 whole regions and 793 to 1,119 deaths.
- So the leaf is **`L-PLACE.groups`**. It matches `split_leaf`, the `splits_comment`, `TimeBasis("UnseenGroup")` and the `Grouping` on `region`. It is not forced, and the leaf is already reached by gossis_icu_hospital_mortality and heart_disease. No question lacked a fitting answer.

**Collection facts against the source**

- `Samples: Over Time`, `Time: Lost`, `Target: Fixed Delay` (day 30) and non-recurring entities are all consistent with the file and the trial papers.
- No date and no enrolment order means there is no time key to rebuild. The time probe on frame order gives p = 0.67, and the raw rows are sorted by age.
- The outcome is fixed at day 30 and every row has it, so no label is still open at any cut.
- Each trial patient was enrolled once and the release has no patient id. The leftover copies are the imputation template (note 3), not repeat patients.

**Regime:** new patients at an unseen site, matching what is declared.

**The shipped folds (measured)**

| repeat-fold | train share | test rows | test deaths | test regions | US regions in test |
|---|---|---|---|---|---|
| 0-0 | 72.5% | 11,215 | 793 | 2, 6, 7, 13, 16 | 1 |
| 0-1 | 63.1% | 15,045 | 1,057 | 3, 5, 8, 9, 11, 15 | 3 |
| 0-2 | 64.3% | 14,566 | 1,001 | 1, 4, 10, 12, 14 | 4 |
| 1-0 | 68.4% | 12,885 | 916 | 7, 11, 14, 15, 16 | 4 |
| 1-1 | 61.8% | 15,610 | 1,119 | 2, 3, 4, 8, 9, 10 | 2 |
| 1-2 | 69.8% | 12,331 | 816 | 1, 5, 6, 12, 13 | 2 |
| 2-0 | 65.6% | 14,045 | 929 | 1, 4, 8, 10, 12 | 3 |
| 2-1 | 62.4% | 15,341 | 1,118 | 5, 7, 9, 11, 14, 16 | 4 |
| 2-2 | 72.0% | 11,440 | 804 | 2, 3, 6, 13, 15 | 1 |

- Regions are fairly alike. The death rate runs from 5.3% to 8.4%, and the tPA share is 25% in every region, as randomisation would give.
- Scores barely move across splits (builder's experiments and the group probe, untuned):

| split | LightGBM ROC AUC | logistic regression ROC AUC |
|---|---|---|
| grouped by region | 0.821–0.824 | 0.820 |
| random | 0.820–0.824 | 0.821 |
| `grpl` (48 groups) | 0.825 | 0.821 |
| `grps` (121 groups) | 0.823 | 0.821 |
| US → non-US and back (two folds) | 0.815 | 0.820 |

- `groups_not_clustered` agrees: 7.7% of nearest neighbours come from the row's own region, against 6.8% by chance. The grouping costs nothing, so I fitted no further alternative.

**Problems, ranked by `principles.md`**

1. **Weighed factor "Only a few groups" / warning `groups_test_groups_few`. Remedy: accept the warning; no change.**
   - Evidence: 16 regions give 5 or 6 per test fold. Each fold still scores 11,215 to 15,610 patients with 793 to 1,119 deaths.
   - Signal across regions is real: logistic regression 0.820, random forest 0.815, LightGBM 0.821.
   - This is not the covertype case (3 areas): with 5–6 regions per fold the test is not a domain shift between a handful of groups, and grouped and random score the same.
   - `grps` (121 groups) would clear the warning and scores the same. But it is a set of site clusters cut to at least 20 deaths each for validation studies, not a place a model meets, so the region is the more honest unit. Keep `regl`.

2. **The source's own split is not the shipped one (SPLIT-5 / SPLIT-19). Remedy: a sentence in the `splits_comment`.**
   - Steyerberg and Vergouwe validate US → non-US. The shipped folds mix the two: 1 to 4 US regions per test fold.
   - The `splits_comment` says the source split has two groups, too few for repeated folds. That is a valid reason under SPLIT-33. As a source-prescribed split that differs from the shipped one, it should be marked as a departure for the reviewer.
   - The cost of the departure is small: transfer from the US to elsewhere scores 0.815 (LightGBM) and 0.820 (logistic regression), close to the region split.
   - Suggested sentence: "the case study's US / non-US transfer scores 0.815–0.820, within the region folds' range, so the mixed folds lose nothing the source tested."

3. **Template copies cross regions (LEAK-19, near copies). Remedy: none (keep, as documented).**
   - After the drops, 24 rows of the 28-row imputation template share every input with another row. They span regions 4, 5, 6, 8, 9, 14 and 15, so some copies sit on both sides of a fold.
   - The label does not travel with the link: every set of copies holds both outcomes, for example [0, 0, 1] and [0, 1].
   - The link is between imputed values, not one patient seen twice (LEAK-42 / LEAK-43: the label does not follow the link, and there is no order). That is 0.06% of rows and has no effect on the score.

4. **Wording of the use case and time basis (USE-1, SPLIT-32). Remedy: a wording edit.**
   - The `use_case` ends "The model is built on patients of other regions." That writes the split into the use case. Lee et al.'s stated use is a risk estimate at presentation; the transfer to other regions comes from the validation study.
   - Suggested use case: "… used at hospitals other than those whose patients it was built on (the external validation of Steyerberg and Vergouwe 2014)."
   - The time basis says "a later period at a known region is not tested". It should also name, as the tree's both-place-and-later-time rule asks, that later patients in general are untested. That matters here because of the thrombolysis-era note in `fit_reason`.

**Checks that do not apply:** the temporal floor, the window count, the horizon / gap / newest-period checks and the `**Horizon:**` block, because the split is not temporal and the file has no time key. I ran no SPLIT-35 / hidden-group re-split beyond the builder's finer-group runs, because every grouping and random split score within 0.01 of each other.

</details>

<details><summary>Domain practitioner</summary>

**Fit: direct**, with two gaps. One row is one patient seen at the emergency door, before the clot-dissolving drug (the thrombolytic) is given. Every input kept in the file is known then, the 30-day death is what I would act on, and the regions held out stand for the new hospitals a risk score is taken to. The fit comes from USE-8: a trial selects its patients, but the setting this decision is made in selects the same ones, so the selection does not make the fit approximate. The metric scores my decision **partly**: I would choose by log loss, not ROC AUC.

**Speaking as the actor**
I am a cardiologist or emergency physician in 1990–1993, or today in a hospital with no catheter lab. A patient arrives with chest pain and ST elevation (a heart attack, STEMI), within 6 hours of the first symptoms. I decide which clot-dissolving drug to give, whether the patient goes to the coronary care unit or is transferred, and how hard to watch them. The trial's own aim for this model was choosing the therapy and the care resources (Lee et al. 1995).

**1. Inputs at the moment of the prediction.**

- **I have all the kept inputs.** I read age, sex, pulse, systolic pressure and Killip class (the bedside grade of heart failure) at the door. The infarct's location and the number of ECG leads with ST elevation come from the first ECG. I take the history in a few minutes. I know the weight, because accelerated tPA is dosed by weight; height is often only estimated. I know the drug arm when I decide.
- **The time to relief of chest pain is rightly dropped (USE-3).** The randomised arm changes it (p = 3e-11), so it is measured after the drug starts working.
- **I would always have the time since symptom onset, and the file lacks it.** I ask every patient when the pain began. It sets both the risk and the benefit of thrombolysis, and Lee et al. list "time to treatment" among the model's predictors (Lee et al. abstract, via the search snippets). The file holds no such column. The dropped time-to-relief column cannot be it: 64.9% "over 1 h" does not fit an onset-to-treatment time whose median is about 3 h, and that column differs by arm.
  - This is a missing input, not a leak.
  - It shrinks the task a little: in Lee et al. it is a minor predictor next to the five main ones.
  - The README's "as in the source's model" (in `fit_reason`) overstates it. It should say the file lacks the source's time to treatment.
- **I would have more today.** Today I would also have creatinine, cardiac arrest at arrival and the troponin result, the inputs of the GRACE score. In 1990, with a door-to-needle target of about 30 minutes, creatinine was often not back in time. So for the thrombolysis-era decision this is no gap.

**2. The target.**

- **Death within 30 days is what I act on (USE-5).** It was the trial's own primary end point, not a proxy.
- **I want a calibrated probability, not a class.** The benefit of the stronger drug in absolute terms is roughly the baseline risk times the relative reduction. So a risk of 4% against 12% changes what I do, not only who ranks above whom.

**3. Row, unit and test data.**

- **One row is one patient and one decision (USE-11).** No patient recurs.
- **Holding out whole regions mirrors taking the model to another country or hospital system.** It generalises the study design of the one paper that analyses this file, Steyerberg and Vergouwe 2014, which built on the US patients and validated outside the US.
- **The regions differ in their death rates** (I measured them): from 5.3% (region 13) to 8.4% (region 6). How well the predicted risk level carries over to a new region is part of the task.
- **The trial's selection matches the thrombolysis decision.** GUSTO-I excluded patients with a previous stroke, active bleeding, recent surgery, uncontrolled hypertension, or more than 6 hours since onset. Those are exactly the patients I would not give the drug to.
  - So for the use case as written the selection is shared, and the fit is direct (USE-8, selection paragraph).
  - It would not be shared for triaging every heart-attack patient, including the other type of heart attack (NSTEMI), late arrivals and patients who cannot take the drug. Trial patients die less often than registry patients, so I would not use this model for all comers.
  - `fit_reason` and `use_case` should name the selection: "STEMI patients eligible for thrombolysis, within 6 h".
- **One small oddity:** `prevcvd` (previous cerebrovascular disease, 832 patients, 2.0%) is "yes" although previous stroke was an exclusion. It is probably TIA or a protocol deviation; this is a question for the column auditor, not a reason to reject.

**4. Would I use the model?**

- **Yes, within its era and population.**
- **I would trust it because:** it has 40,826 patients from a randomised trial with adjudicated 30-day deaths, the predictors are the bedside ones I already weigh, and its c statistic (ROC AUC) stays at 0.81 outside the US.
- **I would distrust it because of:**
  - the care of 1990–93 (primary angioplasty, stents and modern antiplatelet drugs have cut mortality since);
  - the single imputation of missing values, which the file cannot show;
  - the missing time since onset.
- **I would check the predicted risk level (calibration in the large) at my own site before relying on absolute risks.**

**Gaps, ranked by how much they change the task**

1. **Era of care.** For the decision "which thrombolytic" the fit is direct. For a modern risk triage the predicted risks are too high, while the ranking would largely survive. The `Outdated` note is enough (SEL-18); `fit_reason` already says it.
2. **The time since symptom onset is missing.** I always have it, and Lee et al. used it. The task is slightly weaker than the real decision. A note is enough, but correct "as in the source's model".
3. **The population is limited to thrombolysis-eligible STEMI within 6 h.** It is shared by the use case, so the fit stays direct (USE-8), but it should be named in `use_case` and `fit_reason`.
4. **The predicted risk level shifts between regions** (5.3% to 8.4% deaths). This is a property of the real task, not a defect. It is an argument for a calibration-aware metric (below).

**What a domain expert would change**

- Name the population (thrombolysis-eligible STEMI, within 6 h of onset, excluding previous stroke and bleeding risk) in `use_case` and `fit_reason`.
- Say that the source's time to treatment is not in the file, rather than "as in the source's model".
- Keep `tx` (the drug arm). It is randomised and known at the decision, and it lets the model give the risk under each drug, which is the trial's own use of the model.
- Score calibration (below).

**Metric: partly**

- **ROC AUC is the declared fallback (MET-8), and it is not wrong.** The case study reports the c statistic, which is ROC AUC.
- **But that paper scores calibration together with discrimination.** Steyerberg and Vergouwe report calibration in the large and the calibration slope next to the c statistic. Under MET-8, a source that scores calibration asked for probabilities.
- **My decision runs on the absolute risk.** The therapy choice depends on the absolute benefit, and triage on a risk level. Neither source fixes one threshold or a cost, so MET-6 and MET-7 do not apply, and a threshold metric would be wrong.
- **The region shifts make calibration on unseen sites part of the task**, and ROC AUC ignores them.
- **I would choose `log_loss`** (Brier score as the more readable alternative). It is a strictly proper rule (MET-8) and scores both how well the model ranks patients and how well its risks match the deaths.
- **The panel's own numbers point the same way** (issues/mic.md, random and site-grouped folds):
  - On ROC AUC, LightGBM and logistic regression are tied: 0.826 against 0.826, LightGBM ahead on 5 to 9 of 15 folds.
  - On log loss they separate: regression with splines is ahead on 13–14 of 15 folds (0.1985), LightGBM 0.2010.
  - So log loss also helps against the `no_spread` flag without changing the task (MET-10: resolution; diversity).
- **This is the curator's call, not a defect.** `roc_auc` is defensible under MET-5 and MET-8, and the definition already names log loss as the alternative.

**Rules cited**
USE-1, USE-3, USE-5, USE-8 (and its selection paragraph), USE-11, SEL-18, MET-5, MET-6, MET-7, MET-8, MET-10.

**Sources**

- The definition, the record's 2026-11-25 screening block, issues/mic.md, and my own death rates by region and arm computed from gusto.csv.
- Lee et al. 1995, abstract: [PubMed 7882472](https://pubmed.ncbi.nlm.nih.gov/7882472/), [Duke Scholars](https://scholars.duke.edu/publication/694676). It lists "time to treatment", height and weight among the predictors.
- GUSTO-I design and exclusions: [ACC trial summary](https://www.acc.org/latest-in-cardiology/clinical-trials/2010/02/23/19/06/gusto1), [Erasmus repository, time from symptom onset (1996)](https://repub.eur.nl/pub/5525/TimefromSymptom_1996.pdf).
- Steyerberg and Vergouwe 2014: [PMC4155437](https://pmc.ncbi.nlm.nih.gov/articles/PMC4155437). It is the case study on this file, scores it by the c statistic plus calibration, and itself calls the data "likely outdated".

</details>

<details><summary>Precedent check</summary>

**Precedent check: gusto_i_mi_mortality (2026-11-25)**

I found three departures. Two of them need the curator to decide.

1. **The five derived flags were dropped under a rule that does not cover them.** CLEAN-5 only covers exact copies, and two earlier datasets kept columns of the same kind.
2. **The fold layout over the 16 regions sits between two recent calls of Andrej's** that went different ways.
3. **The record is missing the `Outdated` marker.** The screening, the mic item and every earlier case of a dated treatment era carry it.

Everything else follows precedent (table at the end). The register's flags do not apply here:
- **TP-3 drift:** the 2026-11-11 exclude, early_stage_diabetes_risk_prediction, was retired for USE-2 (no decision is made from the inputs), not for spread. open_university_learning_analytics_dataset was retired as `Too Small` (Andrej, 2026-11-20).
- **USE-8 opposite outcomes:** none of those pairs is about the treatment era.

**Finding 1: derived flags dropped. Departs from precedent with no reason given (CLEAN-5, Should)**

**Consistency check (AI, 2026-11-25):** should `sho`, `hig`, `ant`, `hyp` and `hrt` be dropped, when expresso_churn_prediction kept `ARPU_SEGMENT` and 2_month_survival_rate_prediction kept `dzclass`, both recodes of another column?

* **Problem:**
  - The definition drops the five flags "that recode other columns (CLEAN-5)". CLEAN-5 reads "exact copies of another column".
  - None of the five is a copy:
    - `sho` collapses Killip class into two levels.
    - `ant` is one level of `miloc`.
    - `hig` combines two columns.
    - `hyp` and `hrt` are thresholds, and they are not even exact (5 and 8 patients sit at the cut).
  - Precedent:
    - Lennart, 2026-10-22, expresso_churn_prediction: "keep ARPU_SEGMENT as released (CLEAN-5 not triggered, as `dzclass`)". `ARPU_SEGMENT` is "REVENUE / 3 rounded in every row" (exact).
    - 2_month_survival_rate_prediction: "dzclass groups the eight dzgroup values into four classes; both are kept as in the source".
    - nhanes_dxa_body_fat, an AI draft of this same batch, keeps BMI "as released" next to weight and height.
  - CLEAN-22 (Must) lets a column leave only "for what they are (a leak, an identifier, a copy …)".
  - The effect is small: logistic regression ROC AUC +0.003 on 15 of 15 folds with the flags, LightGBM −0.001.
  - `tpa` is a different case. It relabels `tx` one-to-one, which follows kdd_cup_09_appetency (Andrej, 2026-11-11: columns that "relabel" another, dropped under CLEAN-5) and in_vehicle_coupon_recommendation (Andrej, 2026-11-10). Its drop stands.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | Drop them, recorded as an exception. The fact that would set this case apart: the flags are dichotomies of the source's simplified model, with cut points that may have been chosen on this same cohort (a pulse above 80 is not the usual tachycardia cut of 100), so they carry the authors' choices made on all rows | keeps the inputs to what was recorded at presentation | the fact is unverified (Lee et al.'s full text was not read), and Killip III–IV and systolic BP < 100 are standard clinical cuts |
  | b | Keep them as released, as for ARPU_SEGMENT and dzclass | follows two curator precedents and CLEAN-22's wording | the flags repeat information their source columns already hold |
  | c | Keep the drop and reopen expresso_churn_prediction and 2_month_survival_rate_prediction to match | one rule for all recodes | reopens settled datasets for a 0.003 effect |
  | d | Amend CLEAN-5 to cover deterministic recodings and coarsenings of a kept column | settles the question for good | changes a rule on the strength of one case |

* **Recommendation:** (b), unless the curator confirms the fact in (a). The drop as written stretches CLEAN-5 past its text, against two settled cases.

**Finding 2: 3×3 folds over 16 regions, next to Andrej's leave-one-country-out of 2026-11-24 (groups_test_groups_few; SPLIT protocol)**

**Consistency check (AI, 2026-11-25):** with 16 regions, should the warning be accepted with 3×3 folds, or should each region be held out once, as for economic_well_being_prediction_challenge?

* **Problem:**
  - The builder proposes to accept `groups_test_groups_few` with 3×3 folds of 5–6 regions each. The group probe supports it: LR 0.820, LightGBM 0.821.
  - The curators' calls on the same warning:

    | Case | Groups | Layout chosen | Who, date |
    |---|---|---|---|
    | economic_well_being_prediction_challenge | 18 countries (10 surveyed in 2014-2016) | leave one country out on those 10: "3x3 CV produces too similar splits" | Andrej, 2026-11-24 |
    | heart_disease | 3 hospitals | leave one hospital out | curator-accepted |
    | sat11_hand_algo_runtime | 32 families | 3×3 accepted | Andrej, 2026-11-23 |
    | huesken_sirna_efficacy | 30 genes | 3×3 accepted | Myunghwan, 2026-10-26; Lennart, 2026-11-04 |

  - 16 regions is closer to the 18 countries than to 30 or 32 groups.
  - The source's own validation is US → non-US (Steyerberg and Vergouwe 2014). The `regl` codes rebuild it exactly, much as economic_well_being followed the source's test design.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | 3×3, accepted. The fact that would set it apart: each region holds 1,231–4,352 patients and 95–294 deaths, so a test fold of 11k–16k patients is stable, unlike countries of a few hundred rows | protocol default; matches sat11 and huesken | repeats reshuffle the same 16 regions, the "too similar splits" Andrej named |
  | b | Leave one region out (16 folds, 1 repeat), as economic_well_being | every region tested once; distinct test sides | a protocol departure to accept (`splits_dimensions_off_protocol`) |
  | c | (a) or (b), plus the US → non-US split recorded as a check in the notes | ties the split to the source's validation | two groups cannot be the shipped split |

* **Recommendation:** for the curator to weigh. (a) is defensible with the stated fact. (b) follows Andrej's most recent reasoning. Either way, add the accepted warning to `accepted_check_warnings` (it is not in dataset.py yet).

**Finding 3: `Outdated` marker missing (SEL-18, Should)**

**Consistency check (AI, 2026-11-25):** should the record carry `Outdated`, as the earlier cases of a dated treatment era do?

* **Problem:**
  - The 2026-11-25 screening and the mic item call the thrombolysis era an "`Outdated` note under SEL-18", and the fit_reason says so too. The record's tags lack the marker.
  - The marker is on:
    - cirrhosis_patient_survival_prediction (Andrej, 2026-10-15: "marker `Outdated` added", a trial arm and a treatment era since replaced);
    - 2_month_survival_rate_prediction (care of 1989–1994);
    - protein_model_quality_rf_pcp (Lennart, 2026-11-04 and 11-05).
* **Options:** (a) add `Outdated` as a note on a kept dataset; (b) leave it off and name the fact that sets GUSTO apart (none found).
* **Recommendation:** (a). It is the curator's to set, as in every precedent.

On the fit: `direct` follows the written USE-8 case row, "The era alone stays direct (2_month_survival_rate_prediction, …)" (Lennart, 2026-10-27). cirrhosis_patient_survival_prediction was set `approximate` with only the era in its fit_reason (Andrej, 2026-11-05), although an input of its own (Stage, a liver biopsy rarely taken today) could carry it under the heart_disease row. GUSTO has no such input: every input is recorded at presentation today, and fibrinolysis remains therapy where primary PCI cannot be done in time. So GUSTO is consistent with the written row. The cirrhosis/2_month pair is the inconsistency, and it is worth a separate cross-dataset item, not an issue here.

**Consistent with precedent**

| Decision | Follows |
|---|---|
| `ttr` dropped: the arm changes it (p = 3e-11), so it is recorded after presentation | USE-3 (Must); the Tensions row "a real task against a leak" (kickstarter's `staff_pick`); crash2_trauma_early_death and aids_clinical_trials_group_175 screenings (post-baseline columns out). The case-study models' use of it does not override the prediction point |
| `tx` (randomised arm) kept as input | cirrhosis_patient_survival_prediction `Drug` kept, the arm of a superseded trial (Andrej, 2026-10-15) |
| `tpa` dropped | kdd_cup_09_appetency (Andrej, 2026-11-11), in_vehicle_coupon_recommendation (Andrej, 2026-11-10) |
| 4 exact raw copies dropped; 8 rows that match only after the site groups are dropped kept | LEAK-19; hiva_agnostic (distinct units that the inputs cannot tell apart stay) |
| Split leaf L-PLACE.groups by region; `grpl`/`grps` unused | leaf examples gossis_icu_hospital_mortality and heart_disease |
| Metric: `roc_auc` fallback (the case study reports c statistic plus calibration) | MET-5, gallstone_disease (multi-metric papers go to the fallback, Lennart, 2026-10-21); heart_disease_* `roc_auc` not `log_loss` (Lennart, 2026-10-21) |
| `no_spread` kept, re-check with tuned results | TP-3 cases (amex_non_iid_1m: a large, low-noise task where strong methods converge; open_university_learning_analytics_dataset "pending tuned results") |
| Not `Trivial` | TP-4: TIMI 0.794 against 0.826 for the methods. Contrast ljubljana_breast_cancer (the rule matched the methods) and sepsis_survival_minimal_clinical_records (+0.0012, retired under step 2) |
| Built next to mic, not instead of it | PROV-4 and the mic item's option B |

No drift by one curator on these rules, and no third exception of one kind, came up.

Rules: CLEAN-5, CLEAN-22, CLEAN-19, SEL-18, USE-3, USE-8, LEAK-19, MET-5, TP-3, TP-4, PROV-4.

</details>

<details><summary>Blind review</summary>

I'd include this dataset, with small changes: it is a real, well-known prediction task with honest features and a fair grouped split. Its limits are little room between methods, wide public exposure, and a few dozen bad rows.

**What the task is.** GUSTO-I was a randomised trial of clot-busting treatment in about 41,000 heart-attack patients across many countries (NEJM 1993). The task is to predict death within 30 days from what is known when the patient is admitted and randomised: age, Killip class, blood pressure, pulse, infarct location, history, and the treatment arm. This is a real use: it is the basis of the GUSTO and TIMI-style risk models doctors use to triage patients and choose how hard to treat them. Steyerberg's textbook uses this exact data as its standard example for building clinical prediction models.

**Is the evaluation honest?** Every feature is a baseline measurement taken at admission. The treatment (`tx`) is assigned by randomisation at that same moment, so no column comes from after the prediction. Holding out whole regions is a sensible test of whether a model transfers to a new place:
* There are 16 regions, with 1,231 to 4,352 rows each.
* The death rate varies only from 5.3% to 8.4% between regions, so the region folds are stable.

**Signal.**

* Death rate is 6.98% (2,851 deaths), which is enough to score.
* With region-grouped 3-fold splits, LightGBM reaches AUC 0.826–0.830 and plain logistic regression 0.818–0.823. Age plus Killip class alone gives about 0.78.
* Effect directions match the literature. Death rate by Killip class is 5.1% (I), 13.9% (II), 32.8% (III) and 57.8% (IV); older age, lower blood pressure and higher pulse all raise risk.

**Concerns, most serious first**

1. **Little room to separate methods, and the data is widely seen.** Gradient boosting beats logistic regression by less than 0.01 AUC. The risk is close to additive in a few variables, so most methods will tie. The data is also a textbook dataset published in R packages, so pretrained or prior-based methods may have seen it.
   * Change: keep it, but score with log-loss or Brier score as well as AUC, since how well predicted risks match real death rates is what matters clinically. Treat it as a well-specified, low-headroom task.

2. **A handful of junk records.**
   * About 25 rows fall into two tight clusters. One has pulse 53, systolic BP 97, ST elevation 2, about 31 years old, about 190 cm. The other has pulse 53, BP 104, about 40 years old. Within each cluster, age, height and weight differ only slightly (for example age 31.102, 31.547 or 31.859). These rows are spread across several regions and treatment arms, and their outcomes conflict.
   * 8 rows are exact duplicates, some of them in different regions, so they would appear in both train and test.
   * These look like placeholder or test records, not patients.
   * Change: drop both clusters and the exact duplicates.

3. **Some impossible values.** Pulse is 0 in 4 rows and systolic BP is 0 in 6 (57 rows are below 60). Age reaches 110 in 3 rows; the youngest patient is 19.03.
   * Change: set pulse or BP of 0 to missing, and set ages above about 100 to missing (or drop those rows).

4. **The diabetes column needs a check against the codebook.** The diabetes split (`dia`: 34,821 no / 6,005 yes) exactly equals Killip I versus Killip II–IV (34,821 / 6,005).
   * Row by row the two are different (only 911 + 168 + 77 of the Killip II–IV patients are diabetic), and diabetes has a plausible effect: 10.9% versus 6.3% death rate.
   * So it is probably a coincidence, but an exact match is unusual. The predtools source defines `dia` only as "whether the patient had diabetes".
   * Change: confirm the column against the original codebook.

5. **Smaller preparation points.**
   * The source has 40,830 rows; this table has 40,826. The 4 dropped rows are not documented.
   * The source has 29 variables and the table keeps 19 predictors. The ones dropped (for example `sho` (shock), `hig`, `hrt`) look redundant or left out on purpose, which is fine, but say so.
   * Region is stored as an integer (correct for grouping) and is rightly not used as a feature.
   * Category types and encodings are sensible, and nothing is missing.
   * `task.md` names no training weight, so there was nothing to judge there.

**What I could not check**

* The hbiostat data page and codebook: the page came back empty when fetched. So I could not confirm the variable definitions (`ste`, `pan`, `fam`, region codes) or the diabetes/Killip question.
* Whether "anonymized" (the predtools wording) means values were perturbed. The 3-decimal ages hint at it.
* The PMC and NEJM papers. I relied on my own knowledge of GUSTO-I and its published model (C-statistic about 0.81–0.84), which matches what I found.

</details>

<details><summary>Task gamer</summary>

**GUSTO-I 30-day mortality: how far the task can be gamed**

**Verdict:** only a little. One recording artefact is worth about +0.007 AUC. Missing heights and weights were filled in by imputation, and the filled-in values have a different decimal format, so the model can tell which patients were never measured. I found no copies across the split, no order leak, no column recorded after admission and no lookup that recovers the label.

Reference models, scored on the 9 shipped splits:
- **Baseline:** untuned LightGBM on `features()`, AUC **0.8209** (range 0.810–0.829).
- **Better honest model:** a lightly tuned LightGBM (400 trees, learning rate 0.02, 8 leaves, at least 50 rows per leaf), AUC **0.8271** (range 0.814–0.836). All gains below are measured against this one.
- **Noise:** adding a column of random numbers to the tuned model gives 0.8267–0.8268, so the noise is about ±0.0005.

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | "Imputed" flag for height and weight: the value is neither a whole cm or kg nor a converted inch or pound value | `work/imputed.py`, `work/final.py` | 0.8271 | 0.8342 (flags added)<br>0.8352 (flags, counts and formats together) | +0.007 (+0.005 to +0.009), about 14× noise | Uncertain. It knows a measurement is missing only if height and weight were taken at admission (see below) | Ship the missingness openly, or round the imputed values onto the measured grid, or drop the imputed rows' values |
| 2 | How often each height value occurs (rare heights are the imputed ones) | `work/counts.py`, `work/final.py` | 0.8271 | 0.8350 (all rows)<br>0.8351 (training rows only) | +0.008 (+0.006 to +0.011) | Same as #1: it is the same signal. Counting over test rows adds nothing | Same as #1 |
| 3 | Unit format of height and weight: whole cm or kg versus a value converted from inches or pounds | `work/formats.py`, `work/final.py` | 0.8271 | 0.8285 | +0.0014 (+0.0002 to +0.0027), about 3× noise | Yes. It mostly identifies country or site, and a hospital knows its own units | Not needed. Rounding to whole cm and kg would remove it |

No flaw that hurts an honest model was found (see the checks under the findings).

**Findings**

**1 and 2: the imputed-measurement flag**

- **How the values were made.** The published `gusto.rda` has 40,830 rows and no missing values; the kit keeps 40,826. About 12% of heights are not on a 1 cm grid, and not on the grid of inches converted to cm (rounded or truncated to 0.1 cm). Examples: 171.3, 172.2 and a lump of 957 rows at 177.3. These values look like regression imputation: from sex, weight and the other columns they are predicted with R² 0.76, against 0.52 for measured heights.
- **The mortality gap.** Patients with an imputed height die within 30 days at 14.3%, against 6.0% for the others. The gap holds inside each region: for example 17.1% vs 5.5% in region 2 and 14.6% vs 5.4% in region 12. For weight the rates are 8.7% vs 6.8%.
- **The imputed values themselves do not leak the label.** Within the imputed rows, adding the outcome to a regression of height on the other columns gives t = −0.1. So the only information is the flag.
- **Is it an exploit?** The flag stands for "height or weight was not recorded". A model at the admission desk would know that only if these measurements were taken at enrolment. If the case report form was completed later, and early deaths were simply never measured, the flag uses information from after admission. The deciding fact is when GUSTO collected height and weight, and I could not find it.
- **An honest variant.** Turning the imputed values into missing values (NaN) scores 0.8325, so most of the gain comes from knowing that a value is missing.
- **Fix.** Either ship an explicit missingness indicator, if the measurement really was taken at admission, or put imputed values on the same grid as measured ones so they cannot be told apart.

**3: units**

- Whole-cm heights are 98% of rows in some regions (5, 6, 8) and about 40% in others (7, 9). This is country or site practice, not the patient's condition.
- Within a region, rows on the inch grid have about the same mortality as whole-cm rows. The small gain is a proxy for region, and the model is not allowed to use region directly. It is minor, and a deployed model would know its own site's units anyway.

**Attacks that found nothing**

- **Row order:** the label against row position has correlation 0.004. Neighbouring rows agree 0.8698 of the time, against 0.8701 expected by chance. Kit order is unrelated to source order (correlation −0.003).
- **Copies across the split:** 17 rows have exact feature copies, in clusters inside the source file (shared pulse 53, systolic BP 97 and height, with ages close together). Labels within these clusters disagree. Using the label of the nearest training row as the prediction gives AUC 0.56–0.58, far worse than the model.
- **Counts over all rows:** for age, weight, pulse and blood pressure the score stays at 0.8267–0.8274, within noise. Counts of age values computed from training rows only also give 0.8271.
- **Other formats:**
  - Age decimals and last digits show no pattern.
  - `ste`, pulse and blood pressure are whole numbers with no format signal.
  - There are a few sentinel-like values: pulse 0 (4 rows, 3 deaths), systolic BP 0 (6 rows, all dead), and age 108 or 110 (3 rows). They are too few to matter, and a pulse or blood pressure of 0 at admission is real information.
  - Format features alone give AUC 0.580, which is the imputation flag again.
- **Train versus test classifier:** AUC 0.57–0.67. This is the regional shift in units, not anything label-related.
- **Columns from after admission:** none found. The kit dropped the source's derived columns (`sho`, `hig`, `hyp`, `hrt`, `ttr`, `ant`), the hospital-group columns (`grpl`, `grps`) and `tpa`. The treatment `tx` is randomised at enrolment.
- **Transforms over all rows:** none. Values are on raw scales.
- **The metric:** AUC is pooled over all test rows. Region death rates range from 5.3% to 8.4%, but region cannot be recovered from the features except weakly through units (#3).
- **Flaws that hurt an honest model:** none found. The grouped split has no training rows a deployed model would not see, and the 4 rows dropped from the source were all in the near-duplicate clusters.

**What I could not check**

- When GUSTO-I measured height and weight relative to enrolment. This decides whether #1 is a leak or a legitimate missingness signal.
- How the published file was imputed (method, and whether the outcome was used). The rows show no dependence on the outcome, but I found no documentation.
- Looking up rows in the published file works: 40,826 of 40,826 rows match, and the labels agree on 99.98%. That is not a flaw of the task.
- I found no competition forum or leak write-up for this dataset; it is a teaching dataset for clinical prediction models.

Sources:
- [hbiostat GUSTO data](https://hbiostat.org/data/repo/gusto.rda)
- [predtools gusto.R](https://github.com/resplab/predtools/blob/master/R/gusto.R)
- [mice-ext-val gusto](https://metodologianavarrabiomed.github.io/mice-ext-val/reference/gusto.html)
- [arXiv 2608.01333](https://arxiv.org/pdf/2608.01333)

</details>

<details><summary>Advocate</summary>

I recommend shipping `gusto_i_mi_mortality` after one Must fix: drop `height`. The evidence agents found a real leak there, and the dataset has no defect that the remedy ladder can't fix.

**My own measurement**: the 9 shipped region folds, with `height` dropped.

| Model | ROC AUC | log loss | Against plain logistic regression |
|---|---|---|---|
| logistic regression | 0.8202 | 0.2023 | – |
| logistic regression with splines | 0.8262 | 0.2002 | +0.0059 AUC (standard error 0.0009), better on 9 of 9 folds; log loss better on 9 of 9 |
| LightGBM, lightly tuned (the task-gamer's settings) | 0.8262 | 0.2006 | +0.0060 AUC (standard error 0.0009), better on 9 of 9; log loss better on 9 of 9 |
| LightGBM, defaults | 0.8187 | 0.2045 | −0.0015 AUC, better on 1 of 9; log loss worse on 9 of 9 |

**Opening brief**

**1. The task is real and the data fits it directly (P3; USE-8 Must, USE-5).**

- The domain practitioner rates the fit "direct". Every kept input is known at the emergency door. Death by day 30 was the trial's own primary end point.
- The trial's selection (heart attacks with ST elevation, within 6 hours, eligible for the clot-dissolving drug) is the same population this decision is made for. Under USE-8 that keeps the fit direct.
- The blind reviewer, who saw none of our notes, also says include: "a real, well-known prediction task with honest features and a fair grouped split."
- **The era objection** is a note, not an exclusion. SEL-18 (Should) excludes only when the task is gone, and clot-dissolving drugs are still used where primary angioplasty can't be done in time.
- **Concede:** the record should carry the `Outdated` marker, as cirrhosis, 2_month_survival and protein_model_quality do (precedent checker, finding 3).
- P3 outranks every quality objection below. The Tensions row "a real task against imperfect cleaning" says keep the task and fix what is cheap.

**2. Every kept input except `height` is known at presentation, shown by a test on the data (P4; USE-3, LEAK-1 Must).**

- Randomisation gives a decisive test: a column measured after treatment differs between the trial arms.
  - Every kept column is balanced across the arms (p ≥ 0.087).
  - `ttr` (time to relief of chest pain) is not (p = 2.7e-11), and the definition drops it. The claim auditor reproduced this.
- **Concede the column auditor's finding:** the values filled in for missing heights are tied to death.
  - 2,132 filled heights (5.2% of rows) have 19.9% deaths against about 6% for the rest.
  - The odds ratio is 2.65 (p = 2e-54) after adjusting for the presentation inputs and region, and the gap holds in 15 of 16 regions.
  - This is the LEAK-10 (Must) mechanism: missingness that encodes the outcome. Precedent: expresso_churn_prediction's REGION and kick's WheelType were dropped on the same kind of conditional test.
- **Mildest remedy that resolves it:** drop `height` (fix the definition, the second rung of the ladder).
  - It costs logistic regression nothing (+0.0001). LightGBM loses only the 0.002 it was taking from the fill pattern.
  - Setting the fills to missing doesn't work: the missingness carries the same signal.
  - The fills in `weight` show no outcome signal (adjusted p = 0.99), so `weight` stays.
- The Tensions row "a real task against a leak" applies: fix the leak and keep the task.

**3. The split follows the application and passes every check (P4; L-PLACE.groups).**

- The split auditor walked the decision tree on its own and reached the same leaf: whole regions held out, 5 or 6 of the 16 per test fold, with no region on both sides.
- Each test fold holds 11,215 to 15,610 patients and 793 to 1,119 deaths.
- Grouped and random folds score alike (logistic regression 0.820 against 0.821). The source's own test, training on the US and testing elsewhere, scores 0.815 to 0.820, inside the region folds' range.
- **Fold layout:** the precedent checker asks whether to use 3×3 folds or leave one region out (as for economic_well_being, 18 countries). What sets this case apart: each region holds 95 to 294 deaths, so a fold of 5 or 6 regions is stable. The precedents with that kind of fold size are sat11 (32 groups) and huesken (30), both accepted at 3×3.
- **Concede the process gap:** the warning `groups_test_groups_few` is accepted in the builder's report but not in `dataset.py`. Add it to `accepted_check_warnings` with the group probe's numbers, and add one sentence on the US to non-US check to `splits_comment`.

**4. The task is worth benchmarking: methods separate, consistently (P6; TP-3 and TP-4 Must, TP-2).**

- The `no_spread` flag doesn't describe what my folds show (table above). Tuned gradient boosting and a regression with splines both beat plain logistic regression by about 0.006 AUC on 9 of 9 folds, about 6.5 standard errors. Default LightGBM trails.
- So the task rewards a model that captures smooth effects and is tuned properly. That is a real distinction between methods.
- **Concede:** the gap is under 0.01 in absolute terms. The `no_spread` definition reads as having a 0.01 alternative criterion, so the flag may stand on that reading. The evidence table lists "strong methods converge on a large, low-noise dataset" (amex) as a kept case, and TP-2 step 2 leaves any retirement to the curator.
- **Not trivial:** the TIMI score, a published score not fitted on these data, reaches 0.794. The methods are ahead, so TP-4's rule test is passed.
- At 40,826 patients this is the largest heart-attack death task open to us. It joins the benchmark next to `mic` (option B of the mic decision item, PROV-4), not instead of it.

**5. The data is what it claims to be (P5).**

- The claim auditor tested about 30 claims. None that bears on validity or value was refuted, and the definition's numbers reproduce exactly. In particular:
  - the US regions are the only set of 8 regions that matches both the paper's patient count (23,034) and its deaths (1,565);
  - death rates by arm match the NEJM 1993 trial;
  - region 1 matches the published West-region table;
  - the reading "2 means yes" for `prevcvd` and `prevcabg` holds on a decisive test.
- The open permission is quoted from the repository's page.
- The 28 "template" rows are 0.07% of the data. Their labels disagree within each cluster, and copying the nearest training row's label scores only 0.56 to 0.58 AUC. Keeping them with a note follows LEAK-19 and the hiva precedent.
- **Concede (P7, CLEAN-11, cheap):**
  - Three Killip class I patients with a pulse or blood pressure of 0, and pulse values of 1 to 9 alongside a measured pressure, are missing values written as 0. Set them to missing (8 cells at most).
  - Reword "mostly Killip IV".
- The blind reviewer's point that the `dia` counts equal the Killip I split is a coincidence. The two differ row by row, and the diabetes share (14.7%) matches the trial.

**6. The metric follows the rules (P6; MET-5 and MET-8 Should).**

- The case study reports four measures and names none as the criterion, so MET-5 sends the task to the fallback, `roc_auc` for a binary task. That matches the heart_disease and gallstone_disease precedents.
- The domain practitioner's case for log loss is legitimate: the source scores calibration, and MET-8 says such a source "asked for probabilities". Log loss also resolves the methods, 9 of 9 folds in my run.
- Either metric is within the rules. Under MET-10 this is the curator's call, not a defect, and the definition already names log loss as the alternative.

**7. The remaining objections are about quality or wording; none blocks shipping (P7).**

- **The five dropped flags** (`sho`, `hig`, `ant`, `hyp`, `hrt`):
  - **Concede:** CLEAN-5 covers exact copies only, and expresso's ARPU_SEGMENT and 2_month_survival's dzclass were kept.
  - The mildest choice: keep them as released, unless the curator records as an exception that the cut points are the source's choices on this cohort (a pulse above 80 is not the usual threshold).
  - The effect is at most 0.003 either way. It is a quality question and cannot outrank anything above.
- **Wording fixes:**
  - say 40,826 patients, not 40,830;
  - name the population (ST elevation, thrombolysis-eligible, within 6 hours) in `use_case` and `fit_reason`;
  - replace "as in the source's model" with a note that the source's time to treatment is not in the file;
  - stop the use case from stating the split.
- Independent failures are not conflicts: each of these is fixed on its own rung of the ladder, and none of them is a Must left standing.

**Verdict:** ship after changes. `height` dropped (LEAK-10), `Outdated` marker added, the warning accepted in `dataset.py`, the zeros of Killip I patients set to missing, and the wording fixes. Two calls for the curator: `roc_auc` or `log_loss`, and whether to keep the five flags.

</details>

<details><summary>Advocate rebuttal</summary>

**Rebuttal: the advocate, `gusto_i_mi_mortality`**

The critic and I agree on the verdict ("ship after changes"), on the one Must fix (drop `height`) and on most of the smaller fixes. We disagree on three things: the metric, whether TP-3 is still open, and the fold layout.

**1. `height` must go (LEAK-10 via LEAK-38, Must): concede, we already agree.**

- The critic's rounding test adds a fact I did not have. After rounding to whole centimetres, a model still finds the filled rows at AUC 0.82. So LEAK-13 harmonisation cannot fix this, and dropping the column is the mildest remedy that works.
- One correction to the critic's framing. With `height` dropped, the spread does not go away. In my run, tuned LightGBM and the spline regression still beat plain logistic regression by +0.006 AUC, on 9 of 9 folds. So the artefact does not "decide which method wins" once it is gone.

**2. Wording, population and `Outdated` (USE-8, SEL-18, Should): concede, both briefs ask for the same thing.**

- Name the population in `use_case` and `fit_reason`: STEMI, eligible for clot-dissolving treatment, within 6 hours.
- Replace "as in the source's model" with a note that the source's time to treatment is not in the file.
- Remove the split sentence from `use_case`.
- Add `Outdated` as a note. The fit stays direct.

**3. The split's open calls: concede the recorded warning and the `splits_comment` sentence. On the layout, I dispute any lean toward leaving one region out.**

- Andrej left one country out for economic_well_being because only 10 countries were usable for testing. With 3×3 folds that is 3 or 4 countries per fold, and he wrote that "3x3 CV produces too similar splits" (precedent checker, table row).
- Here all 16 regions are tested, 5 or 6 per fold. Each test fold holds 793 to 1,119 deaths, and each region alone holds only 95 to 294. Leaving one region out would give 16 test sides with as few as 95 deaths each. That is a noisier AUC per fold, and it is a protocol departure (`splits_dimensions_off_protocol`) that 3×3 avoids.
- The groups-per-fold precedents are sat11 (32 groups) and huesken (30), both accepted at 3×3.
- It stays the curator's call, but the evidence favours 3×3.

**4. Metric (MET-8, Should): partly concede.**

- I agree the critic's case for `log_loss` is about fidelity, not about separating methods. The source scores calibration, and the clinician acts on absolute risk across regions whose death rates run from 5.3% to 8.4%. That is a sound reading of MET-8 ("asked for probabilities").
- What I dispute is that `roc_auc` "ignores" a rule. The source names four measures with no single criterion, so MET-5's fallback is also within the rules, and so are the heart_disease and gallstone precedents.
- Under MET-10 this is a weighing call, not a defect. If the curator weighs the decision (absolute risk) above consistency with the precedents, `log_loss` is the better fit, and I would not oppose it. It also resolves the methods on 9 of 9 folds, so nothing is lost either way.

**5. TP-3 "still open, no tuned results exist": dispute, a new fact came up.**

- Tuned results exist, with `height` already dropped (table in my brief):
  - tuned LightGBM 0.8262 and spline logistic regression 0.8262, against 0.8202 for plain logistic regression;
  - +0.006 AUC with a standard error of 0.0009, better on 9 of 9 folds;
  - log loss also better on 9 of 9 folds.
- The re-check the critic asks for has been run, and it shows consistent separation.
- What stays open is only whether a gap under 0.01 meets the `no_spread` definition's alternative criterion. I conceded that already. TP-2 step 2 leaves that call to the curator, and amex is the precedent for keeping such a task.

**6. The five flags (CLEAN-22, CLEAN-5): concede.**

- Keep them as released, unless the curator records an exception: the cut points were the source's choices, possibly made on this same cohort.
- My brief said the same. The critic's facts on the thresholds (5 and 8 patients sit at the cut) strengthen the case for keeping them.

**7. Impossible values and wrong notes (CLEAN-11, Should): concede the pulse and pressure fixes, the note and the count. On the ages, I agree with the critic's own remedy: a question, not a fix.**

- Set to missing: pulse 1 to 9, and pulse or pressure of 0 in patients not in shock.
- Fix the "mostly Killip IV" note and the count (40,826).
- The ages 108, 108 and 110 are odd because they are whole numbers. The column auditor calls them "unusual rather than impossible", and three rows cannot move a score. So document them and leave them as they are, with no change to the definition.

**Net:** apart from point 5, nothing is actually in dispute. That one is answered by the tuned run, which has now been done. The changes to make:
- drop `height`;
- add the `Outdated` note;
- the wording fixes;
- record the accepted warning in `dataset.py`, and add the US to non-US sentence to `splits_comment`;
- set the impossible zeros and pulses to missing;
- keep the five flags.

Three calls go to the curator: `roc_auc` or `log_loss` (log loss is defensible), 3×3 folds or leave one region out (I recommend 3×3), and whether a gap of 0.006 on 9 of 9 folds counts as spread.

</details>

<details><summary>Critic</summary>

I'm opposing `gusto_i_mi_mortality` as defined. Shipping should wait on one validity fix (point 1) and a handful of smaller changes. None of the points calls for excluding the task, which is real and well matched to its source.

I checked one thing myself: whether rounding the heights would fix point 1.

**Opening brief: the critic, `gusto_i_mi_mortality`**

**1. The filled-in heights flag patients who die. `height` must go (LEAK-10, Must, via LEAK-38's conditional-test clause; LEAK-13, Must).**

- **Problem:** the source says missing predictor values were filled by "a single imputation procedure" (Steyerberg and Vergouwe 2014). It does not say whether the outcome was used. The filled heights can be spotted by their decimals:
  - 2,132 heights (5.2%) are neither whole or half centimetres nor converted inches. 19.9% of these patients died, against 6.3% of the others.
  - The gap holds in 15 of 16 regions.
  - It survives adjustment for everything known at presentation (age, sex, Killip class, blood pressure, pulse, infarct location, ST leads, previous MI, region): odds ratio 2.65, p = 2e-54 (column auditor).
  - Killip class barely differs between the two groups, so "too sick to measure at the door" does not explain the gap.
- **Effect on the task:** a model that learns which heights are filled gains +0.0045 ROC AUC (LightGBM, better on 9 of 9 folds). A regression with a fill flag gains +0.0066, and the task gamer measured +0.007, about 14 times the noise. That is more than the 0.003 for which `ttr` was dropped under LEAK-1. It is also more than the whole LightGBM-over-logistic-regression gap (+0.0035), so under `no_spread` this artefact would decide which method wins.
- **The rule:** LEAK-38 says that when a conditional test shows a field's missingness or fill differs by outcome given what is known at the prediction point, LEAK-10 applies and the field is dropped. This test does exactly that.
- **Milder fixes don't work:**
  - Setting the fills to missing keeps the signal (0.8317). LEAK-40 says so too: "no fix when the gaps follow the classes".
  - I tested harmonising the precision (LEAK-13: height and weight rounded to whole cm and kg). It hides the decimals, but a model still finds the filled rows with AUC 0.82 (0.98 before rounding), because regression fills sit on the line the imputation predicted.
- **Remedy:** drop `height`. It costs logistic regression +0.0001 (nothing) and tuned LightGBM −0.0009, which is mostly the leak itself. Add a note on the mechanism. Lee et al.'s height effect may partly reflect the same fills.

**2. The use case and fit overstate how closely the file matches the source's model (USE-8 and SEL-18, Should).**

- **Problem:**
  - `fit_reason` says "as in the source's model", but the file lacks Lee et al.'s time to treatment, an input the clinician always has (domain practitioner).
  - The population is not named: thrombolysis-eligible STEMI within 6 h, with previous stroke and bleeding risk excluded.
  - `use_case` ends with the split ("built on patients of other regions"). That sentence describes the split, not the use case (split auditor).
  - The record lacks the `Outdated` marker, which the screening, the mic item and the precedents on dated treatment eras all carry (cirrhosis, 2_month_survival).
- **Effect:** the fit stays direct, but a reader is told the task is more complete and more general than it is.
- **Remedy:** reword `fit_reason` and `use_case` along those lines and add `Outdated` as a note. The fit stays direct.

**3. The split's open calls are not recorded (house rule on check warnings; SPLIT protocol).**

- **Problem:**
  - `groups_test_groups_few` is reported as accepted, but `dataset.py` has no `accepted_check_warnings` entry (claim auditor #18).
  - With 16 regions, the fold layout sits between two recent calls of Andrej's:
    - economic_well_being_prediction_challenge, 18 countries: leave one country out, since "3x3 CV produces too similar splits" (2026-11-24);
    - sat11_hand_algo_runtime, 32 families: 3×3 folds accepted.
  - The source's own US → non-US validation is not mentioned as a departure (split auditor).
- **Remedy:**
  - Add the accepted warning with its numbers: LR 0.820 and LightGBM 0.821 across regions; each test fold holds 11,215 to 15,610 patients and 793 to 1,119 deaths.
  - Put the layout to the curator: 3×3, or leave one region out.
  - Add one sentence to `splits_comment`: the US → non-US transfer scores 0.815 to 0.820, inside the range of the region folds.

**4. The metric ignores the calibration the source scores and the decision runs on (MET-8, Should).**

- **Problem:**
  - The case study on this file scores the c statistic *together with* calibration in the large and the calibration slope. MET-8: "a source that scores calibration … asked for probabilities".
  - The clinician acts on the absolute risk: the benefit of the stronger drug is roughly the baseline risk times the relative reduction (domain practitioner).
  - Regional death rates vary from 5.3% to 8.4%, so carrying the risk level to an unseen region is part of the task, and ROC AUC cannot see it.
- **Remedy:** `log_loss` instead of the `roc_auc` fallback; the definition's own reason already names it as the alternative. I ask for this for fidelity to the source and the decision, not to make methods separate better.

**5. Whether the dataset is worth benchmarking is still open (TP-3, Must).**

- **Problem:** untuned linear, random forest and LightGBM models reach 0.819, 0.817 and 0.820. No tuned results exist. After the fix in point 1, part of the remaining gap goes too.
- **Remedy:** none to the definition. The `no_spread` re-check with tuned results, after the height drop, has to happen before the verdict is final. This is a condition, not a reason to exclude: TIMI's 0.794 makes "Trivial" unproven (TP-4).

**6. The five flags were dropped under a rule that does not cover them (CLEAN-22, Must; CLEAN-5, Should).**

- **Problem:** CLEAN-5 covers exact copies of another column. These flags are not copies:
  - `sho` collapses Killip class into two levels;
  - `ant` is one level of `miloc`;
  - `hig` combines two columns;
  - `hyp` and `hrt` are thresholds, and not even exact ones (5 and 8 patients sit at the cut).
- CLEAN-22 lets a column leave only "for what it is". The curators kept columns of this kind in expresso_churn_prediction (`ARPU_SEGMENT`) and 2_month_survival_rate_prediction (`dzclass`) (precedent checker).
- **Effect:** small, a quality point (logistic regression −0.003).
- **Remedy:** keep them as released. Or, if the curator wants the drop, record it as an exception with the fact that sets it apart (cut points possibly chosen on this same cohort; pulse above 80 is not the usual cut of 100).

**7. Impossible values are kept, and one note is wrong (CLEAN-11, Should).**

- **Problem:**
  - Pulse of 1, 6, 8 and 9 in four Killip I patients (one with systolic pressure 180).
  - Pulse 0 with a measured pressure.
  - Systolic pressure 0 in a Killip I patient.
  - Ages 108, 108 and 110, entered as whole numbers while 98.8% of ages are fractional.
  - The note says the zeros are "mostly Killip IV, unmeasurable pressure in shock", but 3 of the 8 patients are Killip I (claim auditor #10).
  - `task_summary.row` says 40,830 patients; the table ships 40,826.
- **Remedy:**
  - Set the impossible pulse and pressure values in non-shock patients to missing, as in heart_disease (`chol` = 0) and thyroid_discordant (age 455). Ask the curator about the three ages.
  - Fix the note and the count.

I do not ask to drop the 28-row fill pattern (0.07% of rows; no score effect; labels do not travel with the copies).

</details>

<details><summary>Critic rebuttal</summary>

The advocate concedes most of my brief. The real disputes left are the fold layout, the metric, and one fact about the mic decision.

**Rebuttal: the critic, `gusto_i_mi_mortality`**

**Agreed with the advocate:** drop `height` (LEAK-10, Must), add the `Outdated` marker, add `groups_test_groups_few` to `accepted_check_warnings` with its numbers, add the US → non-US sentence to `splits_comment`, set the impossible zeros and pulses to missing, fix the wording (population, `fit_reason`, the split leaving `use_case`, 40,826 not 40,830), and keep the 28 template rows with a note.

**1. The task is real; the era is a note.** I concede. I never asked to exclude it, and the advocate has taken on the `Outdated` marker and the wording fixes from my point 2.

**2. The leak and the remedy.** I concede the point. One number differs: by my run, dropping `height` costs tuned LightGBM −0.0009, not 0.002. Either way, the cost is the leak.

**3. The split: I dispute 3×3 as the default.**

- The advocate cites sat11 (32 groups) and huesken (30) as the precedents with this fold size. Both have about twice our 16 groups.
- The nearest case is economic_well_being_prediction_challenge, decided by Andrej on 2026-11-25 (its record, CC lines of 2026-11-24 and 2026-11-25). It has 25 groups and ships **1×9 whole-group folds, each group tested once**, chosen over 3×3 on a measurement:
  - 3×3 "trains on a third fewer countries, so it sits about twice as far from the reference";
  - 3×3 shrank the gap between the two best models (−0.0021 against −0.0034);
  - its repeats "share most of their training countries".
- That fits here, where the method gaps are about 0.006 AUC. Folds of 5 or 6 regions train on 10 or 11 of the 16. A 1×8 layout (2 regions per test fold) would train on 14, and still hold about 190 to 590 deaths per test fold, going by the advocate's 95 to 294 per region.
- **Remedy:** the curator decides between 3×3 and 1×8 (or leave one region out). If no one measures it, the economic_well_being call points to 1×k. This is a protocol choice (SPLIT, Should), not a block.

**4. Value: I concede.** The advocate's table is the tuned re-check after the height drop that my point 5 asked for. Splines and tuned LightGBM beat plain logistic regression by about 0.006 AUC on 9 of 9 folds, about 6.5 standard errors. TIMI at 0.794 rules out "trivial". TP-3 is met. Whether `no_spread` stands on the 0.01 reading is a TP-2 call for the curator.

**One factual dispute in the same point.** "It joins the benchmark next to `mic` (option B)" is not settled. The mic item still ends "**Decision:** A, B, C or D?". This record has no CC line, and its `checked_by` and `data_foundry_status` are empty. The review should leave B or C open and not report it as decided.

**5. The data is what it claims: I concede**, with one item left. The three ages of 108 to 110 (whole numbers where 98.8% of ages are fractional) are not addressed. I ask that they go to the curator as one line, not be silently kept.

**6. The metric: I dispute "either is within the rules".**

- MET-8 decides this case directly: "A source that scores calibration together with [another measure] … asked for probabilities."
- The source here scores the c statistic together with calibration in the large and the calibration slope (the definition's own `reason`). That is exactly the Detrano pattern the rule quotes.
- MET-10 (Weigh) only applies to a borderline call between the source's metric and the fallback. MET-8 (Should) is the more specific rule for this fact, so it wins over a Weigh.
- The decision also needs the risk level. The benefit of the stronger drug scales with the absolute risk (domain practitioner), and regional death rates run from 5.3% to 8.4%. ROC AUC cannot see whether a model carries that level to an unseen region.
- **What sets this apart from heart_disease's `roc_auc` in the metrics case table:** nothing, as far as I can see. So the advocate is right that `roc_auc` has a precedent. The curator should therefore decide knowing that the applied precedent and the plain text of MET-8 point different ways, and say which one governs.
- My ask stands: `log_loss`. Log loss resolves the methods on 9 of 9 folds in the advocate's own run, so the choice costs nothing in separation. I don't argue it for separation either; I argue it for fidelity to the source.

**7. The five flags and the wording: I concede.** Keep the flags as released unless the curator records the exception. They are quality points, and none of them blocks shipping.

**Verdict:** ship after the changes we both list. The three calls for the curator:
1. the fold layout, 3×3 or 1×8, with the economic_well_being measurement as the nearest precedent;
2. `log_loss` (MET-8) or `roc_auc` (the heart_disease precedent);
3. the mic option, B or C, which is not yet decided.

</details>
