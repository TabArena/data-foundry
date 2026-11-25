---
unique_name: nhanes_dxa_body_fat
name: NHANES whole-body dual-energy X-ray absorptiometry (DXX) with body measures (BMX)
checked_by:
- AI (UNVERIFIED)
- Andrej
data_foundry_status:
- WIP (Triage)
claimed_by: Andrej
suggestion: TBD -> Yes
priority: 4
decision_markers:
- Selection Bias
tags:
- AI-Filled (Verify)
- Non-IID (Temporal)
- 'Samples: Over Time'
- 'Time: Dated'
- Survey
original_source: GOV Website
year: '2008'
collection_period: 1999-2006, 2011-2018
domain: medical & healthcare
problem_type: Regression
original_data_state: Database (or multiple to-be-joined tables)
source_links:
- https://wwwn.cdc.gov/nchs/nhanes/dxa/dxa.aspx
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2005/DataFiles/DXX_D.htm
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2011/DataFiles/DXX_G.htm
- https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/DXX_J.htm
v2_path: datasets/_dev/tabarena-v0pt2/nhanes_dxa_body_fat/dataset.py
needs_review:
- ai_unverified
type_adapter_id: curation-record-v1
---

## Comments

**⚠️ AI-FILLED — UNVERIFIED. The suggestion, metadata, and notes below were drafted by an AI assistant from the source's pages and papers and, where the block says so, from the source's files downloaded and counted on 2026-11-25, NOT from building the data. A human must verify everything before relying on it.**

**Screening (AI, 2026-11-25):** `TBD -> Yes`, priority 4: 39,691 people with a measured whole-body DXA percent fat and tape-and-scale measures (NHANES 1999-2006 and 2011-2018, counted on the CDC files today), found as the replacement for `body_density_prediction`; it reframes that task (DXA percent fat, not density by underwater weighing) and needs the era break and the imputed scans decided at the add stage.
- Source: CDC/NCHS NHANES, files DXX (whole-body DXA), BMX (body measures) and DEMO (age, sex, ethnicity, survey cycle), joined on `SEQN`, 2-year cycles; DXA overview page https://wwwn.cdc.gov/nchs/nhanes/dxa/dxa.aspx. Measured 2026-11-25 on the downloaded files: 1999-2006 21,858 people with a measured scan plus 5,401 whose scan was multiply imputed (5 imputations per person, `_MULT_`; measured where `DXITOT`, `DXITOTST` in 2005-2006, is 0); 2011-2018 17,833 (`DXAEXSTS` 1 and `DXDTOPF` present; no imputation); 39,691 measured in all, one row per person, no `SEQN` repeated. No DXA file after 2017-2018 (DXX_L returns 404, none for 2017-March 2020). Target `DXDTOPF` (total percent fat), 11.5 to 56.2, SD 8.8. The earlier block's "about 21,800 people", "ages 8-59" for every cycle and "about 16,000" for 2011-2018 are wrong: ages 8-85 in 1999-2004, 8-69 in 2005-2006 ("DXA scans were administered to eligible survey participants aged 8-69", DXX_D), 8-59 in 2011-2018. Features in both eras: sex, age, ethnicity, weight, height, BMI, waist (iliac crest), upper-arm circumference, upper-leg and arm length; thigh and calf circumference, triceps and subscapular skinfolds in 1999-2006 only; hip in 2017-2018 only. Fixed today: the source link to BMX_L (2021-2023 body measures, no DXA) replaced by the DXA overview and DXX_D; `collection_period` set; `year` left empty (the first DXA release date is not stated on the pages read).
- Use case: a clinician, a screening programme or a gym estimates body fat (and body-fat obesity) from a tape and a scale instead of a DXA scan; Woolcott and Bergman built the relative fat mass on these files as "a simple anthropometric linear equation that is more accurate than the body mass index (BMI) to estimate whole-body fat percentage" (Sci Rep 2018, abstract), Lee et al. built equations "in various epidemiological settings" (Br J Nutr 2017); fit direct for the use case, a reframing for `body_density_prediction` (another reference method: DXA does not give the underwater-weighing number for a person, so the two scores are not comparable). Collection `Samples: Over Time`, `Time: Dated` (the survey cycle, `SDDSRVYR` in DEMO), no target tag (scan and tape measures at the same examination), entities do not recur (a new sample each cycle); type `Survey` (SPLIT-34).
- Split: leaf [L-ORDER.windows] because [SUR.meets] the model meets the surveyed population at later rounds (a body-fat equation is used after it is fitted; the source validated RFM forward, "NHANES 1999-2004 data (n = 12,581) were used for model development and NHANES 2005-2006 data (n = 3,456) were used for model validation"), [ORDER.order] the cycle is recorded, [ORDER.windows] three windows hold on all eight cycles (2013-2014, 2015-2016, 2017-2018, each 3,658 to 5,056 people, the first training on 26,379 of 39,691, 66%). Lee et al. split at random; the forward split is the source's own and fits the use case (source task first). Open, for the add stage: (1) the era break: scanner and software change (Hologic QDR-4500A, then Discovery A with Apex), no DXA in 2007-2010, and 1999-2006 fat mass was adjusted ("the NHANES DXA lean mass was decreased by 5% and an equivalent kilogram weight added to the fat mass", DXX_D); measured today, training on 1999-2006 and testing on 2011-2018 costs 4% to 8% RMSE against a random split within 2011-2018 (linear 4.54 against 4.21, LightGBM 3.59 against 3.44; mean bias -0.63 and -0.26 points); 2011-2018 alone gives only two windows at the half floor (2013-2014 would train on 25%), so dropping the old era moves the split to an exception or the forced step; (2) the era-only features: with test windows in 2011-2018, the skinfolds, thigh and calf are missing in every test row and hip exists only in the last window, so the common 8 measures (or era-only features left in as missing, for a person to decide); (3) children: keep ages 8-19 (another body, but the same equations' use; Woolcott's paediatric RFM was built on these files) or adults only.
- Imputed scans: keep only measured ones. CDC: "Imputed values should not be treated as measured variables", and the imputation is a sequential regression model (IVEware, DXX_D), so an imputed percent fat is a model's prediction, partly from the same body measures, not a measurement. Dropping them selects the sample, as CDC warns ("there seemed to be systematic, non-random patterns to the missing data. Use of only the measured variables could lead to biased results"): measured today, 71% of people with BMI 40 or more in 1999-2006 have an imputed scan (13% below BMI 25), and the imputed median BMI is 28.5 against 24.8; in 2011-2018 the unscanned (no imputation) have median BMI 27.2 against 25.3. Both eras thus miss the heaviest people the same way (the table limit, "weight over 300 pounds" then 450), a `Selection Bias` to state in the notes, not a reason against the task. The "Supplemental Highly Variable Data" files are not used.
- Siblings and duplicates: `body_density_prediction` (`Yes (Disagreement)`, shipped; its issue of 2026-11-25 recommends keeping it until this record is added, then retiring it as replaced); `body_fat_prediction_dataset` (`No`, a duplicate of it); other NHANES records are other targets on the same survey (`nhanes_bmi_from_habits`, `nhanes_undiagnosed_diabetes`, temporal by cycle, and more; PROV-7). External collections: none found.
- Better data: found as better data for `body_density_prediction`. Nothing better for this record: NHANES has no whole-body DXA after 2017-2018 (checked today); UK Biobank's DXA imaging subset is restricted access; KNHANES ran DXA in 2008-2011 (Korea, registration; not counted, another population rather than a larger one); the Kaggle body-fat files are small or from bioimpedance scales, not a reference measurement.
- Papers and pages: CDC DXA overview and DXX_D, DXX_G, DXX_J documentation; Woolcott and Bergman 2018, Sci Rep 8:10980 (doi 10.1038/s41598-018-29362-1, full text through Europe PMC, PMC6054651); Lee et al. 2017, Br J Nutr 118(10):858-866 (doi 10.1017/S0007114517002665, abstract); Woolcott and Bergman 2019 (paediatric RFM, doi 10.1038/s41598-019-51701-z); Kelly et al. 2009, PLoS One (DXA reference values, not read).
- Metric: no unique one: RFM's "Model selection was based on the ability to predict whole-body fat percentage (R 2 ) ..., the lowest RMSE, the lowest Akaike information criterion, the overall performance in terms of accuracy and precision, and the simplicity" (Methods), and it reports bias, accuracy within 20%, precision, R² and RMSE; Lee et al. report R² and the standard error of estimate; so the fallback `rmse` in percent-fat points (MET-5, MET-8), which both papers also report. Inputs none (the survey weights the papers use are not needed for a prediction score).
- Baselines (measured 2026-11-25, untuned LightGBM against linear regression, RMSE in percent-fat points, repeated 3-fold): both eras on the common 8 measures, 39,691 people: 3.39 against 4.22; 2011-2018: 3.42 against 4.21 (R² 0.84 against 0.76); 1999-2006 with skinfolds: 2.88 against 3.32; a linear model with pairwise interactions closes most of the gap (3.53 and 2.92), which comes from mixing sexes and ages; on men 22-81 alone the methods tie (3.08 against 3.04).
- Risks for /add-dataset: regional fat and lean, bone and every other DXA column are outcomes of the same scan, never features (LEAK-10); `BMXBMI` is weight over height squared (redundant, keep or drop as a feature-set choice, not a leak); pregnant women are not scanned; the selection of the measured scans and the table limits (`Selection Bias`); the era break and the era-only features above; 24 files to join (3 per cycle). Licence: public domain (US federal survey data).
- Priority: gap 0 (medical, regression and temporal are not thin), use case + (the RFM and Lee papers name the estimate and the obesity decision; fit direct), source + (NCHS documentation and two papers on these files), shape + (39,691 people, mixed features, 8 dated cycles); no risk counted (better data none; the reframing of the old task is `body_density_prediction`'s decision, not a risk of this data).

**Screening (AI, 2026-10-31):** `TBD -> Yes`, priority 4: whole-body DXA percent fat with tape-and-scale body measures for about 4,000 people per NHANES cycle, the precedent the curation rules name for `body_density_prediction` (252 men, 1985); the target is the quantity body density stands in for, measured by a reference method.
- Source: CDC/NCHS NHANES DXA whole-body files: DXX_G (2011-2012) 5,692 records, 4,521 with total percent fat (DXDTOPF); DXX_J (2017-2018) 5,114 records, 3,658 with it; "Participants aged 8-59 years were eligible"; "Whole body DXA scans were administered from 1999-2006 and 2011-2018" (DXX_J). Joined by SEQN to the body measures BMX (weight, height, waist, arm and thigh circumference; hip from 2017-2018; skinfolds in 1999-2006, per the scout) and demographics. The 21,768 people of the precedent were not recounted; 2011-2018 alone should give about 16,000.
- Use case: a clinician, gym or fitness device estimates body fat from a tape and a scale instead of a DXA scan or underwater weighing (the curator on `body_density_prediction`: still "done by models in machines in gyms"); Woolcott and Bergman built Relative Fat Mass equations on NHANES 1999-2006 DXA (Sci Rep 2019, n = 10,390 aged 8-19, doi 10.1038/s41598-019-51701-z), "useful to estimate whole-body fat percentage and diagnose body fat-defined overweight or obesity"; fit direct; regime IID by person as on `body_density_prediction`, or temporal by cycle as the other NHANES records (DXA software versions changed across cycles, DXX_J): the curator decides.
- Siblings and duplicates: `body_density_prediction` (`Yes (Disagreement)`, shipped; Outdated, Not Representative, Too Small), `body_fat_prediction_dataset` (`No`, its duplicate); `nhanes_bmi_from_habits` (another target on the same exam, PROV-7). External collections: none known (not searched: the run's web search budget was used up).
- Better data: found as better data for `body_density_prediction`; no further search this round.
- Papers and pages: the DXX file pages; Woolcott and Bergman 2019 (abstract, read through Europe PMC).
- Metric: the RFM paper reports several accuracy measures (estimates within a range of the measured fat, obesity misclassification) without one ranked criterion (MET-5), so the fallback `rmse` in percent-fat points, as declared for `body_density_prediction` (MET-8); inputs none.
- Risks for /add-dataset: the 1999-2006 DXA was released with multiple imputations of missing scans (the scout's note; the 2011-2018 pages do not mention it): take one imputation or use 2011-2018 only; regional fat and lean of the same scan are outcomes, never features (LEAK-10); exclusions (pregnancy, over 450 lb or 6 ft 5 in, recent contrast) and "Whole body not scanned, other reason" (690 in 2017-2018) leave a selected sample; ages 8-59 only.
- Priority: gap 0 (medical, regression not thin), use case + (named by the curator and by the RFM papers), source + (NCHS documentation), shape + (about 16,000 people or more, mixed features), risk 0.

**Assessment (AI, 2026-10-31):** a candidate from the data-scouting run of 2026-10-30/31, not screened yet. Found through better data for `body_density_prediction`.
- as published: 21,768 people per the curator's precedent in selection.md (not recounted); one row per examined person; target DXDTOPF 'Total Percent Fat' plus regional fat/lean; features from BMX: weight, height, ...; target: whole-body percent fat by DXA, the quantity body density is a proxy for (Siri's formula), measured by a better reference method; access: open.
- Why: the precedent named in selection.md and SKILL.md step 3 for this exact record; same anthropometric features known at the prediction point
- Adds: about 86x the people of the 252 men from 1985, both sexes and ages 8-59+, a national sample; risks: 1999-2006 files are 5 imputations (use one, or the 2011-2018 cycles only), exclusions for pregnancy and >450 lb

**Assessment (AI, 2026-11-25):** corrections to today's screening block, found while adding the dataset: the 5% shift of lean to fat mass is in both eras, not 1999-2006 only (DXX_G and DXX_J: "The NHANES BCA option was enabled ... this option adds 5% of lean mass to the fat mass"); the era break is the scanner hardware and software (Hologic QDR-4500A, software 8.26 and then Discovery 12.4, against Discovery A with Apex in 2011-2018). And 76%, not 71%, of people with BMI 40 or more in 1999-2006 have an imputed scan (recounted on the first imputation record; 13% below BMI 25 and the medians 28.5 against 24.8 hold). The definition keeps 39,601 people, not 39,691: 90 people of 1999-2006 whose flag reads measured carry a percent fat that differs across CDC's five imputation records and are dropped.

**Assessment (AI, 2026-11-25):** review panel (full): ship after changes (five applied: 90 people with a varying imputed label dropped, four windows, the no-gap reason on the same-day scan, a non-Hispanic Asian level from 2011, the notes on weighting, selection and tested ages); disputed: CLEAN-1 (keep the 893 2011-2018 scans with an invalid region), CLEAN-22 (the six measures taken in some cycles only); for the curator: issues 1-3 and the horizon H. Priority 4: gap 0, use case +, source +, shape +, risk 0 (gap: medical, regression and temporal are not thin among the accepted definitions; use case: the relative fat mass and Lee papers name the estimate and the obesity decision, fit direct; risk: no leak, the open issues move no score and none argues against shipping).

CC (2026-11-25, Andrej): review of the added dataset (Review H, 1, 2, 3):
- `Selection Bias` set (issue 3, B): the heaviest people often have no usable scan (in 2017-2018, 50% of examined adults aged 20-59 with BMI 40 or more have one, against 75% below BMI 30), and no one aged 60 or over is tested; nothing changes in the definition.
- `year` set to 2008, the definition's (the first DXA file, 1999-2000, was published in January 2008).
- Asked whether the 893 newer-scanner scans with an invalid region can be aligned across the eras instead of kept or dropped (issue 1), and whether measures brought back would still be dropped for models when the test rows lack them (issue 2); both answered, open.

CC (2026-11-25, Andrej): the declared horizon (one two-year survey cycle, no gap, windows starting 2017, 2015, 2013 and 2011; Review H, as implemented) is checked: the cycle is the finest time the release holds and the source's own forward step, and the scan is taken at the same examination as the measures, so no label waits.

**Assessment (AI, 2026-11-25):** the curator's questions measured on the definition's 39,601 people, untuned LightGBM, 3 seeds. Issue 1: CDC's own analysts drop every 2011-2018 scan with an invalid region (Stierman et al., Am J Clin Nutr 2021, NCHS); dropping the 893 (140, 148, 241 and 364 per cycle) moves the windows' RMSE by -0.05 to +0.01 points. CDC's 1999-2006 imputation would add 2,943 partly imputed old-era people (median BMI 30.3; their percent fat varies across the five records by a median of 1.6 points) and moves the RMSE by at most 0.016. No published cross-calibration covers NHANES's QDR-4500A and Discovery A. Issue 2: the framework ships every column in every window, so a measure the test rows lack reaches the model as all missing. With the six measures kept, the 2011-2012 window's RMSE rises from 3.43 to 5.36 (bias +3.43) and the others' by 0.01 to 0.10. A method that drops the columns its test rows lack matches the 11-feature scores, or improves them by up to 0.015 with the sagittal diameter.

CC (2026-11-25, Andrej): issue 1, b ("Reply (b): Drop all 893"): every 2011-2018 scan with an invalid body region is dropped, as CDC's analysts do when they compare the eras (Stierman et al. 2021), so both eras keep a scan only when every region is valid; the definition keeps 38,708 people.

CC (2026-11-25, Andrej): issue 2, d ("Reply (d): Keep the sagittal diameter only"): the sagittal abdominal diameter (`BMDAVSAD`, 2011-2016) is an input again, the one era-only measure that windows hold in both training and test rows (2013-2014 and 2015-2016); the skinfolds, thigh, calf and hip stay out. `splits_feature_missing_in_test` is accepted: the 2011-2012 window has no training value of it.

**Assessment (AI, 2026-11-25):** both decisions applied and measured on the rebuilt definition.
- Rows: 38,708 (39,601 less the 893 scans with any of the twelve region invalidity codes not 0; no code is missing among completed scans). Per cycle 4,671, 6,425, 5,797, 4,875 (1999-2006, unchanged), 4,381, 4,908, 4,357 and 3,294 (2011-2018).
- Windows: test 3,294, 4,357, 4,908 and 4,381 people (2017, 2015, 2013, 2011), training 35,414, 31,057, 26,149 and 21,768 (91.5%, 80.2%, 67.6%, 56.2%); a fifth window, 2005-2006, would train on 43.6%. Non-Hispanic Asians are 607 (13.9%) of the 2011-2012 test people.
- Sagittal diameter: the variable is `BMDAVSAD` in BMX_G, BMX_H and BMX_I ("Average Sagittal Abdominal Diameter (cm)"), absent from BMX to BMX_D and BMX_J. Present in 4,334, 4,845 and 4,319 kept rows of 2011, 2013 and 2015 (99%), in no other row; 9.6 to 40.6 cm. The 2017-2018 test rows all lack it while 38% of that window's training rows have it.
- Selection: of the examined adults aged 20-59 in 2017-2018, 28% with BMI 40 or more have a kept scan, against 70% below BMI 30 (49% and 74% with the invalid-region scans).
- `dataset check`: 0 errors, 1 warning (8 distinct cycles); `splits_below_target` and `splits_feature_missing_in_test` accepted (the latter fires on the 2011-2012 window only: 100% missing in training, 1% in test). Leak probe: R^2 0.845 with all features, no single feature above 0.34, no exact feature copies across the split; the 2017-2018 cycle has fewer rows than the band before it (3,294, z -3.4): the cycle had the fewest scans (3,658 with a percent fat), the most without a whole-body value (15.6%) and the most invalid-region scans dropped (364); not censoring, the label being same-day. Task probe: LightGBM RMSE 3.399 against 4.242 for linear regression and 8.565 for the training mean, ahead of the mean on all four windows; dtype probe: no column flagged.
- Side effect in the 2017-2018 window (untuned LightGBM, 5 seeds): RMSE 3.405 with the sagittal diameter against 3.350 without (the window's test rows lack it), and the mean error for its 544 Asian people (measured minus predicted) is -0.91 points with the Asian level against +0.58 without the diameter; the 2013-2014 and 2015-2016 windows gain 0.004 and 0.012, 2011-2012 is unchanged (3.434).

## Review

**Outcome:** added; the AI recommends shipping it. 38,708 people of NHANES 1999-2006 and 2011-2018 with a whole-body DXA percent fat CDC measured on a scan with every body region valid, 12 inputs from a tape, a scale, an abdominal caliper and the interview (sex, age, ethnicity, weight, height, BMI, waist and upper-arm circumference, upper-leg and upper-arm length, the sagittal abdominal diameter of 2011-2016, the survey cycle), RMSE in percent-fat points (fallback). Split: one two-year cycle per window, the four newest (2017-2018, 2015-2016, 2013-2014, 2011-2012), each training on every earlier cycle (91.5% to 56.2% of the people), no gap. Validity: no leak (only the target and the region validity codes are read from the scan file); the label is CDC's measured value, imputed scans dropped, also 90 people whose flag said measured but whose value differs across CDC's five imputation records. Value: LightGBM RMSE 3.40 against 4.24 for linear regression and 8.57 for the training mean (percent-fat points, lower is better), ahead of the mean on all four windows. Weighed: the reference-method label, the size and the source's own forward validation against a sample that thins the heaviest people and tests no one over 59 (issue 3). The panel's five changes are applied: the 90-row filter, four windows, the no-gap reason, a non-Hispanic Asian level from 2011, and the notes on weighting, selection and the tested ages. Replaces `body_density_prediction`'s task with another reference method; the two scores are not comparable. Decided 2026-11-25: the four one-cycle windows (H, as implemented); both eras keep only scans with every region valid, the 893 newer-scanner scans with an invalid region dropped (issue 1, b); the sagittal diameter back as the one era-only input, the five other era-only measures out (issue 2, d); the `Selection Bias` marker (issue 3, B). `dataset check`: 0 errors, 1 warning (8 distinct cycles); `splits_below_target` and `splits_feature_missing_in_test` accepted.

**Main points:** Open: whether the sagittal diameter stays now that every 2017-2018 test row lacks it (issue 4). Settled 2026-11-25: the windows (H), the 893 newer-scanner scans with an invalid region dropped so both eras keep only fully valid scans (issue 1, b), the sagittal diameter back as the one era-only input (issue 2, d) and `Selection Bias` (issue 3). Nothing is open.

**Record judgment:** valid. CDC's whole-body DXA, the reference measurement body-fat equations replace, with the exam's tape-and-scale measures of the same day; the relative fat mass equation was built and validated forward on these files. The sample thins the heaviest people and tests ages 8-59 only.

**Horizon:**

* **Verdict:** keep one two-year cycle per window, the four newest, no gap; confident on the length and the gap, the count follows the windows rule.
* **Length:** one survey cycle, the finest time the release holds (exam dates are not public) and the source's own forward step: the relative fat mass was developed on 1999-2004 and validated on 2005-2006[^h1]. Such equations are refit rarely, about once a decade (our assumption); the data cannot hold windows that long.
* **Gap:** none. The scan is taken at the same examination as the measures (DXX documentation), so a person's label exists when they are examined. The 2011-2018 values as released are CDC's re-analysis with the Apex software: every 2011-2018 DXX page shows "First Published: March 2020", and the original release lag could not be established, so the gap rests on the same-day scan, not on release dates[^h2].
* **Time frame:** the eight cycles with whole-body DXA, 1999-2006 and 2011-2018 (none in 2007-2010, none after 2017-2018; the cycle dates are CDC's). Every window tests on the newer scanner of 2011-2018 and on ages 8-59. The 2011-2012 window trains on the older scanner's cycles alone: it tests across the change of scanner and of sampling, which the windows rule counts as a period a deployed model must handle[^h3]; its feature drift is the largest of the candidates, and its 619 non-Hispanic Asian test people (13.7%) have a level no training row carries.

  | Test cycle | Test people | Train people | Train share | Target mean (test) | Largest feature drift (PSI) |
  |---|---|---|---|---|---|
  | 2017-2018 | 3,658 | 35,943 | 90.8% | 32.32 | age 0.79 |
  | 2015-2016 | 4,598 | 31,345 | 79.2% | 31.85 | age 0.78 |
  | 2013-2014 | 5,056 | 26,289 | 66.4% | 32.07 | age 0.77 |
  | 2011-2012 | 4,521 | 21,768 | 55.0% | 31.26 | ethnicity 1.16 |
  | 2005-2006 (not used) | 4,875 | 16,893 | 42.7% | 30.94 | age 0.76 |

* **Options:**

  | | Option | What it does | Test windows | Pro | Con |
  |---|---|---|---|---|---|
  | A | One cycle, no gap, four windows (implemented) | The four newest cycles, each training on every earlier cycle | 4: 3,658, 4,598, 5,056 and 4,521 people | as many windows as the half-data floor allows; tests across the scanner and sampling change; the source's own forward step | the 2011-2012 window trains on the old scanner alone and meets an ethnicity level it has not seen |
  | B | One cycle, no gap, three windows | As built first: 2017-2018, 2015-2016, 2013-2014 | 3: 3,658, 4,598 and 5,056 people | every window trains on both scanners | one window fewer than the floor allows; leaves out the window across the change of scanner, which the windows rule counts as a reason to test; needs a recorded exception with its fact |
  | C | One cycle, a one-cycle gap | Each window trains on the cycles before the one preceding it | 3: 3,658, 4,598 and 5,056 people (training 79.2%, 66.4%, 55.0%) | covers a release lag, should one exist | no lag is established and the label is same-day; drops the newest training cycle from each window |
  | D | One cycle, no gap, five windows | A plus 2005-2006 | 5: A's four and 4,875 people | one window inside the old scanner era | the fifth trains on 42.7%, below half the data: the curator's exception |
  | E | Two cycles, no gap | 2015-2018, then 2011-2014 | 2: 8,256 and 9,577 people (training 79.2%, 55.0%) | wider test windows | under the three windows a temporal task needs |

* **Recommendation:** A. It reaches the most windows the floor allows, and the window B leaves out tests the change of collection a deployed equation meets; the panel (split auditor, precedent checker, advocate and critic) agrees. **Decision:** A, B, C, D or E?

**Notes for the AI:** A is implemented: `TemporalSplits(window=1, unit="unique", n_windows=4)` on `survey_cycle`, `horizon=2` years, `splits_below_target` accepted in the definition with the reason. B: `n_windows=3`, a CC line with the fact (the AI's best guess: a window trained on the old scanner alone measures a calibration shift no deployed equation meets, since today's clinic DXA is the newer kind) and the reason in `splits_comment` and the acceptance. C: a gap of one cycle in `TemporalSplits`. D: `n_windows=5`, a CC line for the 2005-2006 window under half and `splits_train_under_half` accepted with it. Re-run `dataset check` and `dataset windows`.

[^h1]: Woolcott and Bergman 2018, Sci Rep 8:10980: "NHANES 1999-2004 data (n = 12,581) were used for model development and NHANES 2005-2006 data (n = 3,456) were used for model validation".
[^h2]: **SPLIT-10** (Should): a gap where a label is known only some time after its row; none here, the scan being same-day.
[^h3]: **SPLIT-15** (Must for the newest window, Should for the others): the other windows are argued from the use case, "which periods a deployed model must handle (other years, seasons, holidays, events, a change of rules or of the data collection)"; the evidence is statistics of the data, never a model's score. **SPLIT-14** (Must): every window trains on at least 50% of the data; under that, the curator's exception, never below 30%. **SPLIT-33**: 39,601 rows would get 9 splits.

**Andrej (2026-11-25, ok):** As implemented (A).

**Resolved (2026-11-25, Andrej):** A: one two-year cycle per window, no gap, the four newest cycles (2017-2018, 2015-2016, 2013-2014, 2011-2012), each trained on every earlier cycle (90.8% to 55.0% of the people); nothing changed in the definition with the sign-off. `dataset check`: 0 errors.

**Issues for the curator:**

1. **Keep or drop the 893 newer-scanner scans that have an invalid body region?**

   * **Problem:**
     - In 2011-2018 CDC publishes a whole-body percent fat even when one region of the scan is invalid, and the definition keeps those 893 scans (364 of them, 10%, in the 2017-2018 test window), while in 1999-2006 CDC imputed every such scan and the definition drops it.
     - So the two eras keep different scans: the same heavy person with a partly invalid scan is kept only if scanned after 2010.
     - 149 of the 2017-2018 ones have the trunk coded "excessive x-ray noise due to morbid obesity", a region CDC says could not be analysed accurately, inside the label.
   * **Background:** DXX_J: "If any region was coded as invalid all bone and soft tissue measurements for that region were set to missing"; the whole-body total stays filled, and equals total fat over total mass within 0.05 (critic's check). No measured total exists for such a scan in 1999-2006, only CDC's imputations.
   * **Effect on the task:** the newer test windows hold heavier people than a rule matching the old era would keep; the ranking of models does not move.
   * **Experiments:** LightGBM, RMSE in percent-fat points (lower is better), on the windows as first built; the first table and the scoring rows of the second are the claim auditor's run, the training rows the column auditor's:

     | Rows | Kept rows by cycle (2011 / 2013 / 2015 / 2017) | Median BMI | Test RMSE 2017-2018 | Test RMSE 2015-2016 |
     |---|---|---|---|---|
     | Scans with an invalid region | 140 / 148 / 241 / 364 | 33.6 | 3.78 | 3.68 |
     | Fully valid scans | the rest | 24.9 | 3.38 | 3.31 |

     | Comparison, 2017-2018 window | Run | RMSE |
     |---|---|---|
     | Scored on all test rows | claim auditor | 3.38 |
     | Scored on valid test rows only | claim auditor | 3.37 |
     | Trained on all scans, all test rows | column auditor | 3.417 |
     | Trained on valid scans only, all test rows | column auditor | 3.410 |

   * **Panel:** both auditors who measured it and the advocate recommend keeping with a note; the critic leans to dropping at least the trunk-noise rows, as the only rule that treats both eras alike, and accepts keeping.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with a note (implemented) | Keeps all 893; the curation notes and the Selection Bias note state the difference between eras | CDC's own published value; keeps the heavy tail the sample already thins; scores unchanged | the eras keep different scans; 149 labels include a trunk CDC calls noisy |
     | B | Drop all 893 | Keeps a 2011-2018 scan only when every region is valid | one rule in both eras | thins the heaviest test people further (median BMI 33.6); 893 rows fewer |
     | C | Drop the trunk-noise scans only | Drops the 2011-2018 scans with the trunk coded for obesity noise (149 in 2017-2018, 0 to 5 in each earlier cycle) | removes the labels CDC flags as least accurate | still two rules across eras; a cut on one code |

   * **Recommendation:** A. The label is CDC's published value, the score does not move, and dropping thins the part of the sample that is already under-covered; the asymmetry is stated in the notes[^i1a]. **Decision:** A, B or C?

   **Notes for the AI:** A is implemented. B or C: read the regional invalidity codes of DXX_G to DXX_J (the `DXA*V` columns the claim auditor used) in `_load_raw`, drop 2011-2018 rows with any code other than 0 (B) or the trunk code 3 (C), update the counts in the curation notes and the splits comment, re-run `dataset check`, `dataset windows` and the task probe.

   [^i1a]: **CLEAN-1** (Should): adopt the cleaning rules "that hold for the train and the test period alike". The remedy ladder: the mildest remedy that settles the issue, here a note.

   **Andrej (2026-11-25, discuss):** Why are the only options keeping or dropping, can't we align this to get rid of the measurement inconsistency?

   **Answer (AI, 2026-11-25):** the source publishes two alignments of the invalid regions: CDC's own analysts drop every 2011-2018 scan with an invalid region (option b, one rule in both eras), and CDC's 1999-2006 region imputation could bring the old era's partly invalid scans back (new option d); no published equation aligns the two scanners.

   * **Problem:**
     - CDC's own analysts align the eras by dropping: comparing 1999-2006 with 2011-2018 DXA percent fat, Stierman et al. (NCHS, 2021) write "Those with any missing data during 2011–2018 did not have total body adiposity measures calculated and were excluded"[^i1b]. That is option b, and it gives both eras one rule: a scan counts only when every region is valid (1999-2006 keeps only scans with no region imputed).
     - Imputing the region is CDC's handling for 1999-2006 only ("No publicly-released DXA data from 2011–2018 were imputed", same paper). The old era's partly invalid scans come back only with a label partly made by CDC's imputation model, which used weight and waist, two of our inputs. CDC: "Imputed values should not be treated as measured variables".
     - The 2011-2018 scans need no imputation for the target: their whole-body total is published. An imputation of our own would replace a measured total with a model's guess, which is weaker than either published route.
     - Scanner and software: no published cross-calibration covers NHANES's pair (QDR-4500A with software 8.26 and 12.x, then Discovery A with Apex 4.0 and the NHANES BCA option). NHANES's documentation reports phantom cross-calibration within each era, with corrections "found to be small and correction of the participant data not required". It gives no conversion between the eras. The only shared adjustment is the 5% lean-to-fat correction, applied in both eras. CDC's trend paper compares the eras directly and says only that the different machines "could lead to variability, though use of quality control scans should keep such variability to a minimum". The published in-vivo equations are for other models (QDR 4500W against Discovery Wi or A: Covey et al. 2008; Dowthwaite et al. 2018, 130 girls and young women)[^i1c]. A shift of our own cannot be estimated from the data, because the scanner change coincides with a real change in body fat between the eras (+0.7 points in youth, Stierman et al.).
   * **Background:** the old era's partly invalid scans that CDC imputed. Completed scans (exam status 1) with at least one region imputed, label = the mean of the five records; counted on the downloaded files:

     | | People | Median BMI | Regions imputed | Spread of the percent fat across the five records (points) |
     |---|---|---|---|---|
     | 1999-2006 partly imputed | 2,943 (595 / 680 / 830 / 838 per cycle) | 30.3 (kept 1999-2006 rows: 24.8) | one region in 1,493; the trunk in 1,321 | median 1.6, 90th percentile 3.8, max 13.4 |
     | 2011-2018 with an invalid region (kept now) | 893 (140 / 148 / 241 / 364) | 33.6 (fully valid: 24.9) | the published total, no imputation | none |

   * **Experiments:** untuned LightGBM, 3 seeds, RMSE in percent-fat points (lower is better) on the four windows as defined; b scores its own (valid) test rows:

     | Window | a Keep (implemented) | a on valid test rows | b Drop all 893 | c Drop trunk-noise | d Keep + 1999-2006 partly imputed |
     |---|---|---|---|---|---|
     | 2017-2018 | 3.398 | 3.353 | 3.350 (3,294 test rows) | 3.398 | 3.394 |
     | 2015-2016 | 3.324 | 3.308 | 3.301 (4,357) | 3.317 | 3.315 |
     | 2013-2014 | 3.371 | 3.372 | 3.369 (4,908) | 3.371 | 3.356 |
     | 2011-2012 | 3.427 | 3.434 | 3.434 (4,381) | 3.426 | 3.425 |

     The invalid-region test rows score 3.78 (2017-2018) and 3.61 (2015-2016) under a, and 3.76 and 3.63 under d: adding the old era's heavy scans to training does not help predict them.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep with a note (implemented) | Keeps all 893 | CDC's published total; keeps the heavy tail | two rules across the eras; 149 labels include a trunk CDC calls noisy |
     | b | Drop all 893 | Keeps a 2011-2018 scan only when every region is valid | the source's own alignment (CDC's analysts, 2021); one rule in both eras; scores within 0.05 of a | 893 heavy people fewer (364 in the newest test window); the heavy tail thins further, which `Selection Bias` now flags |
     | c | Drop the trunk-noise scans only | Drops the 154 scans with the trunk coded for obesity noise | removes the labels CDC flags as least accurate | still two rules across the eras |
     | d | Keep, and add 1999-2006's partly imputed scans | Adds 2,943 training people with the mean of CDC's five imputations as the label | aligns the other way, keeping partly invalid scans in both eras; uses CDC's published imputation; the heaviest old-era people come back | part of each added label is CDC's model output from weight and waist, two of our inputs (spread up to 13.4 points); departs from CDC's "not measured" warning; scores move by at most 0.016 |

   * **Recommendation:** b. It is the only alignment the source itself publishes for the measured data. It applies the 1999-2006 rule (every region valid) to 2011-2018, and it moves no score by more than 0.05. d aligns through imputed labels, and the task drops those on purpose[^i1d]. No option aligns the scanners: no conversion exists for NHANES's pair. **Decision:** a, b, c or d?

   [^i1b]: Stierman B, Ogden CL, Yanovski JA, Martin CB, Sarafrazi N, Hales CM. Changes in adiposity among children and adolescents in the United States, 1999-2006 to 2011-2018. Am J Clin Nutr 2021;114(4):1495-1504 (NCHS authors), Methods and Limitations.
   [^i1c]: Covey MK, Smith DW, Berry JK, Hacker ED. Importance of cross-calibration when replacing DXA scanners. J Nurs Meas 2008;16(3):155-170 (abstract only); Dowthwaite JN et al. Cross-calibrated dual-energy X-ray absorptiometry scanners demonstrate systematic bias in pediatric and young adult females. J Clin Densitom 2018;21(2):281-294 (Deming equations QDR 4500W to Discovery A; abstract only). NHANES DXX_G to DXX_J and the 1999-2000 documentation: phantom cross-calibration within each era.
   [^i1d]: **CLEAN-1** (Should): cleaning rules that hold for the train and the test period alike. **USE-5** (Must): "Check how the source built its label before accepting it"; here CDC says imputed values are not measurements.

   **Andrej (2026-11-25, discuss):** Reply (b): Drop all 893

   **Resolved (2026-11-25, Andrej):** b: every 2011-2018 scan with an invalid region is dropped, as CDC's analysts do (Stierman et al. 2021), so both eras keep a scan only when every region is valid. `dataset.py` reads the twelve region invalidity codes of DXX_G to DXX_J and keeps a completed 2011-2018 scan only when all are 0; the curation notes, the `row`, `changes`, the Selection Bias note, the splits comment and the `splits_below_target` reason carry the new counts. 38,708 people (2011-2018: 4,381, 4,908, 4,357 and 3,294 per cycle); the windows train on 91.5%, 80.2%, 67.6% and 56.2%. CC line in the comments. `dataset check`: 0 errors, 1 warning (8 distinct cycles); leak probe: no leak (the newest cycle's lower row count is the dropped scans, not censoring); task probe: LightGBM RMSE 3.399 against 4.242 for linear regression and 8.565 for the training mean; dtype probe: no column flagged.

2. **Bring back the measures NHANES took in some cycles only?**

   * **Problem:**
     - The definition drops six body measures because each was taken in some cycles only, the reason the cross-dataset decision of 2026-11-11 turned down when it kept such columns on seven other datasets.
     - The sagittal abdominal diameter is in 2011-2016, so it reaches the training and the test rows of three windows; the skinfolds, thigh and calf are in training rows only; hip is in the 2017-2018 test rows only.
     - The one reason left, that the skinfolds and the sagittal diameter need calipers, holds only if the use case is tape and scale, which is the curator's reading to confirm.
   * **Background:** kept rows with a value:

     | Measure | Cycles | Kept rows with a value | Use in the shipped windows |
     |---|---|---|---|
     | Thigh and calf circumference (tape), triceps and subscapular skinfolds (calipers) | 1999-2006 | 4,145-6,400 per cycle and measure | training rows only |
     | Sagittal abdominal diameter (calipers) | 2011, 2013, 2015 | 4,470, 4,990, 4,555 | training and test rows of the 2011, 2013 and 2015 windows |
     | Hip circumference (tape) | 2017 | 3,062 of 3,658 | test rows of 2017-2018 only |

   * **Consistency:** `onlinenewspopularity` keeps `kw_min_min`, missing in every test window, and six other definitions kept their columns that start or stop (decision of 2026-11-11, A)[^i2a]. Against it, `anes_voting_2026` inherited a rule that drops questions asked in only some years; nobody raised it as a reason here.
   * **Panel:** the advocate and the critic agree that thigh, calf and hip come back; the critic asks for all six (B), the advocate for C. The builder's comparison of model scores with and without the columns is no reason either way[^i2b]. The domain practitioner names the clinician and the epidemiologist as the actors and the gym as a weak third; a clinic may own calipers.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Common measures only (implemented) | 11 features; the six measures dropped | one feature set across eras | rests on the reason the decision of 2026-11-11 turned down; drops the sagittal diameter that test rows carry |
     | B | Keep all six | 17 features, each missing where not taken; `splits_feature_missing_in_test` accepted with the CC date | follows the decision of 2026-11-11; the data as published | four columns never meet a test row, hip no training row; the question widens past tape and scale |
     | C | Keep the tape measures | Thigh, calf and hip come back; the skinfolds and the sagittal diameter stay out, with a CC line setting the use case to tape and scale | each column leaves for what it is; keeps the question exact | a use-case reading the curator records as an exception; drops the one era-only measure that test rows carry |

   * **Recommendation:** B. It follows the decision of 2026-11-11 without an exception, and the sagittal diameter is information three test windows have; C is the choice if the task stays strictly tape and scale. **Decision:** A, B or C?

   **Notes for the AI:** B: add `BMXTHICR`, `BMXCALF`, `BMXTRI`, `BMXSUB`, `BMDAVSAD` (the 2011-2016 sagittal diameter) and `BMXHIP` (names as the panel read them in the BMX files; confirm in each cycle's codebook) to the kept columns with plain names; update `task_summary.known` and `question` (tape, scale and calipers), `changes` and the Features note; accept `splits_feature_missing_in_test` in `accepted_check_warnings` with the CC date. C: thigh, calf and hip only, the CC line with the tape-and-scale reading, the note that the sagittal diameter exists in three test cycles. Re-run `dataset check`, the leak, task and dtype probes.

   [^i2a]: **CLEAN-22** (Must): "Columns leave for what they are (a leak, an identifier, a copy, the measurement that defines the label), never for how many there are." The cross-dataset item "Accept `splits_feature_missing_in_test` where a column starts or stops being recorded" (Resolved 2026-11-11, Lennart, A): keep the data as the deployed model met it.
   [^i2b]: **EV-4**: a model's score is no reason to drop a column.

   **Andrej (2026-11-25, discuss):** If we would add back the columns, would this mean that in the pipeline they would still be dropped for models during training whenever we know that we wouldn't face these columns in test?

   **Answer (AI, 2026-11-25):** no: nothing in the pipeline drops a column that the test rows lack. The model trains on it and then gets it as missing in every test row, and in the 2011-2012 window this costs a model that does not check 1.9 RMSE points.

   * **Problem:**
     - The definition ships one table and, per window, the row numbers of its training and test sides. Every window has the same columns, and nothing in `data_foundry.v2` drops a column per window. `splits_feature_missing_in_test` only warns: it fires when a column is at least 95% missing on one side and at most 50% missing on the other. Accepting it changes nothing in the data.
     - So the model gets the column with its values on the training rows and as missing on every test row. A standard preprocessing step fitted on the training rows keeps it. AutoGluon 1.6.3's default feature pipeline, run on these windows, drops a column only when the training side lacks it: hip in every window, and the sagittal diameter in 2011-2012. It keeps the skinfolds, thigh and calf, which are missing in every test row.
     - A method could drop such columns itself, since the test rows' inputs are known at prediction time, or impute them. Doing so is the method's choice, not the framework's.
     - The cost depends on the window. In 2011-2012 every training row has the skinfolds, thigh and calf, so the trees never learn a missing branch and send every test row down a default one. In the later windows the 2011+ training rows lack the same measures, so missing already stands for the newer cycles.
   * **Experiments:** untuned LightGBM, 3 seeds, RMSE in percent-fat points (lower is better), on the definition's rows:

     | Window | a Common measures (implemented) | b All six, missing where not taken | b, the method drops the columns its test rows lack | Columns missing in every test row | Columns missing in every training row |
     |---|---|---|---|---|---|
     | 2017-2018 | 3.398 | 3.493 | 3.398 | skinfolds, thigh, calf, sagittal diameter | hip |
     | 2015-2016 | 3.324 | 3.333 | 3.309 | skinfolds, thigh, calf, hip | hip |
     | 2013-2014 | 3.371 | 3.431 | 3.365 | skinfolds, thigh, calf, hip | hip |
     | 2011-2012 | 3.427 | 5.357 (bias +3.43) | 3.427 | skinfolds, thigh, calf, hip | sagittal diameter, hip |

     The third column equals adding the sagittal diameter alone (option d): it is the only one of the six that some windows hold on both sides (2013-2014 and 2015-2016).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Common measures only (implemented) | 11 features | no column a test row lacks; scores as above | drops the sagittal diameter that the 2013 and 2015 test rows carry; rests on a reason the decision of 2026-11-11 turned down |
     | b | Keep all six | 17 features; `splits_feature_missing_in_test` accepted | follows the decision of 2026-11-11; the data as published | four columns (the skinfolds, thigh, calf) are missing in every test row of every window, and hip has no training row in any; the framework passes them as missing; a method that does not drop them loses 1.9 points in 2011-2012, so that window ranks methods by how they handle a column the test rows lack |
     | c | Keep the tape measures | Thigh, calf and hip; the use case read as tape and scale | the use case stays strict | thigh and calf are 1999-2006 only, so c has b's 2011-2012 problem; drops the sagittal diameter |
     | d | Keep the sagittal diameter only | Adds the 2011-2016 sagittal diameter (12 features) | the one era-only measure that test rows carry; better by 0.006 to 0.015 in two windows; no column that every test row lacks | departs from the decision of 2026-11-11 for five columns: no test row has the four 1999-2006 measures, no training row has hip; adds a caliper measure to a tape-and-scale question |

   * **Recommendation:** d. It brings back the only measure a test row can use. Of the five columns it leaves out, four are missing in every test row of every window and hip in every training row, so no window can use them, and with them the 2011-2012 score would depend on a method's missing-value handling rather than on body fat[^i2c]. Choose b to follow the decision of 2026-11-11 without an exception. **Decision:** a, b, c or d?

   [^i2c]: **CLEAN-22** (Must): columns leave for what they are, never for how many there are. The cross-dataset item of 2026-11-11 (A) kept columns that start or stop within the history. Here four columns stop before the first test window, so no test row has them, and hip starts in the last test window, so no training row has it.

   **Andrej (2026-11-25, discuss):** Reply (d): Keep the sagittal diameter only

   **Resolved (2026-11-25, Andrej):** d: the sagittal abdominal diameter (`BMDAVSAD` in BMX_G to BMX_I, "Average Sagittal Abdominal Diameter (cm)") is an input again as `sagittal_abdominal_diameter_cm`, 12 features; the skinfolds, thigh, calf and hip stay out. The notes say where it is missing (every row of 1999-2006 and 2017-2018, 1% of 2011-2016) and why it ships (the 2013-2014 and 2015-2016 windows hold it in training and test rows); `question`, `known`, `changes` and `fit_reason` name it. `splits_feature_missing_in_test` fired on the 2011-2012 window (no training value, 1% missing in test) and is accepted with the CC date. Measured: the 2013-2014 and 2015-2016 windows gain 0.004 and 0.012 RMSE points; in 2017-2018, whose test rows all lack it, RMSE is 3.405 against 3.350 without it and the Asian level's mean error turns from +0.58 to -0.91 points (comments). `dataset check`: 0 errors.

3. **Set the `Selection Bias` marker?**

   * **Problem:**
     - Many of the heaviest people have no usable scan: in 2017-2018 only 50% of examined adults aged 20-59 with BMI 40 or more have one, against 75% of those below BMI 30.
     - Completed scans without a whole-body value grow from 4.8% of 2011-2012 to 15.6% of 2017-2018, and these people are heavier (median BMI 29.9 against 25.7).
     - No one aged 60 or over is in a test window, and pregnant women and people over the table limit were never scanned.
   * **Effect on the task:** an equation is tested on fewer very heavy and no older people than a clinic meets; the obesity call for BMI 40 or more is rarely in doubt, and LightGBM's RMSE there (2.99 to 3.39) is no worse than overall (domain practitioner).
   * **Panel:** the domain practitioner, the claim auditor, the advocate and the critic recommend setting it; the fit stays direct.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No marker (implemented) | The selection stays in the notes and `fit_reason` | none found | the record hides a selection the notes document |
     | B | Set `Selection Bias` | Adds the marker to the record | flags the thinned heavy tail and the missing older people where the curator looks first | none found |

   * **Recommendation:** B; the definition already names the gap in `fit_reason` and the notes[^i3a]. **Decision:** A or B?

   **Notes for the AI:** B: add `Selection Bias` to the record's `decision_markers` with a CC line; nothing changes in the definition.

   [^i3a]: selection.md, "Selection bias": rows not drawn from the population the use case predicts for are marked `Selection Bias`, a concern flag, usually on a `Yes` record; name the gap in `fit_reason` and give the evidence in the record.

   **Andrej (2026-11-25, change):** Option B: Set Selection Bias.

   **Resolved (2026-11-25, Andrej):** B: the record carries `Selection Bias` (the thinned heavy tail, no one aged 60 or over tested, pregnant women and people over the table limit never scanned), with a CC line; nothing changed in the definition, whose `fit_reason` and notes already name the gap.

4. **Keep the sagittal abdominal diameter, now that every 2017-2018 test row lacks it?**

   * **Problem:**
     - The answer behind issue 2's choice (d) said the diameter leaves no column that every test row lacks, but it does: CDC measured it in 2011-2016 only, so every 2017-2018 test row lacks it while 38% of that window's training rows have it.
     - On that newest window the diameter makes the score worse (LightGBM RMSE 3.405 with it, 3.350 without) and turns the correction for Non-Hispanic Asians into an over-correction, since every Asian training row has the diameter and none of those test rows does.
     - Keep the diameter as applied, or drop it again (issue 2's A)?
   * **Experiments:** LightGBM, 5 seeds, the definition's four windows, RMSE in percent-fat points (lower is better); the Asian rows' mean error is measured minus predicted, for the 544 Non-Hispanic Asian test people of 2017-2018:

     | Window | With the diameter (as applied) | Without it |
     |---|---|---|
     | 2017-2018 | 3.405 | 3.350 |
     | 2015-2016 | gains 0.012 over without | |
     | 2013-2014 | gains 0.004 over without | |
     | 2011-2012 | 3.434 | 3.434 |
     | 2017-2018 Asian rows, mean error | -0.91 | +0.58 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep the diameter (implemented) | as issue 2 (d) applied it | gains 0.004 to 0.012 on the 2013 and 2015 windows | worse on the newest window (+0.055), and the Asian rows over-corrected there; the newest window is the deployment period |
     | B | Drop it again | issue 2's A: the eleven measures every cycle shares | no column missing in a test window; the newest window scores best | gives up the small gain on 2013 and 2015 |

   * **Recommendation:** B: the newest window is the period a deployed model faces, and there the diameter hurts; the gain elsewhere is under 0.015. **Decision:** keep A, or change to B?

   **Notes for the AI:** on B, remove `BMDAVSAD` / `sagittal_abdominal_diameter_cm` from `_clean` and the features, drop the acceptance of `splits_feature_missing_in_test`, restore the eleven-measure notes and re-run `dataset check` and the task probe. Numbers from the run that applied issue 2 (d) on 2026-11-25.

**Review panel:** ship after changes (mediator). Full panel. Claims: 27 tested, 21 hold, 2 refuted (the 90 people with a varying imputed label, fixed; the eras' different scan rules, issue 1), 4 untested or open (the no-gap reason and the metric's weighting, both fixed in the notes). Blind review: include with changes; its main concern, how the imputed scans were handled, is answered by the filter. Task gamer: no exploit above noise. Agreed: no leak, the split leaf, four windows, the 90-row filter, the non-Hispanic Asian level, the notes. Disputed: the 893 scans with an invalid region (issue 1), the measures taken in some cycles only (issue 2). The reports cite the builder's draft issues: its issue 1, the scanner break, is now the horizon (H); its issue 2 is issue 2; its issue 3, the children, stays as built (kept) and is not raised.

<details><summary>Mediator</summary>

**Verdict: ship after changes.** Five changes need no decision. Two calls, plus the `Selection Bias` marker, go to the curator. The panel found no leak, and both sides argue for shipping.

**Judgment record**

```text
Verdict: ship after changes.
Validity: SEL holds; USE-1, USE-3 hold (direct fit, actor = clinician or epidemiologist, the prediction point is the exam);
  USE-5 triggered, fixed (drop the 90 people whose "measured" label varies across the five _MULT_ records);
  LEAK-10 holds (only DXDTOPF is read from DXX; task gamer: no exploit above noise);
  SPLIT-1, SPLIT-36 hold (Survey → SUR.meets → L-ORDER.windows, nothing forced); SPLIT-15 (Should) triggered, fixed
  (n_windows=4: the 2011-12 window trains on 55.1%, above SPLIT-14's floor; a change in data collection is a reason
  to test it); SPLIT-10 holds (no gap: same-day scan);
  CLEAN-1 / P5 era asymmetry (893 partly invalid 2011-18 scans kept): a weighing call → curator, issue 1.
Value: TP holds (LightGBM RMSE ≈3.39 against 8.4-8.8 for the dummy and 4.3 for linear; folds of 3,658-5,056);
  MET-5 → fallback rmse, MET-1 met with a note (unweighted, unlike the source).
Quality: CLEAN-22 (Must) + the settled item of 2026-11-11: dropping the six era-only measures departs from precedent
  → curator, issue 2. CLEAN-19: add a Non-Hispanic Asian level (cheap, safe, from the source).
Weighed: size +, reference-method target +, source +; selection (no test rows aged 60+, heavy tail thinned) -.
For the curator: issue 1 (drop or keep the 893 scans with an invalid region), issue 2 (which era-only measures stay),
  issue 3 (Selection Bias marker).
```

**Changes to make now (no decision needed)**

1. **USE-5 / P5, the 90-row filter.** Keep a 1999-2006 person only if `DXDTOPF` is the same in all five `_MULT_` records. This drops 80 people of 2003-04 and 10 of 2005-06, all training rows. In `_clean`, correct the comment "the measured values are the same in all five", and correct the "measured scans only" note.
2. **SPLIT-15, four windows.** Set `n_windows=4` and rewrite `splits_comment`. The count rests on data statistics only (55.1% train share, the 4,521 test people, the drift PSI 0.836), never on a model's RMSE. Name the target (9), the count reached (4) and what stops a fifth (2005-06 would train on 42.8%, below the floor). Accept `splits_below_target` with that reason.
3. **SPLIT-10, the no-gap reason.** Rest "no gap" on the same-day scan alone. Add that the 2011-18 values are CDC's March 2020 Apex re-analysis. Drop both "known when the next cycle starts" and the RMSE argument.
4. **CLEAN-19 / CLEAN-1, ethnicity.** From 2011, take `RIDRETH3` with its "Non-Hispanic Asian" level. Add a note that Asians in earlier cycles stay in "Other race". Measured effect: the bias for Asian people in the 2017 test window falls from +0.98 to +0.58 points.
5. **Notes (EV-2, MET-1, USE-8):**
   * Metric reason: the source's RMSE was survey-weighted and pooled over the imputations; ours is unweighted on measured scans, because a clinician scores the patient in front of them (precedents MET-16 and `anes_voting_2026`).
   * Rewrite the `Selection Bias` note:
     * the eras do not drop the same scans (see issue 1);
     * completed scans without a percent fat grow from 4.8% of 2011-12 to 15.6% of 2017-18, and these people are heavier (median BMI 29.9 against 25.7);
     * only 50% of adults with BMI ≥ 40 have a usable scan in 2017-18, against 75% below BMI 30.
   * `use_case`: the tested population is aged 8-59.
   * Record's screening block: "71%" becomes 76%, and the 5% lean-to-fat shift applies to both eras.

**Issues for the curator, ranked**

**1. The 893 scans of 2011-18 with an invalid region: keep or drop (validity, P5 / CLEAN-1 Should; a weighing call).**
- **Problem:** 1999-2006 drops every scan with an invalid region, because CDC imputed those. 2011-18 keeps them, because CDC still publishes a whole-body total: 893 rows, 8.9-10% of the 2017-18 test window. 149 of them have the trunk coded 3, "excessive x-ray noise due to morbid obesity".
- **Effect:** ranking: none measured (RMSE on valid rows 3.37 against 3.38; training on valid scans only, 3.410 against 3.417). These rows are harder (3.78 against 3.38) and heavier (median BMI 33.6).
- **Advocate, keep with a note:** it is the mildest remedy; the label is CDC's own published value; dropping thins a heavy tail that is already under-covered. Both auditors who measured it recommend this.
- **Critic, drop (at least the trunk-noise rows):** dropping is the only rule that treats both eras the same, since no measured total exists for such scans in 1999-2006. The critic accepts "keep with a note" if the curator picks it.
- **Why it is not mine to settle:** no Must is triggered and no rule ranks one side above the other. It is a trade between a label that includes a region CDC calls inaccurate and keeping the heavy people in the test set.
- **My lean:** keep with a note. It is the lower rung of the remedy ladder, and the measured effect is nil.
- **Decision:** (a) keep with a note, (b) drop all 893, or (c) drop only the trunk-code-3 rows.

**2. The six measures taken in some cycles only (CLEAN-22 Must; the cross-dataset item resolved 2026-11-11 by Lennart, A).**
- **Disputed fact, settled by my count** (measured on the rows the definition keeps):

  | Measure | Kept rows with a value | Use in the shipped windows |
  |---|---|---|
  | Thigh, calf, triceps and subscapular skinfolds | 1999-2006 only (4,145-6,400 per cycle) | training rows only |
  | Sagittal diameter | 2011 (4,470), 2013 (4,990), 2015 (4,555) | on both sides of the 2013 and 2015 windows, and of 2011 once four windows ship |
  | Hip | 2017 only (3,062 of 3,658) | test rows only, no training row |

  The advocate's claim that none of these columns could inform a test prediction is false for the sagittal diameter; the critic is right.
- **Rule:**
  * "Taken in some cycles only" is the reason the settled item rejected. The LightGBM comparison is inadmissible (EV-4).
  * "Needs calipers" is not one of the reasons CLEAN-22 names for dropping a column (a leak, an identifier, a copy, the measurement that defines the label). It is a P3 argument: the actor would not have the input. It holds only if the use case is "tape and scale".
  * That framing is a call the rules leave to the curator. Skinfold equations are standard field practice, and the domain practitioner names clinicians, not gyms, as the actors.
- **Advocate, option (c):** drop the skinfolds and the sagittal diameter as caliper measures, keep thigh, calf and hip.
- **Critic, option (b):** keep all six, missing where not taken, and accept `splits_feature_missing_in_test`. The critic accepts (c) only with a CC line confirming tape-and-scale and a note that the sagittal diameter exists in three test cycles.
- **Agreed by both:** thigh, calf and hip stay. No fact sets them apart from `onlinenewspopularity`'s `kw_min_min`.
- **Decision:**
  * (b) keep all six; or
  * (c) keep thigh, calf and hip, and drop the caliper measures with a CC line that sets the use case to tape and scale.

  Either way the CC date accepts `splits_feature_missing_in_test`. Plain A, as built (drop all six), has no fact behind it.

**3. The `Selection Bias` marker (SEL, Weigh/flag).** The domain practitioner, the claim auditor and both sides recommend setting it. The marker is the curator's to set. Decision: set it, yes or no.

**Agreed facts**

- 39,691 people, `SEQN` unique, per-cycle counts as in the notes. No leak: every feature is taken at the exam, and only `DXDTOPF` is read from the scan file.
- 90 kept 1999-2006 people carry a label that varies across the five imputation records (up to 4.6 points in 2003-04, 0.1 in 2005-06).
- 893 kept 2011-18 scans have an invalid region. Dropping them does not change the score (3.37 against 3.38).
- The 2011-12 window trains on 55.1%, above SPLIT-14's floor; 2005-06 would train on 42.8%, below it. The current reason for three windows uses a model's score, which SPLIT-15 bars.
- The scan is taken the same day as the measures. Every 2011-18 DXX file shows "First Published: March 2020".
- The test cycles hold ages 8-59 only. "Other race" goes from 3-5% of training rows to 16-23% of test rows, 67-77% of them Asian.
- RMSE is the right metric (MET-5 fallback, MET-8). The source's version was survey-weighted.
- Fit: direct (USE-8).

**Task gamer exploits (none is an issue).** The definition has no `Potential leak, kept on purpose:` notes and no accepted warnings, so none of these is a known exploit with a stated gain.
- **#1 and #2, each feature's percentile rank or distance from the mean within its own cycle, test rows included:** LEAK-30's mechanism, applied by the participant; no column is scaled at the source. New, measured gain +0.006 and 0.000, within the noise of a random column (+0.001 to +0.006). No issue.
- **#3, global ranks:** a control, not an exploit.
- **Looking up rows in the public NHANES files:** true of every public source (PROV). Not ranked, not specific to this dataset. No issue.
- **`survey_cycle` worth 0.03 RMSE:** the time key, known at deployment (USE-3). Legitimate.
- **The gamer's open point on imputed targets:** answered by change 1.

**Consistency with precedent**

- **Follows precedent:**
  * the split regime and the unweighted metric (`anes_voting_2026`, MET-16);
  * both eras in training (REVIEW 2026-11-11, "the data as the deployed model met it");
  * dropping CDC's imputed scans (CLEAN-2; CDC: "should not be treated as measured variables");
  * keeping the children;
  * fallback RMSE (`body_density_prediction`).
- **Four windows:** brought back in line with SPLIT-15 and `anes_voting_2026` (precedent checker, finding B). If the curator keeps three, it becomes an exception with a CC fact: the AI's best guess is that a window trained on the old scanner alone measures a calibration shift no deployed equation meets.
- **The era-only columns (finding A):** dropping all six departs from the settled item of 2026-11-11 (`onlinenewspopularity` and six others kept theirs). Options (b) and (c) above follow it for the tape measures. Option (c) needs the use-case fact as a recorded exception (CLEAN-22, P3).
- **`anes_voting_2026`'s inherited drop rule** (questions asked in only some years left out) is a counter-precedent. It was not raised as a reason here, and resolving it would be an amendment (precedent checker, option d), not this dataset's call.
- No third exception of any reason, and no drift in a curator's decisions.

</details>

<details><summary>Claim audit</summary>

I tested 27 claims for `nhanes_dxa_body_fat`. Two are refuted, both about which scans count as "measured", and neither touches the leak, the split or the metric. Four are untested or open, and the rest hold.

**Claims tested**

| # | Claim | Where | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | 39,691 people: 21,858 in 1999-2006 and 17,833 in 2011-2018, with the eight per-cycle counts | curation_comments, screening | Rebuilt the frame from the definition | holds | 4,671 / 6,425 / 5,877 / 4,885 / 4,521 / 5,056 / 4,598 / 3,658 | EV-2 |
| 2 | 5,401 people with an imputed scan were dropped | curation_comments | Counted flag ≠ 0 with a percent fat, on imputation record 1 | holds | 1,207 + 1,196 + 1,414 + 1,584 | — |
| 3 | "The measured values are the same in all five" imputation records, so the flag `DXITOT` = 0 means a measured percent fat | `_clean` step 1–2, curation_comments | Spread of `DXDTOPF` across the 5 records per person where the flag is 0 | **refuted** | 2003-04: 80 people with `DXITOT` = 0 and all 12 regional flags 0 still have a different `DXDTOPF` in each record (median spread 1.65 points, max 4.6). DXX_D says people with fully valid data "have 5 identical records". 2005-06: 10 more people have soft-tissue flag 0 but bone flag `DXITOTBN` = 1, and their percent fat varies by 0.1 | PROV / LEAK-free; target fidelity (P5) |
| 4 | Only measured scans are kept, and both eras miss the heaviest people "the same way" | curation_comments (Selection Bias), screening | Read the 2011-18 invalidity codes (`DXA*V`) on the rows we keep | **refuted (asymmetry)** | In 1999-2006 a scan with any invalid region was imputed, so we drop it. In 2011-18 CDC still publishes a total percent fat when a region is invalid (DXX_J: "If any region was coded as invalid all bone and soft tissue measurements for that region were set to missing"), and we keep those rows: 893 kept rows (140 / 148 / 241 / 364 per cycle; 10% of the 2017-18 test fold). In 2017-18, 149 of them have trunk code 3, "Excessive x-ray noise due to morbid obesity". Their median BMI is 33.6, against 24.9 for fully valid scans. LightGBM test RMSE on them is 3.78 against 3.38 (2017) and 3.68 against 3.31 (2015). In 1999-2006 the same kind of person (heavy, partly invalid scan) is dropped | SPLIT-1 / P5 (same row definition in train and test) |
| 5 | Pregnant women were not scanned | curation_comments | `RIDEXPRG` = 1 among kept rows | holds | 0 in every cycle | — |
| 6 | Table limit 300 lb in 1999-2006, then 450 lb and 6 ft 5 in | curation_comments | DXX_D and DXX_G text; maximum measured weight | holds | DXX_D "over 300 pounds", DXX_G "over 450 pounds or height over 6'5"". Max weight 138–142 kg in 1999-2004 (a self-reported limit), 188.5 kg from 2011 | — |
| 7 | DXA ages: 8-85 in 1999-2004, 8-69 in 2005-06, 8-59 in 2011-18 | curation_comments, splits_comment | Min and max of `RIDAGEYR` per cycle | holds | 8–85, 8–69, 8–59 | — |
| 8 | The 5% shift of lean to fat mass is in both eras; the break is the scanner and its software | curation_comments | Text of DXX_D and DXX_G/J | holds | DXX_D: "lean mass was decreased by 5%". DXX_G and DXX_J: "NHANES BCA option was enabled … adds 5% of lean mass to the fat mass". Software: 8.x, then Discovery v12 from 2005, then Apex | — |
| 9 | Correction to the screening block (it reads as if the 5% shift were 1999-2006 only) | builder report | Same text as #8 | holds: the record's screening block is wrong on this | — | writing |
| 10 | Missing measures: 0.3% to 0.9% per measure | curation_comments | `isna` on the frame | holds | 0.29% to 0.86% | — |
| 11 | No row repeats; 4 rows share every feature but differ in target | curation_comments, check | Grouped on all features | holds | 7 rows share every feature with another row; `SEQN` is unique (assert) | — |
| 12 | No copies across the split | implied | NHANES draws a new sample each cycle; `SEQN` is unique across cycles | holds | assert passes | PROV / SPLIT |
| 13 | BMI is weight over height squared as CDC computes it | curation_comments | Builder's recompute | holds | Max difference 0.05 | — |
| 14 | Features are known at the examination, and the scan is taken the same day | curation_comments | Codebooks: BMX and DEMO come from the same MEC exam; no DXA column is read | holds | Only `DXDTOPF` and the status and flag columns are read from DXX | LEAK-10 |
| 15 | Split: three windows (2017, 2015, 2013) with train shares 90.8%, 79.2%, 66.5% | splits_comment | `flat_splits` | holds | 36,033/3,658; 31,435/4,598; 26,379/5,056. Every test fold holds one cycle only | SPLIT-15 |
| 16 | No gap: "every training label is known when the next cycle starts" | splits_comment | DXX_G to DXX_J pages | **untested / weak** | The scan is taken the same day, so the label exists then. But every 2011-18 DXX file shows "First Published: March 2020" (all re-analysed with Apex), so the labels as shipped were public only after the last test cycle. I could not find the original release dates | SPLIT gap rules |
| 17 | The RFM paper validated forward, developing on 1999-2004 and validating on 2005-06 | record, splits_comment | Europe PMC full text of PMC6054651 | holds | Quote verified | SPLIT-34 |
| 18 | Metric fallback: RFM selected its model on R², RMSE, AIC, accuracy, precision and simplicity together | metric reason | Same full text | holds | "Model selection was based on … (R²) …, the lowest RMSE, the lowest Akaike information criterion …, accuracy and precision, and the simplicity" | MET-5, MET-8 |
| 19 | Lee et al. 2017 report R² and the SEE | metric reason | — | **untested** (abstract only, not fetched) | — | MET-1 |
| 20 | RMSE is computable: no inputs, every fold scorable | metric (MET-2) | Fold sizes; a dummy (training mean) RMSE per fold | holds | Folds hold 3,658 to 5,056 rows; dummy RMSE 8.77, 8.70, 8.44 | MET-2 |
| 21 | Target scale: percent-fat points, identity transform | metric (MET-3) | `MetricSpec` | holds | `target_transform='identity'` | MET-3 |
| 22 | The metric means what the source's meant | MET-2 | Compared with RFM | **open (weighing)** | RFM's RMSE is survey-weighted ("probability weights for all analyses") and pools all 5 imputations with Rubin's rules. Ours is unweighted on measured scans only. Same target and scale, but a different population and a different weighting | MET-1, MET-2 |
| 23 | Survey weights are not needed for a prediction score | screening | — | **open (weighing)** | Unweighted RMSE over-represents the groups NHANES oversamples. Defensible for a clinician's patients, but the source did weight | MET-1 |
| 24 | First publication is 2008 | `Source.year` | dxx99 documentation | holds | "First Published: January 2008" | PROV |
| 25 | 71% of people with BMI ≥ 40 in 1999-2006 have an imputed scan; median BMI imputed 28.5 against measured 24.8 | screening | Recomputed on imputation record 1 | holds in direction, number off | 76% (13% below BMI 25); medians 28.5 and 24.8 match | EV-2 |
| 26 | Children are about 39% of the test cycles | builder report | Share of age < 20 in the 2017 test fold | holds | 38.5% | — |
| 27 | First DXA publication 2008 and the 24 download URLs | builder report | Raw files present (24 `.xpt`) | holds | — | — |

**Refuted claims, ranked (all validity, P5 then P4; none is a leak)**

**1. 90 rows in 1999-2006 carry an imputed percent fat although the definition calls them measured (#3).** This is a Should-level fidelity problem with a small blast radius: 0.2% of rows, all of them training rows. The 80 people of 2003-04 look like a flag error in DXX_C. Their percent fat differs by up to 4.6 points between imputation records, so the value we ship is one model draw (record 1). The 10 of 2005-06 are cases where the definition reads only the soft-tissue flag `DXITOTST` and ignores the bone flag `DXITOTBN`. They change by 0.1 point, which is cosmetic.
- **What it changes:** the comment "the measured values are the same in all five" is false, and so is the curation note that only measured scans are kept.
- **Mildest remedy:** in `_clean`, keep a person only if `DXDTOPF` is identical across their five `_MULT_` records. This drops the 90 rows and covers both causes. Also correct the comment.

**2. The two eras do not apply the same row filter, so "both eras miss the heaviest people the same way" is false (#4).** The asymmetry:
- In 1999-2006, any invalid region led CDC to impute the scan, and we drop it.
- In 2011-2018, CDC publishes a total for scans with an invalid region, and we keep them.

This adds 893 heavy-skewed rows to the new era only, 10% of the 2017-18 test fold (median BMI 33.6, 149 of them with trunk "obesity noise").

- **Effect on the score:** these rows are harder (RMSE 3.78 against 3.38 in 2017). Dropping them everywhere leaves the RMSE on valid rows essentially unchanged (3.37 against 3.38), so the benchmark ranking is unlikely to move. Their totals still include a region that CDC itself calls "could not be analyzed accurately".
- **What it changes:** the Selection Bias note, and the claim that the row definition is the same across the split.
- **Options for the curator** (a weighing call between faithful labels and a representative heavy tail):
  - (a) **The mildest remedy, and my recommendation:** keep the rows and rewrite the note. The new era keeps partly invalid scans, the old era loses them, and the test folds are heavier than the training rows for that reason.
  - (b) Require every 2011-18 invalidity code to be 0 for both eras to apply the same filter. This costs 893 rows and thins the heavy tail of the test folds further.

**Untested or open, ranked**

**3. The metric's meaning against the source's (#22, #23).** This is a weighing call (MET-1), not a refutation. The fallback RMSE is justified under MET-5, and I verified the RFM quote. The source's RMSE was survey-weighted and pooled the imputations; ours is unweighted on measured scans only. Mildest remedy: one sentence in the metric reason saying the source's RMSE was design-weighted and ours is not, and why (a clinician meets the patients in front of them, not the US population).

**4. The no-gap claim (#16).** The label is realized the same day, so no gap is defensible. Still, every 2011-18 label as shipped was published in March 2020, after the Apex re-analysis, so it was not public "when the next cycle starts". The builder also could not establish the original release dates. Mildest remedy: write in the splits comment that the 2011-18 values are a 2020 re-analysis and that no gap is applied because the scan is same-day, not because of the release dates.

**5. Lee et al. 2017 metrics (#19).** Not fetched. It does not affect the fallback, since RFM alone already shows no single metric.

**Smaller corrections**

- The record's screening block says "71%" where the recount gives 76%.
- The screening block also reads as if the 5% shift were 1999-2006 only (the builder already caught this).

</details>

<details><summary>Column audit</summary>

I found no leak. There are two moderate cleaning findings for the curator; neither blocks shipping. The dtype probe flags 0 of 11 columns, and no feature's missing share moves by cycle.

**Scope.** I read `dataset.py`, the record's 2026-11-25 screening block, the builder's report and check log, and the DXX_G codebook. I checked against the raw `.xpt` files and ran the dtype probe. LightGBM experiments re-ran the three shipped windows, training on every earlier cycle with 400 trees.

**Prediction point:** the examination, once the tape and scale measures are taken. The scan is the same day.

**Files of the release**

- **Read:** DXX, BMX and DEMO for the eight cycles with whole-body DXA.
- **Left out, with a reason in the notes:** the other DXA files (android/gynoid, femur, spine), the survey weights and the "Supplemental Highly Variable Data" files.
- **No newer DXA:** `P_DXX` (2017 to March 2020), `DXX_L` and `P_DXXAG` all return 404 today. 2007-2010 ran no DXA.
- **Finding:** none.

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| survey_cycle | first year of the two-year NHANES cycle (from the file suffix, asserted equal to `SDDSRVYR`) | yes | int64, 8 values; also the time key | fine (a numeric cycle makes linear models extrapolate, which is a modelling matter, as the builder notes) | — |
| sex | `RIAGENDR`, 1 Male / 2 Female | yes | categorical, decoded to the codebook's words | fine | CLEAN-12 |
| age_years | `RIDAGEYR`, age in years at screening; top-coded at 85 in 1999-2006 | yes | int, 8-85; the test cycles are 8-59 | fine. Exact age at exam in months (`RIDAGEEX` / `RIDEXAGM`, recorded for 99.5% of under-20s in every cycle) made no difference: 3.423 / 3.339 / 3.375 against 3.417 / 3.332 / 3.371 | — |
| race_ethnicity | `RIDRETH1`, 5 levels | yes | categorical, decoded | **question for the curator** (problem 2): "Other race" shifts meaning between eras | CLEAN-1, CLEAN-19 |
| weight_kg | `BMXWT`, examination scale | yes | float, 16.9-188.5, 0.2-0.5% missing in every cycle | fine. About 0.4% of weights were taken in clothing (`BMIWT`=3, 3-21 people per cycle) and are not adjusted; that is measurement noise and needs no action | — |
| standing_height_cm | `BMXHT` | yes | float, 0.2-1.0% missing, stable | fine | — |
| bmi | `BMXBMI`, CDC's weight/height² (recomputed: within 0.05) | yes | float; redundant, not a leak | fine | — |
| upper_leg_length_cm | `BMXLEG` | yes | float, 0.6-1.3% missing | fine | — |
| upper_arm_length_cm | `BMXARML` | yes | float, 0.3-0.8% missing | fine | — |
| arm_circumference_cm | `BMXARMC` | yes | float, 0.3-0.8% missing | fine | — |
| waist_circumference_cm | `BMXWAIST` | yes | float, 0.5-1.0% missing (`BMIWAIST`=1, could not obtain) | fine | — |
| percent_body_fat (target) | `DXDTOPF`, whole-body percent fat | — (same-day scan) | float, 11.5-56.2 | **cleaning problem** (problem 1): "measured" is defined differently in the two eras | CLEAN-1 |

**Columns not read (all correct):**
- Regional fat, lean and bone values of the scan: outcomes of the same scan (LEAK-10).
- `_MULT_`, `DXITOT` and `DXAEXSTS`: used only to filter rows.
- `RIDEXPRG`: pregnant women were never scanned.
- `RIDEXMON`: not a measurement of the person.
- Era-only measures (skinfolds, thigh, calf, sagittal diameter, hip): dropped with a reason in the notes.

No feature is recorded after the prediction point, none has missingness caused by the outcome, and none comes from a window, a later lookup or a fit over the whole release.

**Problems, ranked**

**1. The target's "measured" filter differs between eras (validity, CLEAN-1, Should).**
- **1999-2006:** a person is kept only when the total imputation flag `DXITOT` is 0. Every scan with an invalid region was imputed and is dropped; 0 kept rows carry a region flag in 1999-2004, and 19 do in 2005-2006.
- **2011-2018:** a person is kept when `DXAEXSTS` is 1. DXX_G says that for an invalid region "all bone and soft tissue measurements for that region were set to missing", but `DXDTOPF` stays filled. So 893 kept people (5.0% of 2011-2018) have a whole-body percent fat although at least one region was invalid:
  - 3.0% in 2011, 2.9% in 2013, 4.4% in 2015, **8.9% in 2017-18**, the newest test window;
  - in 2017-18, 149 of them have the trunk coded 3, "excessive x-ray noise due to morbid obesity". Earlier cycles have 0 to 5 such codes, so the coding practice changed;
  - these people run fatter (median percent fat 41.3 against 31.5 in 2017-18).
- **Effect on scores:** these rows score worse in the 2017-18 window (RMSE 3.77 against 3.38). Training on valid scans only barely moves the score (3.417 to 3.410).
- **The notes:** "Measured scans only" in `curation_comments` is therefore not exact for 2011-2018.
- **Mildest remedy:** keep the rows and state the difference in the notes and in the Selection Bias line. The alternative is to drop 2011-2018 scans with any tissue invalidity code ≠ 0, which matches the old era's rule but thins the heavy end further. This is the curator's call.

**2. `race_ethnicity` lumps Non-Hispanic Asians into "Other race" (validity / value, CLEAN-1 and CLEAN-19, Could–Should).**
- **How the category shifts:** from 2011, NHANES oversamples Asians and codes them in `RIDRETH3` (code 6). "Other race" grows from 3-5% of rows in 1999-2006 to 16-23% in 2011-2018, and about two thirds of it is now Asian: 560-619 people per cycle, 12-15% of each test window.
- **Why it matters for the use case:** Asians carry more fat at a given BMI, which is the known clinical reason for lower BMI cutoffs.
- **Experiment:** adding a "Non-Hispanic Asian" level from `RIDRETH3` (2011 on; it trains from 2011-12 in every window) gives:
  - RMSE 3.397 / 3.314 / 3.373 against 3.417 / 3.332 / 3.371 (2017 / 2015 / 2013);
  - in 2017-18, the Asian bias falls from +0.98 to +0.58 points and the Asian RMSE from 3.62 to 3.50.
- **Remedy:** add that level and state that older cycles' Asians remain in "Other race", or keep `RIDRETH1` and say in the notes why the coding of every cycle was preferred.

**3. Accepted as is, no action.**
- BMI duplicates weight and height (it is the field's own feature).
- Clothing-weighed rows are not adjusted (0.4%).
- Ages are top-coded at 85 in training only.
- The scanner break and the era-only features are covered by the builder's issues 1 and 2.

</details>

<details><summary>Split audit</summary>

**Verdict: right with notes.** The split matches the use case, and I found no leak in it. One rule point needs the curator: the definition leaves out a fourth test window, 2011-2012, that the rules allow. The other two notes need no change to the split.

**Tree walk (SPLIT-36)**

* **Collection type:** Survey.
* **[SUR.meets]** "the surveyed population at a later round". A body-fat equation is fitted on past people and used on people met later. The source tests this way itself: Woolcott and Bergman built the relative fat mass on 1999-2004 and validated it on 2005-2006. I also weighed the other answer, "people the survey did not sample" (the fill-in step). A measurement rules it out: the relation between the measures and body fat changes over time. A forward model trained on as many rows as a model fitted inside the test cycle does worse in every window:

| Window | Forward model, same training size | Model fitted inside the cycle |
|---|---|---|
| 2017 | 3.70 | 3.66 |
| 2015 | 3.58 | 3.49 |
| 2013 | 3.64 | 3.53 |
| 2011 | 3.76 | 3.55 |

* **[ORDER.order]** yes: the cycle is recorded (`SDDSRVYR`, which the code checks against the file).
* **[ORDER.windows]** yes: three or four one-cycle windows keep at least half the rows for training and thousands of people per test window.
* **[ORDER.small]** no: a random split would train on about 26,000 people, far above 2,500.
* **Leaf: [L-ORDER.windows].** This is the leaf in `split_leaf` and the `splits_comment`, and the definition ships a temporal split with the tag `Non-IID (Temporal)`. Nothing is forced, no leaf is new, and every question had an answer that fits.

**Collection facts and regime**

* **Collection facts:** `Samples: Over Time`, `Time: Dated`, entities do not recur. NHANES draws a new sample every cycle, so no person appears on both sides of a cut.
* **Household members:** they sit in the same cycle, so they always stay on one side.
* **Labels and inputs:** the scan is taken the same day, so no label is still open at a cut. No input is issued ahead of the time column. The raw row order does not matter here, because the cycle sets the order.
* **Time column:** the cycle is the moment the prediction is made (USE-3).
* **Regime:** a new person at a later round, which is what the definition declares.

**Problems, ranked**

**1. The fourth window, 2011-2012, is left out for a reason the rule counts in favour (SPLIT-15, Should; validity).**
* **Numbers:**
  * A random split would get 9 splits; 3 are shipped.
  * The 2011 window trains on 55.1% of the rows and tests 4,521 people, so it passes the half floor (SPLIT-14).
  * 2005-2006 is the only other candidate, at 42.8%: below the floor.
* **What the rule says:** within the floor, take as many windows as reach the target. SPLIT-15 names "a change of … the data collection" as a period a deployed model must handle, which argues for adding a window.
* **The definition's reason:** the `splits_comment` drops 2011 because it would "test the scanner change rather than later people". That is the same reason, read the other way.
* **What the window statistics show:**
  * The largest drift of all candidates: PSI 0.836, and race and ethnicity 0.38 against 0.16-0.18. This fits 2011's design change: as far as I know NHANES began oversampling Asian Americans in 2011, and they fall under "Other race" in the race variable. I did not check this against the source.
  * The largest forward-versus-inside gap in the stationarity test above: 3.76 against 3.55.
* **How it is used:** a model trained on older data alone and used after the measurement changed is how these equations are actually used. The relative fat mass was published in 2018 from 1999-2006 data.
* **The worry checked:** I did not use any model score to choose the window. The fear that 2011 only measures scanner noise does not show in the scores: LightGBM on 2011 gets RMSE 3.45 with a mean error of +0.25, against +0.42 on 2015.
* **Mildest remedy:** set `n_windows=4`. Or keep three windows with a CC line from the curator. This is the review's issue 1, option C; the evidence points to C rather than A.

**2. A growing share of heavy people drops out of the newest test windows (SEL, Selection Bias; Could).**
* Some completed scans (`DXAEXSTS` 1) have no whole-body percent fat, because one body region could not be read. That share grows every cycle:

| Cycle | Completed scans without percent fat |
|---|---|
| 2011 | 228 (4.8%) |
| 2013 | 390 (7.2%) |
| 2015 | 514 (10.1%) |
| 2017 | 678 (15.6%) |

* These people are heavier: median BMI 29.9 against 25.7.
* The newest cycle has 72% of 2013's rows a cycle, above the 60% warning line. Its mean body fat is 32.32, not lower than earlier cycles, so this is not a download cut.
* **Remedy:** add these numbers to the Selection Bias note; the split stays as it is.

**3. The survey cycle is a model input (note, no action).**
* In each test window the cycle is one value outside the training range.
* With the cycle column dropped, LightGBM changes by -0.03 to +0.08 RMSE; the builder saw a linear model extrapolate on it (10.80 on option B).
* This is a modelling matter, as the builder says.

**Horizon (for the review's horizon block)**

* **Window length:** one two-year cycle. This is the finest time the release holds (exam dates are not public), and it matches the source's own forward step. Stated by the source.
* **Gap:** none. The label comes from the same day's scan, which the source states.
  * **Our assumption:** the release lag of the DXA files is unknown. All 2011-2018 pages show "First Published: March 2020", a reanalysis with APEX v4.
  * **Measured:** a one-cycle gap raises RMSE by only +0.03 to +0.09, so no recent labels act as a shortcut (SPLIT-10).
* **Refit cadence:** in practice these equations are refit rarely, about once a decade (our assumption). The data cannot hold windows that long.
* **Time frame:** the newest windows sit in 2011-2018, the newest scanner era. NHANES ran no whole-body DXA after 2017-2018.

| Option | Test windows (test people) | Training share | Count |
|---|---|---|---|
| **1 cycle, no gap (implemented)** | 2017 (3,658), 2015 (4,598), 2013 (5,056) | 90.8 / 79.2 / 66.5% | 3 |
| 1 cycle, no gap, 4 windows (recommended) | the above plus 2011 (4,521) | … / 55.1% | 4 |
| 1 cycle, one-cycle gap | 2017, 2015, 2013 | 79.2 / 66.5 / 55.1% | 3 |
| 2 cycles, no gap | 2015-2018 (8,256), then 2011-2014 | 79.2%, then under the floor | 2: fails |

**Recommendation:** one-cycle windows, no gap, four windows.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner report: `nhanes_dxa_body_fat`**

I took the role of a primary-care or obesity-clinic physician, or a cohort epidemiologist without a DXA scanner. Either needs a body-fat percentage from a tape, a scale and a short interview, to decide whether a patient has excess adiposity or to use it as an exposure in a study.

**Fit: direct.** One row is one person at one examination. The inputs are what a tape, a scale and an intake form give. The label is the reference scan the equation replaces. The test data is people examined after the equation was fitted, which is how relative fat mass (RFM) was built and validated on these same files. I agree with `fit="direct"` under USE-1, USE-3, USE-5 and USE-8. The gaps below are real but narrow, and the `fit_reason` names the main ones.

**Metric scores the decision: yes (RMSE in percent-fat points).**
- An equation like this is judged by its standard error of estimate, which is RMSE, plus bias and limits of agreement. That is what Lee 2017 and Woolcott & Bergman 2018 report. I would pick the same metric.
- The obesity decision uses a threshold, but no single one exists. Cutoffs vary by source (25%/35%, Kelly 2009's NHANES references, percentiles for children) and differ by sex and age. Under MET-7 a range of thresholds is scored threshold-free, so a well-scored continuous estimate serves every cutoff (MET-8).
- The unit is the person, which is where I act (MET-1). MET-5 is applied correctly: both papers report several metrics, so the fallback is right.
- I would not choose a classification metric at 25%/35%.

**The five questions, as the actor**

1. **Inputs at the moment of prediction.**
   - I always have weight, height, BMI, waist, sex, age and self-reported ethnicity.
   - Mid-upper-arm circumference is routine in nutrition work. Upper-leg and upper-arm length are NHANES anthropometry that no clinic records. They are harmless (a tape gives them), but a model that leans on them could not run on my intake data.
   - I would normally also have hip circumference (waist-to-hip ratio) and often neck circumference (the US Navy formula). Here hip exists only in 2017-18 and neck not at all. Gyms in practice use bioimpedance or calipers, not this table, so the clinician and the epidemiologist are the right actors and the gym is a weak third.
   - `survey_cycle` is not something I would know as an input. It is "now" at deployment and mostly encodes the scanner era. This is acceptable as the time key.
   - No leak: every column is taken before or instead of the scan.

2. **Target.** DXA percent fat is the clinical reference for adiposity. The 2025 Lancet Diabetes & Endocrinology Commission on clinical obesity (Rubino et al.) accepts DXA or anthropometric confirmation of excess adiposity beyond BMI. So this is what I act on, not a proxy. I want a number, which I then compare with my cutoff. One caveat: this is Hologic DXA with NHANES's 5% lean-to-fat adjustment. A GE Lunar scan would read differently, so the label is "NHANES-calibrated DXA percent fat". That is the quantity the NHANES reference cutoffs use, so no change is needed.

3. **One row, one decision; is the test data what I would face?** Yes on the row. On the test data, new people examined later is the right framing (USE-10: a new entity, one row per person under USE-11). The test sample differs from my clinic in three ways:
   - **No one aged 60 or over in any test row.** Older adults are where BMI fails most (sarcopenic obesity) and where I most want the estimate. They appear only in training (1999-2006, older scanner) and are never scored.
   - **The heaviest people are thinned.** In the test cycles, adults aged 20-59 with BMI ≥ 40 have a usable scan in 50-70% of cases, against 75-86% for BMI < 30. 2017-18 is the worst: 10.6% of the examined have BMI ≥ 40, against 7.4% of those in the data.
   - This selection matters less than it looks. For BMI ≥ 40 the obesity decision is not in doubt, and LightGBM's RMSE there (3.0-3.4) is no worse than overall. The `Selection Bias` marker the builder suggested should be set. Under USE-8 the fit stays direct: a general-population screening setting shares most of this selection, and the people missing are the least-contested cases.

4. **Would I use it? Yes.**
   - On the test cycles, adults aged 20 and over: an untuned LightGBM classifies DXA obesity at 25%/35% correctly for 86-87% of people. BMI ≥ 30 manages 64-66%. That gap is the reason equations like RFM exist.
   - What would make me trust it: errors that are flat across sex, age and ethnicity, and validation on the people I see.
   - What would make me distrust it: the ethnicity issue in gap 2 below, and the missing older adults.

5. **Metric:** see above.

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. **Ages 60 and over are never tested (moderate).** The benchmark scores an equation for ages 8-59 only. That is a narrower population than the use case names ("a clinician … estimates body fat"), and it leaves out the group with the largest gap between BMI and fat. The cause is the source: DXA eligibility ended at 59 from 2011, so this is a scope note, not a fix. `task_summary.row` and `split` already say the test cycles hold ages 8-59. The `use_case` sentence could say the tested population is under 60.

2. **The ethnicity code changes meaning between train and test (low to moderate; fixable).** This is new evidence; it is not in the builder report or the record.
   - The definition uses `RIDRETH1`. Its category "Other race, including multi-racial" is 3-5% of the training rows from 1999-2006, but 16-23% of each test cycle.
   - The reason is that NHANES began oversampling Asian Americans in 2011. By `RIDRETH3`, 67-77% of the "Other" people in 2011-18 are non-Hispanic Asian, against a mixed residual group before.
   - Asian Americans carry more fat at a given BMI; that is why the WHO sets lower BMI cutoffs for Asian populations. A clinician would treat this group separately.
   - Measured with LightGBM (400 trees, 2 seeds, the shipped windows): mean bias on Asian test people is -0.58 / -0.10 / -0.98 points in 2013 / 2015 / 2017, against -0.16 / +0.49 / -0.19 for everyone else. Their RMSE is 3.26 / 3.54 / 3.62 against 3.37 / 3.33 / 3.42 overall. That is a systematic underestimate of about 0.4-0.8 points relative to the rest.
   - Possible fix: ship `RIDRETH3`. It has a non-Hispanic Asian category in 2011-18, and the pre-2011 rows would keep "Other, including Asian", or carry the coding as a separate feature. Every training side holds at least 2011-12, so models can learn the Asian category. Whether to do this is the curator's call. The cost is a category that is unknown, not wrong, before 2011.

3. **Missing inputs that a clinician usually has, and extra inputs a clinician lacks (low).**
   - Hip circumference is dropped because it is taken in one cycle only. That is right for the benchmark, but an expert's equation would use it.
   - Upper-leg and upper-arm lengths are survey-only. RFM shows height, waist and sex carry most of the signal, so the task does not hinge on them.
   - No change proposed; one clause in the notes ("leg and arm length are survey measures a clinic does not take") would be honest.

4. **Children are in the same task as adults (low).** Paediatric adiposity is judged against age- and sex-specific percentiles, and growth is fast enough that age in months matters. NHANES has `RIDEXAGM`, age in months at the exam, for people under 20. The paediatric RFM justifies keeping children (builder issue 3, recommendation A). An expert would add age in months for under-20s. This is optional and small.

5. **The scanner era (low; the panel already has it).** The QDR-4500A versus Discovery A break costs 4-8% RMSE, per the builder's issue 1. In practice I would retrain on the newest scanner, and the shipped split, with every window testing on Discovery A, mirrors that. I agree with the builder's option A.

6. **Ethnicity as an input at all (note only).** Race-based clinical equations are being withdrawn: eGFR in 2021, spirometry's GLI-Global in 2023. Some clinicians would not enter ethnicity. It is known at the prediction point, so it is legitimate under USE-6. Lee 2017 used it; RFM does not. Not a change, just context for the curator.

**What a domain expert would change**
- Use `RIDRETH3` with its Asian category, or add a flag for it (gap 2).
- Set the `Selection Bias` marker.
- Say in the use case that the tested population is aged 8-59.
- Optionally add age in months for under-20s.

I would not change the target, the metric, the split regime or the restriction to measured scans. Dropping CDC's imputed scans is right: an imputed percent fat is a model output, and scoring against it would grade a model against IVEware.

**Evidence** (measured)
- Coverage by BMI in the test cycles. Among examined people aged 20-59, not pregnant, the share with a completed scan and a percent fat: BMI ≥ 40 is 0.70 / 0.66 / 0.69 / 0.50, and BMI < 30 is 0.78 / 0.86 / 0.79 / 0.75, for 2011 / 2013 / 2015 / 2017.
- Share of "Other race" by cycle: 0.031, 0.037, 0.043, 0.047 for 1999-2005, then 0.178, 0.164, 0.167, 0.232 for 2011-2017. Of these, 0.77 / 0.71 / 0.73 / 0.67 are Asian by `RIDRETH3` in 2011 / 2013 / 2015 / 2017.
- LightGBM per window: 2013 / 2015 / 2017.

  | Measure | 2013 | 2015 | 2017 |
  |---|---|---|---|
  | RMSE | 3.37 | 3.33 | 3.42 |
  | Correct obesity call at 25%/35%, adults (model) | 0.86 | 0.86 | 0.87 |
  | Correct obesity call, adults (BMI ≥ 30) | 0.64 | 0.66 | 0.65 |
  | Obesity prevalence at 25%/35%, adults | 0.70 | 0.71 | 0.72 |
  | RMSE at BMI ≥ 40 | 3.39 | 3.20 | 2.99 |

**Sources**
- Read: `dataset.py`, the generated README, the record's 2026-11-25 screening block, the builder report, `issues/body_density_prediction.md`, `use_case.md` and `metrics.md`, and the CDC files `DXX`, `BMX` and `DEMO` (including `RIDRETH3`).
- Cited from domain knowledge, not fetched in this session:
  - NHANES 2011+ Asian oversampling (DEMO_G documentation)
  - Woolcott & Bergman 2018, Sci Rep 8:10980 (RFM)
  - Woolcott & Bergman 2019 (paediatric RFM)
  - Lee et al. 2017, Br J Nutr 118:858
  - Kelly et al. 2009, PLoS One (NHANES DXA reference values)
  - Rubino et al. 2025, Lancet Diabetes Endocrinol (clinical obesity commission)
  - WHO Expert Consultation 2004 on BMI in Asian populations
  - CKD-EPI 2021 race-free eGFR
  - GLI-Global 2023 spirometry

</details>

<details><summary>Precedent check</summary>

I found two departures from precedent among the builder's draft recommendations for `nhanes_dxa_body_fat`. Neither names a fact that sets this case apart. The other decisions follow their precedents. The decision register flags nothing on this dataset, and its flags on SPLIT-9, SPLIT-10 and SPLIT-14 are about other datasets. The curator hasn't decided anything yet, so I'm checking the AI's recommendations. I edited nothing.

**Per decision**

| # | Decision (builder's draft) | Verdict | Closest precedents |
|---|---|---|---|
| 1 | Survey → [SUR.meets] later rounds → [L-ORDER.windows] on `survey_cycle`; train on all earlier cycles, no gap | consistent | split_tree.md Survey step names `anes_voting_2026` and `sdss_17` for "the surveyed population at a later round". `anes_voting_2026`: one round per window, no gap because the label is known before the next round (CC 2026-11-11, Lennart). SPLIT-11 (train on everything before the window). The relative fat mass paper (Woolcott and Bergman 2018) itself fits on 1999-2004 and validates on 2005-06. |
| 2 | Issue 1 A: keep both scanner eras in training | consistent | SPLIT-11. The settled REVIEW.md item of 2026-11-11 (Lennart, A): keep "the data as the deployed model met it". `anes_voting_2026` trains across all of its studies. |
| 2b | Same issue: ship 3 windows; offer 2011-12 only as option C | **departs; the stated reason runs against the rule** | SPLIT-15. `anes_voting_2026` (9 windows, 4 of them under half, CC 2026-11-11 Lennart; exception signed 2026-11-19 Andrej). See finding B. |
| 3 | Issue 2 A: drop the measures taken in some cycles only (thigh, calf, 2 skinfolds, sagittal abdominal diameter, hip) | **departs; reason given for some columns, none for the tape measures** | REVIEW.md cross-dataset item "Accept `splits_feature_missing_in_test` where a column starts or stops being recorded" (Resolved 2026-11-11, Lennart, A, citing CLEAN-22, a Must). It was applied on 7 definitions. Closest pair: `onlinenewspopularity`, where `kw_min_min` is missing in every test window and kept. Also `delivery_eta_1m` issue 2 (2026-11-10). See finding A. |
| 4 | Issue 3 A: keep ages 8-19 | consistent | No precedent the other way. The paediatric relative fat mass was built on these same files. Fits task fidelity. |
| 5 | Keep measured scans only; drop CDC's multiply imputed ones | consistent | An imputed percent fat is a model's output, not a measurement (CDC: "should not be treated as measured variables"). LEAK-40 (`gallstone_disease`) is about fills in features, not in the target, so it does not apply. CLEAN-2: we do not impute. |
| 6 | Metric: fallback `rmse` in percent-fat points; survey weights not read, scoring unweighted | consistent | `body_density_prediction` (MET-8 fallback rmse). MET-16 and `anes_voting_2026` (unweighted, weights never a feature). |
| 7 | BMI kept beside weight and height | consistent | It is a column the source ships, not a leak; dropping it would need a "what it is" reason under CLEAN-22. |
| 8 | `Selection Bias` suggested in the notes, marker not set | no conflict | The marker is the curator's to set. |

**Finding A: dropping the era-only measures (issue 2) departs from the settled cross-dataset item**

Consistency check: should the measures NHANES took in some cycles only stay, missing where they weren't taken, as `onlinenewspopularity` and the six other definitions of 2026-11-11 kept theirs?

* **Problem:**
  - The draft recommends A: keep only the measures taken in every cycle, 11 features. The settled item (Lennart, 2026-11-11, A) kept every column that starts or stops within the history, "the data as the deployed model met it". It rejected dropping such columns because "removes information the deployed model has; departs from CLEAN-22".
  - Closest pair: `onlinenewspopularity`'s `kw_min_min` is present in training and missing in every test window, and it was kept. NHANES's thigh, calf and skinfold measures have the same shape: taken in 1999-2006, absent from all three test cycles.
  - The draft gives three reasons:
    1. "Taken in some cycles only": the very reason the item rejected.
    2. LightGBM scores worse with the columns kept (3.51 vs 3.42): a model score, which is no reason to drop a column (CLEAN-22, EV-4).
    3. "The skinfolds and the sagittal diameter need calipers, not a tape": a use-case fact. It covers 3 of the 6 columns. Thigh, calf and hip are tape measures.
  - A counter-precedent exists. `anes_voting_2026`'s code (from v1) drops questions that don't vary in the test years or appear in only one year. That would drop the skinfolds, thigh, calf and hip and keep the sagittal diameter. The precedents themselves are not uniform, so the curator should hear about both.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | Drop them, recorded as an exception with its fact. The AI's best guess at that fact: the deployed equation is used in a clinic with a fixed set of measures, not on the next survey cycle, so NHANES's changes of protocol are not something a deployed model meets (unlike `delivery_eta_1m` or `onlinenewspopularity`). Optionally add the caliper fact for the skinfolds and sagittal diameter. | Keeps the tape-and-scale use case exact; one feature set across eras | Needs the fact written in a CC line; thigh, calf and hip rest on (a)'s fact alone |
  | b | Treat it like `onlinenewspopularity`: keep all 6 columns, missing where not taken, and accept `splits_feature_missing_in_test` with the CC date | One rule for all eight datasets; the data as published | Thigh, calf and skinfolds never appear in a test row; hip appears in no training row |
  | c | Split it: drop the caliper measures (skinfolds, sagittal diameter) as outside the use case's tools, keep the tape measures (thigh, calf, hip) as recorded | Each column leaves for what it is | A narrower use-case reading that the curator has to confirm |
  | d | Amend the rule: a column absent from every test window (or from every training side) is dropped, which is ANES's rule written down | Settles the ANES vs `onlinenewspopularity` split | Reopens `onlinenewspopularity`'s decision of 2026-11-11 |

* **Recommendation:** (a) or (c), with the distinguishing fact written in a CC line. Not plain A as drafted: its main stated reason is the one the settled item rejected, and the score argument isn't admissible.

Rules: CLEAN-22 (Must). REVIEW.md "From the two new temporal checks of 2026-11-11", item 1. definitions.md row `splits_feature_missing_in_test` ("drop it, keep it as the deployed model met it, or start the data at the change; accept only with the curator's decision").

**Finding B: three windows when a fourth passes the floor (issue 1)**

Consistency check: should 2011-12 become a fourth test window, since SPLIT-15 asks for as many windows as the floor allows and names a change of data collection as a reason to test across it?

* **Problem:**
  - The target is 9 windows (`splits_below_target`). The 2011-12 window trains on 21,858 of 39,691 people (55.1%), above SPLIT-14's half floor. SPLIT-15 asks for "within them [the floor], as many windows as reach the target".
  - The draft leaves 2011-12 out because it "would test the scanner change rather than later people". But SPLIT-15 lists "a change of rules or of the data collection" among the periods a deployed model must handle. So the stated reason counts for the window, not against it.
  - The window choice is backed by model RMSE (issue 1's table). SPLIT-15 says the evidence for choosing windows is "statistics of the data, never a model's score".
  - Precedent: `anes_voting_2026` took 9 windows, 4 of them under half (down to 40.0%), to add elections (CC 2026-11-11 Lennart; exception 2026-11-19 Andrej). Here a fifth window, 2005-06 at 42.8%, would be the same kind of exception. 2003-04 would train on 28%, below the 30% minimum, so it isn't possible.
* **Options:**

  | | Option | Pro | Con |
  |---|---|---|---|
  | a | 3 windows, recorded as an exception with its fact. The AI's best guess at that fact: a window trained on the old scanner alone measures a calibration shift no deployed equation meets, because today's clinic DXA is the newer kind | Every window trains on both eras | Below the reachable count without a rule-backed reason |
  | b | 4 windows: add 2011-12 at 55.1% (draft option C) | Follows SPLIT-15 and the ANES pattern; tests across the collection change | One window is dominated by the scanner shift (linear 4.49 vs about 3.5 elsewhere) |
  | c | 5 windows: add 2011-12 and 2005-06 (42.8%) as a curator's exception, as on ANES | Closest to the target; a window inside the old era | Another exception to SPLIT-14 (the register already says an amendment is due for SPLIT-14: 5 datasets) |
  | d | Amend SPLIT-15 so a measured instrument break may cap the windows | Makes (a) a rule rather than a one-off | A change to a rule over one dataset |

* **Recommendation:** (b). It follows SPLIT-15 and stays within the floor. If the curator prefers (a), the fact belongs in a CC line and in the `splits_comment`.

Rules: SPLIT-14 (Must), SPLIT-15 (Should). split_tree.md "The windows check". `anes_voting_2026` `accepted_check_warnings.splits_train_under_half`.

**No drift, no third exception**

No curator has decided on this record yet, so there is no drift to check. Neither departure is a third exception of its kind. The register's "amendment due" flag on SPLIT-14 (exceptions on 5 datasets) matters only if option (c) of finding B is taken.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** This is a real, well-known task (estimating DXA percent body fat from simple body measurements), the target is not trivial to predict and the split is honest. Two things need fixing first: confirm how the 1999–2006 imputed DXA values were handled, and decide what to do about the shifts in who was scanned between survey cycles.

**What the task is.** Clinicians, epidemiologists and fitness or insurance screeners want an adiposity number when no DXA scanner is available. Published body-fat equations, such as the Relative Fat Mass index, were derived from exactly this NHANES DXA data. Every feature (sex, age, race, weight, height, BMI, limb lengths, arm and waist circumference) is measured in the same exam visit, before or without the scan, so none of them gives away the target.

**Concerns, most serious first**

1. **I can't tell how the multiply imputed 1999–2006 values were handled.** The CDC page says "missing and invalid DXA data from NHANES 1999-2006 were imputed using multiple-imputation methodology", with five versions of each value (variable `_MULT_`). About 22% of 2005–06 participants had at least one body region imputed. The imputation model used "measured weight and waist circumference" as "critical predictor variables", which are features here. If imputed rows were kept, part of the target is a model output built from the features, and scores would be inflated on the 1999–2006 rows.
   - Evidence that imputed rows were mostly removed: 2005 has 4,885 rows, against roughly 5,080 participants with fully valid data. Our 2005 target minimum is 11.7, while the published range of the total percent fat variable (DXDTOPF) for 2005–06 is reported as 8.8–58.
   - Evidence that this is unverified: the table has no imputation flag (`DXITOTST`) and no implicate column.
   - For 2017 the count matches exactly: 3,658 rows, which equals the 3,658 valid DXDTOPF values.
   - **Change:** document that only one implicate was kept and that rows with `DXITOTST` ≠ 0 were dropped. Otherwise rebuild with that filter.

2. **Who was scanned changes across the temporal split.**
   - **Age:** the maximum age is 85 for 1999–2003, 69 for 2005 and 59 from 2011 onward.
   - **Weight:** the scanner table limit rose from 300 lb to 450 lb. Maximum weight is 133–142 kg before 2011 and 176–188 kg after.
   - **Missing cycles:** 2007–2010 are absent, because no whole-body DXA was done then.
   - **Effect:** the three test windows (presumably 2013, 2015 and 2017) contain heavy people who barely appear in the earlier training years, and training contains older adults who never appear in test.
   - **Scanner:** the hardware and software changed (QDR-4500A with Discovery v12.4, then Discovery A with APEX 4.0). Both eras apply the same 5% lean-to-fat correction, and I found no correction published for comparing percent fat between the two eras.
   - **Judgement:** this is a fair real-world shift, not leakage, but it should be stated. **Change:** either restrict to ages 8–59 for comparability, or keep it and document it as covariate shift.

3. **The extremes of the target look clipped or filtered.** The target runs from 11.5 to 56.2 and every cycle has a minimum of about 11.5–12.7. The source reports values down to 8.8. This may just be a side effect of dropping imputed or invalid scans, but I could not confirm that. **Change:** document the filter.

4. **Minor issues.**
   - **BMI is redundant:** it equals weight / height² exactly (0 mismatches above 0.1). That is harmless.
   - **`survey_cycle` as a feature:** in a temporal split, tree models can only treat the unseen test cycle as the last training cycle. That is fine, but consider dropping it or marking it as the time index only.
   - **Duplicates:** 4 pairs of rows have identical features but different targets, mostly rows with missing waist. There are no exact duplicates. I'm not concerned.
   - **Missing values:** 0.3–0.9% per feature, left as NaN. Column types are sensible (sex and race are categorical). Race uses the 5-level coding, which is consistent across cycles.
   - **Weights:** no training-weight column is labelled. The NHANES survey design weights are not used, which is acceptable for a prediction benchmark.

**Signal and difficulty.** I trained on all cycles before each test window.

| Test window | LightGBM R² | LightGBM MAE (% fat) | Linear R² (sex, age, BMI, waist, height) | Linear MAE (% fat) |
|---|---|---|---|---|
| 2013 | 0.839 | 2.65 | 0.715 | 3.50 |
| 2015 | 0.853 | 2.63 | 0.735 | 3.54 |
| 2017 | 0.847 | 2.64 | 0.744 | 3.47 |

- There is strong signal, but the target is not solved, and the gap between models is wide enough to rank methods.
- With 39,691 rows and test windows of 3.7k–5k rows, there is plenty of data to score.
- Values are plausible: females average 37.1% body fat and males 26.5%, with no impossible anthropometrics.

**What I could not check**
- The CDC imputation technical PDF did not come through as readable text, so I don't have the full list of variables the imputation model used.
- Without participant IDs (`SEQN`) and the imputation flags in the table, I can't confirm which implicate was kept or whether imputed rows were dropped.
- I did not read the 2011–2016 codebooks for their exclusion rules.
- I can't tell whether the target's range reflects filtering by the preparer.

</details>

<details><summary>Task gamer</summary>

The task barely leaks: nothing I tried beat the honest LightGBM baseline (mean RMSE 3.387) by more than random noise. The best "exploit" gained 0.006.

**Noise level:** adding a column of random numbers moved the mean RMSE by +0.001 to +0.006 (3.3887–3.3937). LightGBM gives the same result for every seed here, so this spread is the yardstick for every gain below.

**Baseline**: RMSE 3.4154 / 3.3572 / 3.3893 on the 2017 / 2015 / 2013 test windows, mean 3.3873.

| # | Exploit | Script | Honest score | Exploited score | Gain (per split, range) | A deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Each numeric feature's percentile rank within its own survey cycle, test rows included | measured | 3.3873 | 3.3815 | −0.002 to +0.018 (mean +0.006) | Partly: a survey analyst could rank a new cycle against its own population | None needed; same size as noise |
| 2 | Each feature's distance from its own cycle mean, test rows included | measured | 3.3873 | 3.3874 | −0.022 to +0.020 (mean 0.000) | Same as #1 | None |
| 3 | Global ranks over all rows (a control: trees ignore monotone transforms) | measured | 3.3873 | 3.3828 | +0.001 to +0.006 | n/a | n/a |

Row 3 shows that 0.005 of movement comes from LightGBM's binning alone, so #1 is not a real gain.

**Flaws that hurt an honest model:** none found. I tried four honest choices:
- Training only on ages ≤59, the test windows' age range: 3.3832.
- Replacing `survey_cycle` with a flag for the newer scanner era (2011 on) vs. the older one (1999–2005): 3.3834.
- Training only on 2011 onward: 3.4454.
- Training on 2005 onward, ages ≤59: 3.4142.

The first two are within noise of the baseline; the last two are worse. So the older cycles, despite their different scanner and wider age range, help rather than hurt.

**Signal, not an exploit:** `survey_cycle` is worth 0.03 RMSE (3.417 without it). Mean body fat drifts upward over the cycles (31.1 in 2001, 32.3 in 2017), and the scanner software changed in 2011. A deployed model knows the cycle, so this is legitimate.

**Attacks that found nothing**
- **Formats.**
  - All values have one decimal, except BMI at two; the target has one decimal and about 10% whole numbers in every cycle.
  - Last-digit and missing-value features alone score 8.654, the same as predicting the mean (target SD is 8.84). Adding sex, cycle and age gives 6.624 against 6.617 without them.
  - BMI minus weight/height² has a correlation of 0.002 with the target; as a feature it scores 3.3887.
- **Missing values:** rows missing height, leg length or waist average 1–2 points more body fat, but that is ≤0.9% of rows and the model already handles NaN.
- **Order and ids:** row position as a feature scores 3.3913. Position vs. target correlation within each cycle is −0.04 to 0.04; consecutive rows' targets correlate at −0.003.
- **Copies across the split:** only 2 exact feature duplicates between train and test (in the 2017 split). Predicting each test row with its nearest training row's label scores 4.74–4.90, far worse than the model. There is no participant id, and nobody appears in two cycles.
- **Train vs. test classifier:** AUC 0.64–0.68, driven by age (test cycles stop at 59) and higher weights in 2011 onward. That is a coverage shift, not a leak.
- **Columns from after the prediction point:** every column is a tape-and-scale measurement taken at the exam. Nothing is derived from the DXA scan.
- **Weight, whole-table scaling, lookup formulas:** there is no training weight, and no column is standardised or min-max scaled.
- **Web:** this is not a competition dataset, so there are no leak threads or winning write-ups. Looking rows up in the public NHANES files would work, since the target is the published DXA value; I'm not ranking that.

**What I could not check**
- **Imputed targets in 1999–2005.** The CDC's 1999–2006 DXA files fill missing scans with multiply imputed values. Those were predicted from the same body measurements used as features here. The old cycles top out at a weight of 133–142 kg, against a 136 kg scanner limit, which suggests the imputed rows were dropped. The kit has no imputation flag, though, so I can't rule out some remaining. If any remain, they are mildly noisy training labels and would not leak into the 2013–2017 test windows, which have no imputation. The fact that decides it is the published imputation flag for each row.
- **Scanner calibration across eras:** whether the CDC adjusted the 1999–2005 scanner values to match the newer one.

Sources:
- [NHANES DXA overview](https://wwwn.cdc.gov/nchs/nhanes/dxa/dxa.aspx)
- [DXA technical documentation](https://wwwn.cdc.gov/nchs/data/nhanes/public/1999/documents/dxa_techdoc.pdf)
- [Body composition data, 1999–2004](https://pubmed.ncbi.nlm.nih.gov/20812448/)
- [PMC2737140](https://pmc.ncbi.nlm.nih.gov/articles/PMC2737140)

</details>

<details><summary>Advocate, opening brief</summary>

**Advocate's opening brief: `nhanes_dxa_body_fat`**

**Position:** ship the dataset. Two parts should change before it ships: add one parameter for a fourth window, and add a filter that drops 90 rows. Everything else stays as defined, with sharper notes. No agent found a leak, a wrong split regime, a wrong target or a wrong metric. Every real problem they found has a fix on the "fix the definition" or "keep with a note" rung of the remedy ladder.

**1. The task is real, the fit is direct, and nothing leaks (P3 USE-1 and USE-8; P4 LEAK-10, Must).**
- **Evidence:**
  - The domain practitioner agrees with `fit="direct"`. The inputs are what a tape, a scale and an intake form give. The label is the reference scan they replace.
  - The relative fat mass equation (Woolcott and Bergman 2018) was built on these same files.
  - On adults in the test cycles, an untuned LightGBM classifies obesity correctly for 86–87% of people. BMI ≥ 30 gets 64–66%.
  - The column auditor found no leak: no DXA column other than `DXDTOPF` is read, and every feature is taken at the exam.
  - The task gamer tried row-order, format, copy, ranking and train-vs-test attacks. None beat the honest baseline by more than noise: the best gained +0.006 RMSE, the same as a column of random numbers.
  - The blind reviewer, without our notes, says "include with changes".
- **Why it outranks the objections:** these are the P3 and P4 Musts. No finding in any report touches them. Every objection below is P4 Should, P5, P6 or P7.

**2. The split regime mirrors the application (P4 SPLIT-36 and SPLIT-11; SPLIT-15 Must for the newest window).**
- **Evidence:**
  - The split auditor gives "right with notes". The tree walk runs Survey → [SUR.meets] → [L-ORDER.windows], with no step forced.
  - It also ran the alternative and measured that the forward split is needed. A forward model does worse than one fitted inside the test cycle on the same number of rows: 3.70 against 3.66 (2017), 3.58 against 3.49 (2015), 3.64 against 3.53 (2013).
  - The source validated forward too: develop on 1999–2004, validate on 2005–06.
  - The newest cycle, 2017–18, is a test window, as SPLIT-15 requires.
  - No gap is applied. A one-cycle gap moves RMSE by only +0.03 to +0.09, so the newest labels are no shortcut (SPLIT-10).
- **Concession:** the fourth window. 2011–12 trains on 55.1%, above SPLIT-14's floor. SPLIT-15 (Should) lists "a change … of the data collection" as a reason to test a period, not to skip it. The definition's reason for leaving it out runs the other way. The draft also used a model's RMSE to justify the choice, which SPLIT-15 forbids.
  - **Fix:** `n_windows=4` (option C in the builder's issue 1), and update `splits_comment`. This is one parameter. The regime stays as it is.

**3. The target is the right one, and dropping CDC's imputed scans is correct (P5; CLEAN-2).**
- **Evidence:**
  - CDC says: "Imputed values should not be treated as measured variables." The domain practitioner and the precedent checker both agree with the filter. An imputed percent fat is IVEware's output, and its imputation model used weight and waist, which are features here.
- **Concession:** the claim auditor found 90 rows that still carry an imputed or varying percent fat. These are 80 people of 2003–04 whose imputation flag is wrong, and 10 of 2005–06 where the bone flag was ignored. They are 0.2% of rows, all on the training side.
  - **Fix:** keep a person only if `DXDTOPF` is the same in all five `_MULT_` records, and correct the comment "the measured values are the same in all five".
  - **Why this is enough:** no test row is affected and it is a single filter, so the problem calls for a definition fix, not more.

**4. The difference in the "measured" rule between eras gets a note; the data stays as it is (P5 / CLEAN-1 Should; remedy ladder).**
- **Evidence:**
  - 893 rows from 2011–18 keep CDC's published whole-body total even though one region of the scan was invalid. That is 8.9% of the 2017–18 test window.
  - In 1999–2006, CDC imputed such scans, and the definition drops them.
  - Dropping these rows everywhere barely moves the score: 3.37 against 3.38 (claim auditor), and 3.410 against 3.417 (column auditor).
  - The total is CDC's own published value, not ours.
  - Dropping them would thin the heavy tail of the test folds further, and that tail is already the selection problem (point 6).
- **Remedy:** both auditors independently recommend keeping the rows and rewriting the note. The `Selection Bias` line should say that the new era keeps partly invalid scans and the old era does not. Keeping with a note is the mildest remedy that settles it, so no definition change is needed.

**5. The metric is the one the field uses (P6 MET-5 and MET-8).**
- **Evidence:**
  - The relative fat mass paper selected its equation on several criteria together (verified quote), so MET-5 sends the task to the fallback, RMSE.
  - RMSE in percent-fat points is the standard error of estimate that body-fat equations are judged by. The domain practitioner "would pick the same metric".
  - A continuous estimate serves every obesity cutoff, and no single cutoff exists (MET-7 and MET-8).
  - Precedent: `body_density_prediction` also scores with fallback RMSE.
- **Open point:** the source's RMSE was survey-weighted and ours is not. This is a weighing call (MET-1). One sentence in the metric reason settles it: a clinician scores the person in front of them, not the US population. Precedent: `anes_voting_2026` is scored unweighted.

**6. The dataset is worth benchmarking and replaces a much weaker one (P6 TP).**
- **Evidence:**
  - 39,691 people, with test folds of 3,658 to 5,056 people.
  - LightGBM R² is 0.84–0.85 against 0.72–0.74 for a linear model; RMSE is about 3.4 against 8.4–8.8 for predicting the mean. The target is not trivial, and the gap between methods ranks them.
  - It replaces 252 men of 1985 for the same use case.
- **Selection:**
  - There are no test rows aged 60 and over.
  - The heaviest people are thinned. In 2017–18, 50% of examined adults with BMI ≥ 40 have a usable scan, against 75% of those with BMI < 30.
  - Both come from the source (CDC's eligibility rules and table limit), so there is nothing to repair. The domain practitioner judges the fit still direct under USE-8: the missing people with BMI ≥ 40 are the cases where the obesity call is least in doubt, and RMSE there (2.99–3.39) is no worse than overall.
  - **Remedy:** set the `Selection Bias` marker, and add "tested on ages 8–59" to `use_case`. These are notes, not changes to the data.

**7. The feature set: the drop holds on a use-case fact, and the ethnicity coding gets a note or one added level (P7 CLEAN-22 Must; CLEAN-19).**
- **Concession on the era-only measures:** "taken in some cycles only" is the reason the settled cross-dataset item of 2026-11-11 rejected. That item kept `onlinenewspopularity`'s `kw_min_min`. The LightGBM score comparison is also inadmissible as a reason (EV-4).
- **What still holds:** CLEAN-22 lets a column leave for what it is.
  - The skinfolds and the sagittal diameter need calipers, so they are outside the task's own instruments (a tape and a scale), as stated in `task_summary`.
  - The cases differ from the precedent. `onlinenewspopularity`'s deployed model meets that site's own changes of logging. A clinic using this equation never meets NHANES's protocol changes.
  - None of these columns could inform a test prediction in the shipped windows: thigh, calf and the skinfolds are in no test row, and hip is in no training row.
- **Fix:** record the use-case fact as an exception in a CC line, which is the precedent checker's option (a). If the curator wants the precedent followed strictly, option (c) is the mildest fallback: drop the caliper measures and keep thigh, calf and hip.
- **Ethnicity:** "Other race" grows from 3–5% of training rows to 16–23% of test rows, mostly Asians oversampled from 2011. Adding a non-Hispanic Asian level from `RIDRETH3` cuts the bias for Asian test people from +0.98 to +0.58 points.
  - This is a P7 quality point. Both auditors offer a mild fix: add the level, or keep `RIDRETH1` with a note. I support adding the level. It is cheap, safe, comes from the source and needs no data dropped.

**For the curator:** the panel's findings are separate fixes that do not conflict, and none is a Must that can't be fixed. Ship after these changes:
- four windows;
- the 90-row filter;
- the `RIDRETH3` level;
- notes on the era rule, the weighting, the release dates and the selection;
- a recorded exception for the dropped columns, or option (c).

The release-date note: the 2011–18 labels are a 2020 re-analysis, and no gap is applied because the scan is same-day.

</details>

<details><summary>Critic, opening brief</summary>

**Critic's opening brief: `nhanes_dxa_body_fat`**

**Verdict: ship after changes.** The task is real, and nobody on the panel found a leak: the column auditor, the task gamer and the probes all agree on that. I don't argue against the task itself. I argue against four parts of how it is defined: the target filter, the window count, the dropped measures and the ethnicity coding. I also ask for corrections to notes that are wrong. No point below justifies excluding the dataset.

**1. 90 training labels are imputed but shipped as "measured" (validity, P5; USE-5 Must: check how the source built its label).**
- **Problem:** the definition keeps 1999–2006 rows where the imputation flag is 0, and assumes that "the measured values are the same in all five" imputation records. That assumption fails for 90 people.
- **Evidence:** I rebuilt this from the raw DXX files today. 80 people in 2003–04 have the flag at 0, yet their `DXDTOPF` differs across the five `_MULT_` records by up to 4.6 points. 10 people in 2005–06 differ by up to 0.1 point, because the definition reads only the soft-tissue flag (`DXITOTST`) and ignores the bone flag. The other cycles have none. This confirms claim-auditor #3. For these 90 people, the label we ship is one model draw (from the IVEware imputation model), not a scan.
- **Effect:** 0.2% of rows, all on the training side. Small, but the curation notes say "measured scans only", and that is false.
- **Remedy (fix the definition):** keep a person only if `DXDTOPF` is identical across all five records, and correct the comment in `_clean`.

**2. "Measured" means one thing in training and another in testing (validity, P5; CLEAN-1 Should: rules that hold for the train and the test period alike).**
- **The asymmetry:**
  - In 1999–2006, CDC imputed every scan that had an invalid region. The definition drops those scans.
  - In 2011–2018, CDC still publishes a whole-body percent fat when a region is invalid. The definition keeps those scans: 893 rows, about 9% of the newest test window (2017–18).
- **Evidence:** in 2017–18, 149 of the kept rows have the trunk coded 3, "excessive x-ray noise due to morbid obesity". I confirmed this on DXX_J. For these rows, `DXDTOPF` equals total fat over total mass within 0.05, so the noisy trunk reading is part of the label. The same kind of person is dropped from the old era. So the claim in the Selection Bias note that both eras "miss the heaviest people the same way" is false (claim auditor #4, column auditor problem 1).
- **Effect:** the newest window is mandatory (SPLIT-15 Must), and it scores on labels that CDC says include a region it "could not analyze accurately". Model rankings barely move: RMSE on valid rows only is 3.37 against 3.38.
- **Remedy:**
  - I ask for one filter in both eras: drop 2011–2018 scans with any invalid tissue region.
  - If the curator wants to keep the heavy tail instead, the fallback is to keep the rows and rewrite the "measured scans only" and Selection Bias notes so they state the asymmetry. That is a weighing call, so the curator should get both options.

**3. Three test windows where the rules allow four (validity, P4; SPLIT-15 Should).**
- **Problem:** a 2011–12 window would train on 55.1% of the rows and test 4,521 people, so it clears SPLIT-14's half floor. The `splits_comment` leaves it out because it would "test the scanner change". But SPLIT-15 lists "a change … of the data collection" as a period a deployed model must handle, so that reason counts for the window, not against it.
- **Second flaw:** issue 1 backs the window count with model RMSE. SPLIT-15 says the evidence for choosing windows is "statistics of the data, never a model's score".
- **Agreement:** the split auditor (problem 1) and the precedent checker (finding B) both reach this conclusion. `anes_voting_2026` took every window it could, down to 40% training share.
- **Remedy (fix the definition):** set `n_windows=4`. If the curator keeps three, they record an exception with a fact (a CC line) and say so in the `splits_comment`.

**4. The measures taken in some cycles only are dropped for a reason that was already rejected (quality, P7; CLEAN-22 Must).**
- **Problem:** the definition drops thigh, calf, hip, two skinfolds and the sagittal diameter.
- **Why the reasons fail:**
  - "Taken in some cycles only" is the reason the settled cross-dataset item turned down (REVIEW.md, 2026-11-11, Lennart, option A). That item kept such columns on seven datasets; `onlinenewspopularity`'s `kw_min_min` is missing in every test window and was kept (precedent checker, finding A).
  - The builder's LightGBM comparison is a model score, which EV-4 and CLEAN-22 rule out as a reason to drop a column.
  - "Calipers, not a tape" covers only three of the six columns. It does not even hold for the use case as written: the domain practitioner says gyms use calipers.
- **Remedy (fix the definition):**
  - Keep the columns, missing where they were not taken, and accept `splits_feature_missing_in_test` with a CC date.
  - Or the curator drops them as a recorded exception with a fact that sets this case apart. The precedent checker's option (a) suggests one.

**5. `race_ethnicity` puts the 2011+ Asian oversample in "Other" (quality, P7; CLEAN-1 Should).**
- **Evidence:** "Other race" is 3–5% of the training cycles but 16–23% of the test cycles, and 67–77% of those people are non-Hispanic Asian by `RIDRETH3`.
- **Effect:** the model underestimates their percent fat by about 0.4–0.8 points more than for everyone else (domain practitioner, gap 2). Adding the Asian category cuts the 2017 bias from +0.98 to +0.58 (column auditor, problem 2). This is a known clinical issue: Asians carry more fat at a given BMI.
- **Remedy (cheap):** add a "Non-Hispanic Asian" level from `RIDRETH3` for 2011 on, with a note that Asians in earlier cycles stay in "Other". The fallback is a note on why `RIDRETH1` was kept. This is a quality point and no reason to exclude.

**6. The sample is more selected than the notes say (validity note; `Selection Bias`, selection.md; USE-8).**
- **Evidence:**
  - Completed scans with no percent fat grow from 4.8% of 2011 to 15.6% of 2017, and they are heavier (median BMI 29.9 against 25.7; split auditor, problem 2).
  - Among adults aged 20–59 with BMI ≥ 40, only 50% of the 2017 cycle have a usable scan (domain practitioner).
  - No test row is aged 60 or over.
- **Remedy (notes):** set the `Selection Bias` marker, add these shares to the note, and say in `use_case` that the tested population is aged 8–59.

**7. Notes that misstate the evidence (EV-2; MET-1 Must, met with a note).**
- **Metric:** the source's RMSE (Woolcott and Bergman) is survey-weighted and pooled over the imputations; ours is unweighted on measured scans only. Add one sentence to the metric reason saying so, and why: a clinician scores the person in front of them.
- **No-gap reason:** every 2011–18 DXX file shows "First Published: March 2020" (an Apex re-analysis). The `splits_comment` should rest "no gap" on the same-day scan, not on "known when the next cycle starts".
- **Record's screening block:**
  - "71%" should read 76%.
  - The 5% lean-to-fat shift applies in both eras, not 1999–2006 only.

</details>

<details><summary>Advocate, rebuttal</summary>

**Advocate's rebuttal: `nhanes_dxa_body_fat`**

The critic and I agree on the verdict, "ship after changes". We also agree on five of their seven points. We disagree on the remedy for point 2 and on how the reasons for point 4 should be read. Neither disagreement is about a Must that can't be fixed.

**1. 90 imputed training labels: concede.**
- The critic rebuilt this from the raw DXX files, and so did the claim auditor (#3). That is two independent confirmations.
- **What follows:** the filter from my point 3. Keep a person only if `DXDTOPF` is the same in all five `_MULT_` records, and correct the comment in `_clean`. No test row is affected.

**2. "Measured" differs between eras: I concede the facts and dispute the remedy.**
- **Conceded:**
  - 893 kept rows have an invalid region, and 149 of the 2017–18 rows have trunk code 3.
  - The Selection Bias note's claim that both eras miss the heaviest people "the same way" is false.
  - One correction to my own brief: the claim auditor counts these rows as 10% of the 2017–18 test fold. I wrote 8.9%.
- **Disputed:** the critic asks for the drop filter first. Both auditors who measured this recommend keeping the rows:
  - claim auditor: "(a) The mildest remedy, and my recommendation: keep the rows and rewrite the note";
  - column auditor: "Mildest remedy: keep the rows and state the difference".
- **Why keeping wins:**
  - **The rule:** CLEAN-1 is a Should. The remedy ladder sends a Should to the mildest fix that settles it, and a note settles it.
  - **Scores barely move:** RMSE is 3.37 against 3.38, and 3.410 against 3.417 when training on valid scans only. So there is no measured harm to correct.
  - **The label is CDC's own:** `DXDTOPF` is CDC's published whole-body value, not something we build. The critic's own check shows it equals total fat over total mass within 0.05.
  - **Dropping costs the heavy tail:** these rows have median BMI 33.6. Dropping them would thin the heavy tail of the test folds further, which is exactly the selection problem the critic raises in point 6. The two remedies pull in opposite directions, and keeping avoids that.
- **Agreed:** the curator should see both options. I recommend option (a), keep the rows with a rewritten note.

**3. Four windows: concede.**
- This was already my point 2, and the remedy is the same: `n_windows=4`, plus an updated `splits_comment` that no longer rests on a model's RMSE.

**4. The measures taken in some cycles only: I dispute one argument and accept the fallback.**
- **Conceded:**
  - "Taken in some cycles only" is a rejected reason (REVIEW.md, 2026-11-11).
  - The LightGBM comparison is inadmissible (EV-4).
  - The caliper fact covers only 3 of the 6 columns.
- **Disputed:** "the domain practitioner says gyms use calipers" misreads the report. The practitioner's full sentence is: "Gyms in practice use bioimpedance or calipers, not this table, so the clinician and the epidemiologist are the right actors and the gym is a weak third." That puts the caliper user outside this task's actors. It supports the fact that the skinfolds and the sagittal diameter need instruments the task's actors don't use. It does not refute it.
- **What follows:**
  - For the caliper measures, CLEAN-22 (Must) lets a column leave for what it is, so dropping them is backed by a fact.
  - Thigh, calf and hip are tape measures. They rest only on precedent option (a)'s fact (a clinic never meets NHANES's protocol changes), and that fact is weaker.
  - The practitioner also says they "would normally also have hip circumference". So I now prefer option (c):
    - drop the caliper measures, with a CC line stating the fact;
    - keep thigh, calf and hip, missing where they were not taken;
    - accept `splits_feature_missing_in_test` with a CC date.
  - This meets the critic's first remedy for half of the columns and gives a fact-based exception for the other half.

**5. Asian level in `race_ethnicity`: concede.**
- Add the "Non-Hispanic Asian" level from `RIDRETH3` for 2011 on, with a note that Asians in earlier cycles stay in "Other". The measured effect: bias for Asian test people falls from +0.98 to +0.58.

**6. Selection: concede.**
- Set the `Selection Bias` marker, add the shares to the note, and add "tested on ages 8–59" to `use_case`. These are notes, not data changes.
- One addition the critic leaves out: the domain practitioner still judges the fit direct (USE-8). RMSE on the BMI ≥ 40 rows is 2.99–3.39, no worse than overall.

**7. Notes that misstate the evidence: concede, all four items.**
- One sentence in the metric reason on unweighted against survey-weighted scoring.
- "No gap" rests on the same-day scan, given that the 2011–18 files were first published in March 2020.
- In the record: 71% becomes 76%, and the 5% lean-to-fat shift applies to both eras.

**For the curator:**
- **Changes to the definition:**
  - `n_windows=4`;
  - the five-record identity filter;
  - the `RIDRETH3` level;
  - option (c) for the dropped columns.
- **Notes:** era asymmetry, Selection Bias, the age range, the metric weighting, the no-gap reason and the record's corrections.
- **One weighing call left:** whether to drop the 893 partly invalid 2011–18 scans. I recommend keeping them with a note. The critic asks to drop them but accepts keeping as the fallback.

</details>

<details><summary>Critic, rebuttal</summary>

**Critic's rebuttal: `nhanes_dxa_body_fat`**

The two briefs now agree on most things. I concede five of the advocate's seven points and dispute parts of two. One new fact came up: one of the advocate's claims is wrong when checked against the raw files.

**1. The task is real, direct, and nothing leaks. Conceded.** My brief never disputed this. No finding touches the P3/P4 Musts.

**2. The split regime is right, and four windows. Conceded.** We agree on `n_windows=4` and on rewriting the `splits_comment`. One small point remains. The advocate rests "no gap" on a model's RMSE moving by +0.03 to +0.09. Like the window count, the gap needs a data fact (SPLIT-15: statistics of the data, never a model's score). The fact is the same-day scan. The 2020 Apex release date goes in the comment as a note.

**3. The 90-row filter. Conceded.** We ask for the same fix: keep a person only if `DXDTOPF` is identical across all five `_MULT_` records, and correct the comment in `_clean`.

**4. The era asymmetry: keep the rows with a note. Partly disputed; this is a call for the curator.**
- **I concede:**
  - Both auditors prefer the note.
  - The score barely moves (3.37 against 3.38).
  - CDC itself publishes the whole-body total.
  - Dropping these rows thins a heavy tail that is already under-covered.
- **I dispute that a note fully settles CLEAN-1 (Should: the same rules for train and test).**
  - The two eras cannot be made symmetric by keeping rows. In 1999–2006 no measured total exists for a scan with an invalid region; CDC only published imputations. So dropping is the only symmetric rule.
  - The 149 test rows of 2017–18 with the trunk coded 3 ("excessive x-ray noise due to morbid obesity") score models against a label that CDC says contains a region it could not analyze accurately.
- **What I ask:** put both options in front of the curator. (a) Drop invalid-region scans in 2011–18. (b) Keep them and rewrite "measured scans only" and the `Selection Bias` note to state the asymmetry and the 893 rows. I accept (b) if the curator picks it. I lean to (a) for the trunk-noise rows.

**5. Metric RMSE, with an unweighted note. Conceded.** It is the same sentence I asked for.

**6. Value and selection. Conceded, with one addition to the note.** We agree on the `Selection Bias` marker and on "tested on ages 8–59". The note should also give the split auditor's share: completed scans with no percent fat grow from 4.8% of the 2011 cycle to 15.6% of the 2017 cycle, and they are heavier (median BMI 29.9 against 25.7). The advocate's brief leaves this out, and it is the part of the selection that grows over the test windows.

**7. Feature set. Ethnicity conceded; the dropped columns disputed on a fact.**
- **Ethnicity:** conceded. We both ask for a non-Hispanic Asian level from `RIDRETH3`.
- **The advocate's claim is false.** The advocate says "None of these columns could inform a test prediction in the shipped windows." From the raw BMX files:
  - The sagittal diameter (`BMDAVSAD`) has values in 2011–12 (6,795), 2013–14 (7,218) and 2015–16 (6,983).
  - So it is in the training side and the test rows of the 2013 and 2015 windows, and of 2011 once four windows ship.
  - The claim holds only for thigh, calf and the skinfolds (1999–2006 only) and for hip (2017–18 only).
  - The column that could really inform test predictions is the one being dropped, so the "no harm" argument falls away.
- **"Needs calipers" is not one of the reasons CLEAN-22 (Must) lists.** Those are a leak, an identifier, a copy, or the measurement that defines the label.
  - A caliper reason is an input-availability fact about the use case (USE), and it holds only if the curator confirms the use case is tape-and-scale.
  - The domain practitioner says the clinician is the main actor. A clinic can own an abdominal caliper.
- **Option (a) does not cover thigh, calf and hip.** For these three tape measures, its fact ("a clinic never meets NHANES's protocol changes") is new reasoning with no rule or precedent behind it. The settled cross-dataset item of 2026-11-11 points the other way.
- **What I ask, in order:**
  1. Option (b): keep all six columns and accept `splits_feature_missing_in_test` with the CC date. This follows the precedent.
  2. Or option (c): keep thigh, calf and hip. Drop the skinfolds and the sagittal diameter only if the curator confirms tape-and-scale as the use case in a CC line, and the note says the sagittal diameter was available in three test cycles.
- I oppose (a) as written, because it rests on a false "no test row" premise for the sagittal diameter.

**What still needs the curator:**
- the era rule (drop, or keep with a note);
- the dropped columns: (b) or (c), not (a).

Everything else is agreed: four windows, the 90-row filter, the `RIDRETH3` level, and the notes on weighting, release dates and selection, plus my addition on the growing share of scans with no percent fat.

The cycle counts for each column come from the raw `BMX*.xpt` files of the release.

</details>
