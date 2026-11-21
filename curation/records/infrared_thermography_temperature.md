---
unique_name: infrared_thermography_temperature
name: Infrared Thermography Temperature
checked_by:
- Andrej
data_foundry_status:
- 'DF: Yes'
suggestion: Disagreement
priority: 4
decision_markers:
- Selection Bias
tags:
- New IID
- 'Samples: Over Time'
- 'Time: Dated'
- Dated Event Log
collections:
- New (BeyondArena)
original_source: Website
year: '2023'
collection_period: Nov 2016 - May 2018
domain: medical & healthcare
required_split:
- Random (IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://doi.org/10.13026/9ay4-2c37
- https://physionet.org/content/face-oral-temp-data/1.0.0/
v2_path: datasets/_dev/tabarena-v0pt2/infrared_thermography_temperature/dataset.py
source_row: 665
type_adapter_id: curation-record-v1
---

## Comments

Two targets. Need to carefully check which features make sense to include in the predictive task. Some might be unreasonable. Some features were extracted from infrared images, but those are not given

Discussion: I think this is grouped, subject ID is not unique but counts up with -1,-2,...

**Assessment (AI, 2026-10-07):** Added as a regression of `aveOralM` (oral temperature, monitor mode, the reference of both papers); `aveOralF`, the same readings in fast mode, is dropped as a second measurement of the target. Data: PhysioNet's FLIR_groups1and2.csv, 1,018 subjects (CC0). SubjectID is yymmdd-n and unique per row, so each subject is one row; holding out whole measurement days changes R² by less than 0.004, so the split stays IID, with temporal and day-grouped splits as alternatives. The 17 subjects without a complete round-1 image keep their later image. Random forest R² 0.707 (RMSE 0.274 against 0.509 for the mean), and an additive model beats the source's one-feature calibration on 28 of 30 splits. Is the modality marker an exception here?

**Assessment (AI, 2026-10-20):** priority 4 for the review of the added dataset: gap -, use case +, source +, shape +, no known risk. Well-documented FDA fever-screening regression with a direct use case; the open question is mainly the image-derived modality marker.

**Assessment (AI, 2026-10-20):** review panel (full): ship after changes; the 17 subjects without a complete round-1 image are dropped (their next image follows the oral thermometer; USE-7), 1,018 to 1,001 rows, which supersedes "the 17 keep their later image" above; the use case is rewritten to the clinic triage station of the source (fit direct), the split reason rests on the new person (IID; temporal open as a variant) and the "exception" note now gives the SEL-15 reason (scope open for the curator). The 2026-10-07 measurement (SubjectID unique) supersedes "subject ID is not unique"; the reference is Sensors 22(1):215, 2022. Priority 4: gap - (no thin domain, problem type or regime), use case + (the source's calibration, fit direct), source + (PhysioNet and two papers), shape + (1,001 people, 35 features, categorical), risk 0 (no leak left, recommended to ship).

CC (2026-10-21, Lennart): "yes we should have one clear way to treat 0/1 flags": every 0/1 flag (a feature holding only 0 and 1, plus missing values; booleans too) is categorical (CLEAN-14, amended). Typed categorical here: Cosmetics.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source rmse — root-mean-square difference A_rms (with clinical bias and its SD) (Wang et al. 2022, Sensors 22(1):215, Sec. 2.5-2.6 (PMC8749858)).

CC (2026-10-21, Lennart): split: "IID is okay for now, but document the discussion. I think here we want to approximate and learn a function that is independent of time (like the measurements should be the same between two different days given other inputs are the same) -> no real signal across time". IID kept; the measured year-to-year shift (a first-year calibration over-predicts the second year by 0.06-0.09 °C; past-only training +0.5% to +6.7% RMSE in 6 expanding windows) is recorded in the definition, temporal a candidate variant (SPLIT-31).

CC (2026-10-21, Lennart): scope: "Yes, go with (a)". The facial temperatures read through the thermal camera are measurements (SEL-15), not image descriptors (SEL-13); SEL-15 is amended: a physical quantity measured through an imaging device at defined sites (a temperature, a volume, an angle), used by the field as the instrument's reading, is a measurement, with satimage and wilt as the counter-cases. The marker `Wrong Domain / Source Modality` is removed with this decision.

CC (2026-10-27, Lennart): marker Selection Bias, from the AI review of PR #16: the people were recruited at a university health center, 889 of the 1,020 in the raw file aged 18 to 25 and 3 over 60, against the clinic patients of the triage use case. The definition's fit_reason does not name the age range yet.

CC (2026-10-27, Lennart): fit stays direct: the setting, a university clinic, sees the same mostly young people (USE-8, amended on the review of PR #16); the Selection Bias marker stays.

**Assessment (AI, 2026-10-30):** Dtype review (branch ordinal-and-censored-levels; the column decisions with their codebook evidence are on the review board): left unordered: `Age` (a level outside the scale is a state of its own).

CC (2026-10-31, Lennart): marks on the review board of PR #37 (ordinal scales in the codebook's order, also when shipped as numbers; a state outside a scale missing when the column has no other missing value, else the lowest level; cycles ordered; codes shipped as numbers as categories): 1 columns with a state outside the scale ordered, the state placed by the rule; the age bands ordered, the overlapping 21-30 by its midpoint.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `therlid_infrared_vs_contact_temperature` (TBD -> Yes, priority 2). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-17, Andrej): collection type `Dated Event Log` instead of `Experimental Results` (Review issue 3, a): the subjects were screened one by one at a health centre and each row records its visit date.

CC (2026-11-20, Andrej): the random folds stay `StationaryRelation`, now on the stationary-relation test over the two two-month windows that train on half the subjects (flat for Kumo-Tabular); the window at the set-up change (Nov-Dec 2017, 48%) reads not flat and is named (Review issue 4, C).

## Review

**Outcome:** added. A question on `CrossSectional` (2026-11-13) was withdrawn when the prototype was dropped.

**Main points:** Settled: issue 1 withdrawn (2026-11-13); collection type `Dated Event Log` (issue 3, a, 2026-11-17);
the random folds stay `StationaryRelation`, on the stationary-relation test over the two two-month windows (issue 4,
C, 2026-11-20). Open: issue 2 (three two-month windows instead of random folds) has no Resolved line.

**Issues for Andrej:**

1. **`CrossSectional` instead of `StationaryRelation`?**

   * **Problem:**
     - The oral temperature is a present state measured with the image, read for new people at their own visit[^cs-1].
     - `StationaryRelation` now names a forward use case measured flat; this one forecasts nothing.
     - The measurement stays: folds grouped by day score as random ones do, and past-only training costs +0.5% to +6.7% RMSE.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Stay `StationaryRelation` (implemented) | the tag and its line stay | no change | the tag claims a forward use case |
     | B | `CrossSectional` | the tag changes; the line keeps the measured drift | names the use case; the measurement stays in the line | none found |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag, start the line with `CrossSectional`, keep the measurement; add a CC line.

   [^cs-1]: **SPLIT-32** (Should, 2026-11-13): a target measured together with the features, which the use case reads for new units at their own present, is `CrossSectional`; where dates survive, its line gives the measured drift.

   **Andrej (2026-11-13, change):** Option B: CrossSectional.

   **Resolved (2026-11-13, Andrej):** withdrawn: `CrossSectional` was dropped the same day (it named no split the existing prototypes do not give: a present state used later is forced or a measured `StationaryRelation`, used within the covered time `Retrospective`). The tag stays.

2. **Split: three two-month windows on the visit date (Nov-Dec 2017, Jan-Feb 2018, Mar-Apr 2018) instead of 10 x 3-fold random cross-validation over subjects?**

   * **Problem:**
     - With every fact used the tree gives Temporal · sample order: every subject carries a visit date (1,020 subjects on 154 days, 17 Nov 2016 to 14 May 2018), enough for three windows, and the rule[^split-32] as amended on 2026-11-17 makes such a split temporal, so `StationaryRelation` no longer applies.
     - The definition's own measurements show the relation is not flat: a first-year calibration over-predicts the second year by 0.06-0.09 °C, and past-only training costs +0.5% to +6.7% RMSE.
     - The random split was Lennart's choice of 2026-10-21 (a calibration should not depend on the day), with a temporal variant kept as a candidate.
   * **Background:** Screening subjects arrive one by one and every subject carries a visit date over 18 months, enough for three or more windows of 50+ people. Each window is tested on earlier subjects, which also tests the documented change of set-up between study years; no gap since the label is taken in the same visit. Confidence of the blind walk: high.
   * **Walk:** the questions as answered without the current split[^tree]:
     - Is there an order to how samples arrive in the use case? (use case): yes. Evidence: Use case: people arrive at a clinic's triage station and are imaged one at a time; a maker calibrates a device and then uses it on later people. The tree names 'visitors at a screening point' as yes.
     - Is the order available in the data? (data): yes, a recorded date. Evidence: PhysioNet FLIR_groups1and2.csv (v1.0.0, downloaded 2026-11-17): Date column and SubjectID = YYMMDD-n; all 1,020 subjects dated, 154 distinct days from 2016-11-17 to 2018-05-14.
     - Does the order give the windows the rule[^split-14] and the rule[^split-15] ask for? (data): yes. Evidence: Subjects per month (raw, 1,020): 2016-11 17, 12 53; 2017-02 96, 03 112, 04 117, 10 96, 11 72, 12 49; 2018-01 54, 02 174, 03 101, 04 76, 05 3. Quantiles of the date: 50% at 2017-11-06, 60% at 2018-01-24, 80% at 2018-02-26. Three or more windows with ≥50 test rows each fit: e.g. Mar-May 2018 (~80% train, 180 rows), Feb 2018 (~63%, 174), Nov 2017-Jan 2018 (~44-49%, ~175; under 50% needs curator…
     - Gap[^split-10] (data): no gap. Evidence: The oral readings are taken minutes after the image in the same visit; the date's smallest recorded step is one day, so the label delay (minutes) is within the step.
   * **What the blind dossier lacked, and what it changes:** none to the walk. The definition ships IID (repeated 3-fold over subjects) tagged StationaryRelation, by Lennart's 2026-10-21 decision that a calibration should not depend on the day. In the tree, StationaryRelation is reached only at the ForcedFromTemporal step, when the order gives no usable windows; here the dated order gives them, and the definition's own measurements show the relation is not flat (a first-year calibration over-predicts the second year by 0.06-0.09 °C; past-only training costs +0.5% to +6.7% RMSE; the first second-year window is 5-29% worse). So the leaf stays Temporal ·…
   * **Missing from the blind dossier:** The split comparisons (day-grouped folds = random, R^2 0.699 vs 0.700; 6 expanding windows over the newest half of the days) and the IID decision with its reason.
   * **Source split:** yes, Wang et al. 2022, Sensors 22(1):215 (Sec. 2.5): one random split of subjects: 60% calibration, 40% test ("calibrated on a random 60% of the subjects and tested on the other 40%; the authors note a random split of one pool may bias the estimate upwards (Sec. 4.5)") https://doi.org/10.3390/s22010215. Credible: no, A random draw from one pool with no stated reason tied to deploying a camera on later people; the authors themselves flag the upward bias.. Against the tree's leaf: no, Wang et al. 2022 use one random 60/40 split of subjects (and flag its upward bias); the blind leaf tests later visits on earlier ones by date.
   * **Key to split on:** visit date (Date / SubjectID date part, day resolution); the date is no input (the order is not a column yet: the build computes it).
   * **What changes:** dataset.py: `temporal = Temporal(on=<visit day>, splits=TemporalSplits(window=2, unit="months", cutoffs=("2018-03-01", "2018-01-01", "2017-11-01")))`, `data_tags` without `StationaryRelation`, a new Time basis line and splits_comment; the record's required split and a CC line; the tree's departure table loses this dataset.
   * **Blindness:** what the walker saw of the shipped split before deciding: saw: split_tree.md lists infrared_thermography_temperature as an example under 'Temporal · sample order'; ignored as evidence.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 10 x 3-fold random cross-validation over subjects: train 667-668, test 333-334 of 1,001 subjects, `StationaryRelation` (implemented) | no change | 30 test splits of about 334 people give a steady RMSE; folds grouped by day score as random ones do (R^2 0.699 vs 0.700). | 94-99% of a fold's test subjects share their day with a training subject, and the set-up change between study years (location, distance 0.80 to 0.60 m) is in every training fold, so a camera used on later people is not tested. |
     | B | Three expanding two-month windows on the visit date: test Nov-Dec 2017 (121 subjects), Jan-Feb 2018 (228), Mar-Apr 2018 (177); train on all earlier subjects, 491/612/840 (48.1/60.0/82.4% of the raw 1,020); no gap; the 3 subjects of May 2018 in no split | Declares `Temporal` on the visit day, which the build takes from the date part of `SubjectID` (no input), with `TemporalSplits(window=2, unit="months", cutoffs=("2018-03-01", "2018-01-01", "2017-11-01"))`; `StationaryRelation` and its line give way to a time basis of the recorded date; the split measurements move to the notes; the record's split tag changes. | Tests a calibration on people imaged later, including the first second-year window that the notes measured 5-29% worse; the oral reading is taken in the same visit, so no gap is needed. | Three test sets of 121-228 people, all from the second study year; the oldest trains on under half (48.1%), which the curator signs off under the rule[^split-14]. |

   * **Recommendation:** B, because the dated visits give three windows and the rule[^split-32] as amended on 2026-11-17 makes such a split temporal however flat the relation, and here it is not flat.. **Decision:** A or B?

   **Notes for the AI:** blind walk of 2026-11-17 (split tree at cd3877cb). Applying a change: the definition's split declaration, its time basis tag and line, the record's CC line; if A is kept, the tree's departure table with the reason.

   [^split-10]: **SPLIT-10** (Should): When a label is known only some time after its row (a delivery time, a permit's processing time, an outcome after a follow-up), a model refit at a window's start knows only the rows whose label had arrived.

   [^split-32]: **SPLIT-32** (Should): How the data was collected for the use case, when each sample, each feature and the target come into existence, is information for the split.

   [^split-14]: **SPLIT-14** (Must): A temporal task has at least 3 windows.

   [^split-15]: **SPLIT-15** (Must): The newest window is always a test window: it is the deployment period.

   [^tree]: **SPLIT-36** (Should): walk the decision tree from the record's collection type, answering each question as if no split had been decided; a split the source prescribes is evidence, not an answer.

   **Answer (AI, 2026-11-17):** the walk again under each type issue 3 offers; the split this issue proposes is the same
   under all three.

   * Each row records its visit date (PhysioNet file: 1,020 subjects on 154 days, November 2016 to May 2018), and the
     oral reading is taken in the same visit, so the label is known with the row.

     | Type | Leaf the tree gives | Split |
     |---|---|---|
     | `Experimental Results` (now) | Temporal · sample order | windows on the visit date, no gap |
     | `Dated Event Log` | Temporal · arrival date | windows on the visit date, no gap |
     | `Clinical Study` | its order question sends a set with recorded dates to the dated event log | windows on the visit date, no gap |

   * Issue 3 changes only the leaf's name here; the choice in this issue (windows on the visit date, or the random
     split as shipped) stands on its own.

   **Answer (AI, 2026-11-17):** walked again as a `Dated Event Log` (issue 3): the model is used at the same screening
   point, forward, for subjects who arrive one by one, and each subject's oral reading is taken in the same visit, so
   the leaf is Temporal · arrival date, no gap. The options of this issue stand: windows on the visit date, or the
   random folds as shipped.

3. **Collection type: `Clinical Study` instead of `Experimental Results`?**

   * **Problem:**
     - The record's collection type is `Experimental Results`, the root the walk started from.
     - The walk reads the data as `Clinical Study`: The subjects were recruited one by one at a health center over 18 months, closer to a clinical study at one site; walked under Experimental Results as recorded, where the arrival-order branch fits..
     - The walk followed the recorded type and reached Temporal · sample order.
   * **The doubt:** The subjects were recruited one by one at a health center over 18 months, closer to a clinical study at one site; walked under Experimental Results as recorded, where the arrival-order branch fits.
   * **What changes:** the record's collection-type tag only. The split follows from it, so the tree must be re-walked under the new type; where that gives the same leaf, nothing else changes.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `Experimental Results` (implemented) | no change to the record | the type as the taxonomy assigned it | the doubt stays on the record |
     | B | Tag `Clinical Study` | changes the record's type tag and re-walks the tree from it | The subjects were recruited one by one at a health center over 18 months, closer to a clinical study at one site; walked under Experimental Results… | the type rules must agree; the leaf may change |

   * **Recommendation:** discuss: the collection-type rules decide this, the walk only raises it. **Decision:** A or B?

   **Notes for the AI:** blind walk of 2026-11-17 (split tree at cd3877cb). On B: change the record's type tag to `Clinical Study`, re-walk the tree from it and check whether the leaf changes; update the type rules' examples.

   **Andrej (2026-11-17, change):** Option B: Another type, as the note says. Then rewalk and adapt issue 2 if needed.

   **Answer (AI, 2026-11-17):** Which type: the type rules turn a clinical set with dates into a dated event log, and name
   this dataset as experimental results?

   * **Problem:**
     - The type rules let dates outrank only the clinical study: a clinical set whose rows record a date is a dated
       event log[^ir1].
     - This dataset's rows record the visit date, so read as patients it is a `Dated Event Log`, not a `Clinical Study`.
     - The same rule names infrared_thermography_temperature as experimental results that keep their dated rows.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | `Dated Event Log` | the type tag becomes `Dated Event Log`; the rule's case moves this dataset from the experimental results to the event logs | the rule for patients with dates; the walk's reading (subjects recruited one by one at a health centre) | changes a case the rule names |
     | b | `Clinical Study`, as the note says | the type tag becomes `Clinical Study`, with a written exception to the rule on dated clinical sets | the walk's literal reading | departs from the rule with no fact that sets this case apart |
     | c | Keep `Experimental Results` (implemented) | no change | the rule's own case | the subjects stay read as designed runs |

   * **Recommendation:** a: the reading you chose, put in the type the rules give it. **Decision:** a, b or c?

   [^ir1]: **SPLIT-34** (Should), rule 3: dates outrank only the clinical study: a clinical set whose rows record a
     date is a dated event log; experimental results, surveys and catalogues keep their dated rows.

   **Andrej (2026-11-17, change):** Reply (a): Dated Event Log

   **Resolved (2026-11-17, Andrej):** a: the collection type is `Dated Event Log`. The subjects were screened one by one at
   a health centre and every row records its visit date, so read as patients the type rules make it a dated event
   log. The split stays open in issue 2.

4. **Three windows on the visit date, or random folds on the new test?**

   * **Problem:**
     - Every subject carries a visit date, and three two-month windows train on 48%, 60% and 82% of the 1,001 subjects; since 2026-11-17 a split whose windows can be built is temporal, however flat the relation[^s32w].
     - Under your reading of the window count (30 for 1,001 subjects) the windows fail, and the forced step's test, run on 2026-11-18, reads flat: the random folds would then stay, with `StationaryRelation` resting on that test.
     - The current line rests on Lennart's domain reason and a comparison of day-grouped with random folds, which is neither the windows nor the test.
   * **Experiments:** stationary-relation test, v3 (2026-11-18), RMSE in °C.

     | Period tested | LightGBM | Kumo-Tabular | Verdict |
     |---|---|---|---|
     | April 2018 | inconclusive | flat (+0.0005 ± 0.0017, floor 0.0011) | flat |
     | March 2018 | inconclusive | flat (+0.0010 ± 0.0072, floor 0.0023) | flat |
     | February 2018 | flat | flat | flat |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | 10 x 3 random folds, `StationaryRelation` on the present line (implemented) | No change | No rebuild | The line's basis is not the rule's test |
     | B | Three two-month windows on the visit date (Nov-Dec 2017, Jan-Feb 2018, Mar-Apr 2018), no gap | The visit day (from the subject id) orders the split, no input; the 48% window signed off | Tests later visitors, as the screening point meets them | 121 to 228 test subjects per window |
     | C | The same random folds, `StationaryRelation` on the v3 test | The Time basis line gives the test | 30 splits on a measured basis | Only open if the window-count item takes its option B |

   * **Recommendation:** B with option A of the window-count item, C with its option B. **Decision:** A, B or C?

   **Notes for the AI:** B as the old issue 2's option B (cutoffs 2017-11-01, 2018-01-01, 2018-03-01, window 2 months); the label is read at the visit, so no gap.

   [^s32w]: **SPLIT-32** (Should, amended 2026-11-17): "Where the windows can be built, the split is temporal however flat the relation, and the measurement goes in the notes as what the windows cost."

   **Answer (AI, 2026-11-18):** reassessed with the new forced step (the interchangeable question first; measured not flat leads to whole periods or Too Small) and the pooled flat verdict.

   - Unchanged: B (windows) if three windows suffice; else C, flat on the v3 test, so the random folds keep `StationaryRelation` on a new line.

   **Andrej (2026-11-19, discuss):** Rerun the stationarity test under our new rules

   **Answer (AI, 2026-11-19):** rerun on the two-month windows the new window rules use: the two windows that train on half the subjects or more read flat; the oldest window, Nov-Dec 2017 at 48% training, reads not flat for Kumo-Tabular, so the pooled verdict is not flat if that window counts.

   * **What changed:** the earlier run tested single months (Feb, Mar, Apr 2018). The new rules ask windows of the use case's length (two months, option B) that train on at least half the data, so the test now uses two-month periods (Nov 2016 to Apr 2018, seven periods of 69 to 226 subjects) and tests the three newest.

     | Test period | Train share | Test subjects | LightGBM gap (RMSE, °C) | Kumo-Tabular gap | Floor | Verdict |
     |---|---|---|---|---|---|---|
     | Mar-Apr 2018 | 82% | 179 | -0.010 ± 0.012, inconclusive | -0.002 ± 0.004 | 0.002 | flat |
     | Jan-Feb 2018 | 60% | 220 | -0.007 ± 0.020, inconclusive | +0.001 ± 0.007 | 0.004 | flat |
     | Nov-Dec 2017 | 48% | 120 | +0.016 ± 0.024, inconclusive | +0.010 ± 0.003 | 0.001 | not flat |
     | pooled, three | | | -0.000 ± 0.011 | +0.003 ± 0.003 (2 SD 2.6 floors) | 0.002 | not flat: one period not flat |

     Gap = forward minus contemporaneous RMSE (positive: training on earlier periods costs), mean ± SD over 5 seeds. The contemporaneous model trains on half of the test period itself (30 to 110 subjects), so the floors are small and the comparison is coarse.

   * **What it means under the rules:**
     - Windows come first wherever they can be built (temporal however flat). Three two-month windows exist only with Nov-Dec 2017 at 48% as your exception; then B (three windows) is the leaf and the test only goes in the notes.
     - Without that exception, only two windows train on half or more, too few, and the forced step reads the test: the two windows it then rests on read flat (C: random folds, `StationaryRelation`); counting the 48% period too, not flat, which leaves whole two-month periods held out (`ForcedGroupedFromTemporal`; seven periods, more than the five that 10 repeats need).

   | | Option | What it does | Splits | Tag |
   |---|---|---|---|---|
   | A | 10 x 3 random folds (implemented) | No change, the line rests on the domain reason | 30 | `StationaryRelation` |
   | B | Three two-month windows, Nov-Dec 2017 at 48% as your exception | The visit day orders the split, no input | 3 | none (temporal) |
   | C | The random folds on the test over the two windows at half or more (flat) | The Time basis line gives this run | 30 | `StationaryRelation` |
   | D | 10 x 3 folds grouped by two-month period | Seven periods held out whole | 30 | `ForcedGroupedFromTemporal` |

   **Recommendation:** B: windows can be built with one window at 48%, the kind of exception you accepted today on five datasets, and the rules put windows first. **Decision:** A, B, C or D?

   **Andrej (2026-11-19, discuss):** The data is too small for just three windows. Can we justify assumed stationary?

   **Answer (AI, 2026-11-19):** it can be argued, but it is not needed: the test measures the relation, and on the two windows that train on half the subjects or more it reads flat, which gives `StationaryRelation` (C) on a measurement. An assumed one would have to set aside a documented change.

   * **For a person's reason:** the camera reads the skin's temperature, and its relation to the oral temperature is physiology that does not change between months; Lennart's reason of 2026-10-21 ("a function that is independent of time"); the room temperature, humidity and distance are inputs.
   * **Against it:** the set-up changed between the two study years (two locations, the distance shortened from about 0.8 to 0.6 m), and a calibration fitted on the first year over-predicts the second by about 0.08 °C (the definition's split text); the one window that reads not flat, Nov-Dec 2017, falls at that change.
   * **What the measurement gives:** the two windows at half the data or more (Jan-Feb and Mar-Apr 2018, 60% and 82% training) read flat for Kumo-Tabular, inconclusive for LightGBM; the rule reads the windows it can test.

   | | Option | Splits | Tag | Rests on |
   |---|---|---|---|---|
   | A | 10 x 3 random folds (implemented) | 30 | `StationaryRelation` | Lennart's domain reason |
   | C | the same folds | 30 | `StationaryRelation` | the test on the two windows at half or more |
   | E | the same folds | 30 | `AssumedStationaryRelation` | your domain reason, the set-up change named |

   **Recommendation:** C: the same 30 folds on a measured basis, with the set-up change and the Nov-Dec 2017 reading in the notes. **Decision:** A, B, C, D or E?

   **Andrej (2026-11-20, discuss):** Reply (C): the same folds

   **Resolved (2026-11-20, Andrej):** C. The 10 x 3 random folds stay, tagged `StationaryRelation`; the `Time basis:` line now rests on the stationary-relation test over the two two-month windows on half the subjects or more (flat for Kumo-Tabular) and names the Nov-Dec 2017 reading at the change of set-up. Not rebuilt.

## Reference

Infrared Thermography for Measuring Elevated Body Temperature: Clinical Accuracy, Calibration, and Evaluation
By Quanzeng Wang, Yangling Zhou, Pejman Ghassemi, David McBride, J. Casamento, T. Pfefer. 2021

Published in Italian National Conference on Sensors
