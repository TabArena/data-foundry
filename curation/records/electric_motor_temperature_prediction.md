---
unique_name: electric_motor_temperature_prediction
name: ElectricMotorTemperature
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 4
tags:
- Non-IID (Grouped)
- Multi-target
- 'Samples: No Time Dimension'
- 'Time: Within Entity'
- 'Entities: Recur'
collections:
- New (BeyondArena)
original_source: Kaggle
year: '2021'
domain: industry & manufacturing
required_split:
- Grouped (NON-IID)
problem_type: Regression
original_data_state: One Table
source_links:
- https://www.kaggle.com/datasets/wkirgsn/electric-motor-temperature
notebook_path: datasets/beyond_iid/grouped/electric_motor_temperature_prediction/electric_motor_temperature_prediction.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/electric_motor_temperature_prediction/dataset.py
source_row: 700
type_adapter_id: curation-record-v1
---

## Comments

CC: ""Signal/time-stream data with groups of sessions, likely needs a group-based split based on `profile_id`; unsure about temporal splits as it would be all from the same time at once, or one needs to set time diff per session

add coolant temperature outlier feature, u_d, motor speed; resolve qd coordinates?
could create three datasets from the three targets; need to remove other target to avoid leakage otherwise (likely torque bad, others two okay, pm best)""

Related link: https://www.kaggle.com/datasets/graxlmaxl/identifying-the-physics-behind-an-electric-motor



See Table 2 in paper for what is measured input and what is measured target (https://ieeexplore.ieee.org/abstract/document/9296842)

Text says 4 target temperatures? are 4 PM, ST, SW, SY, we select PM

CC (2026-10-06, Lennart): Kept after the task-probe sweep of the 2026-10-06 build. The probe flagged `no_spread`: R^2 0.970 (linear), 0.963 (LightGBM) and 0.937 (random forest), and with 3 grouped folds the paired gap (0.026) is within 2 standard errors. The tuned methods spread: on BeyondArena the RMSE of the 21 configurations ranges from 1.77 (RealMLP, tuned) to 3.52 (dummy 22.9), so the task separates methods even though all explain most of the variance.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source mse — Kirchgaessner, Wallscheid, Boecker 2021 (IEEE Trans. Energy Conversion, arXiv:2001.06246) rank and tune by MSE in K^2; the scored metric changes from rmse to mse.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship as defined: the authors' own rotor-magnet temperature task, smoothed inputs from the session's past, whole sessions held out, tuned methods spread widely; the two early modality markers can go. Priority 4: gap 0, use case 1, source 1, shape 1, risk -0.

CC (2026-11-06, Andrej): time basis `Timeless` accepted on the BeyondArena v0.2 review page (issue 2, B, through the cross-dataset item on routine `Timeless` issues): 69 undated bench sessions of designed driving cycles of one motor, each held out whole. The `Time basis:` line is in the definition's notes, ending with what the split cannot test; the tag enters `data_tags` once PR #50 is in the working copy.

CC (2026-11-09, Andrej): ship as defined (review page issue 1, A); the declared split and metric checked and kept. The markers `Wrong Domain / Source Modality` and `Time-series (Regression)` leave the record: the question they recorded is answered (tabular methods spread widely on the vectorised time series).

CC (2026-11-09, Andrej): the record's facts are `Samples: No Time Dimension`, `Entities: Recur` and the new `Time: Within Entity` (review page issue 3, b): the 69 sessions are designed bench runs, each recorded as a 2 Hz series, so time runs inside a session and not across sessions.

## Review

**Outcome:** added. Half-second samples (1,296,316) of 69 test-bench sessions of a prototype permanent magnet
synchronous motor at Paderborn University (Kaggle, Kirchgässner et al., 2021): the rotor magnet temperature, which a
commercial vehicle cannot measure, is predicted from the voltages, currents, speed and coolant and ambient temperatures
and their exponentially weighted means over the session so far. The AI recommends shipping it as defined. Reviewed on
2026-11-04 without a review panel, from the gathered evidence (the record and its earlier decisions; no model run
exists for it). Validity: a direct fit; the smoothed inputs use only the session's past, the stator temperatures and the
torque are dropped as in the study, and whole sessions are held out, so no session has samples on both sides of a split
(the group probe: a sample's nearest neighbour is in its own session for 99.4% of the samples, which is why a random
split would be wrong). Value: the `no_spread` probe flag is settled: tuned methods on BeyondArena range from RMSE 1.77 K
(RealMLP, tuned) to 3.52 K, against 22.9 K for the dummy (Lennart, 2026-10-06). Quality: nothing open; the metric is the
study's MSE (settled 2026-10-21). Weighed: the authors' own benchmark task with a stated use (+), a wide spread of
methods (+), one prototype motor on a bench (-). The record still carries two early triage markers that question the
modality (issue 1).

**Main points:** Ship as defined (issue 1); the split by session named `Timeless` (issue 2); the record's facts with the
new `Time: Within Entity` (issue 3). All resolved.

**Record judgment:** valid. A sensor stream turned into rows by the study's own smoothing, so each sample is one
prediction from the session's past; one motor, so the task tests new driving cycles, not new motors.

**Issues for Andrej:**

1. **Ship as defined?**

   * **Problem:**
     - Nothing open was found: the inputs are known in real time, whole sessions are held out, and tuned methods spread
       widely, so the `no_spread` flag is settled.
     - The record still carries `Wrong Domain / Source Modality` and `Time-series (Regression)` from its first triage,
       when it was open whether a stream of sensor samples is a tabular task; the source answers it with tabular models
       on smoothed inputs.
     - Ship as defined, or name what is missing?
   * **Background:** a stream of readings is in scope when it is turned into rows on which tabular models are
     competitive, and out where sequence models are clearly better[^1a]. The source's benchmark compares linear
     regression, support vector regression, k-nearest neighbours, randomised trees and neural networks on the smoothed
     inputs, all tabular models (Kirchgässner, Wallscheid, Böcker, "Data-Driven Permanent Magnet Temperature
     Estimation in Synchronous Motors with Supervised Machine Learning: A Benchmark", IEEE Transactions on Energy
     Conversion 2021;36(3):2059-2067, https://doi.org/10.1109/TEC.2021.3052546, arXiv:2001.06246; read from its
     abstract only, the body was not re-read for this review).
   * **Experiments:** from the task-probe review of 2026-10-06: untuned probe models reach R² 0.94 to 0.97 on the
     three session-grouped folds; the tuned BeyondArena methods spread from RMSE 1.77 K to 3.52 K, the dummy 22.9 K,
     so the task separates methods[^1b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship as defined (implemented) | 1.30M samples of 69 sessions, held out by session, scored by MSE in K² | the source's own task and split; tabular methods spread widely | one prototype motor on a bench |
     | B | Retire as a time-series task | the folder goes, the record gets `No` | none found | drops a task whose source solves it with tabular models on smoothed inputs |

   * **Recommendation:** A, and the two markers can leave the record, as the question they record is answered.
     **Decision:** ship as defined (A), or retire (B)?

   **Notes for the AI:** on A, remove `Wrong Domain / Source Modality` and `Time-series (Regression)` from the record's
   `decision_markers` with a `CC (<date>, Andrej)` line, and add `Andrej` to `checked_by`.

   [^1a]: **SEL-12** (Must): data from a non-tabular modality is out where modality-specific models are clearly
     better, judged per dataset; vectorised time-series data is fine where tabular models are competitive.
   [^1b]: **TP-3** (Must): if tuned methods spread, keep the dataset. Recorded for this dataset in the task-probe
     cases (2026-10-06, Lennart).

   **Resolved (2026-11-09, Andrej):** ship as defined (A); the declared split and metric checked and kept. The markers
   `Wrong Domain / Source Modality` and `Time-series (Regression)` left the record, as the question they recorded is
   answered.

2. **Time basis: name the split by session `Timeless`, as designed runs on a test bench?**

   * **Problem:**
     - Each of the 69 sessions is a designed driving cycle of one prototype motor on a test bench, and the magnet temperature is measured at the same half second as the inputs, so the target is the motor's physical response to the session's inputs, which the smoothed features carry from the session's own past.
     - The sessions carry no date or recording order, and the split holds out whole sessions, tagged `Non-IID` and `Grouped`, with no time basis.
     - Name it `Timeless`, or a `StationaryRelation` argued from the source?
   * **Background:** the outcome of a designed run is `Timeless`, split at random or by run; a present state read
     through a relation that time does not move is a `StationaryRelation`, measured on dated data or argued from the
     source where time is lost[^2t1]. Time within a session matters and is in the features, which smooth over the
     past only; whole sessions are held out, so no session's later samples inform its earlier ones. Across sessions
     only an ageing motor could move the relation, which no session date lets us check. The vehicle use case comes
     later in calendar time, but runs on the same physics.
   * **Effect on the task:** none on rows, splits or scores.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | By session, no time basis (implemented) | as now | none found | the score's time meaning is not stated; `dataset check` notes the missing basis |
     | B | By session, named `Timeless` | `data_tags` gain `Timeless`; a `Time basis:` line names the designed sessions | the sessions are designed runs and the target their physical response | the samples within a session do arise over time, which the tag's name hides |
     | C | By session, named `StationaryRelation` | `data_tags` gain `StationaryRelation`; the line argues from the source that the thermal relation does not move | names a present state read through physics | the prototype is meant for samples arriving over a period, measured where dated; here it rests on argument alone |

   * **Recommendation:** B: designed runs are the prototype's own example, and the within-session time is handled by
     the features and the grouping. **Decision:** A, B or C?

   **Notes for the AI:** once PR #50 is in, on B: `data_tags = ("Non-IID", "Grouped", "Timeless")` (the definition
   lists the regime tags itself) and the curation bullet "- Time basis: Timeless: 69 bench sessions of designed
   driving cycles of one prototype motor; the magnet temperature is the motor's physical response to the session's
   inputs, carried by smoothed features of the session's own past; whole sessions are held out. The sessions have no
   dates, so an ageing of the motor between sessions cannot be checked."; on C the same with `StationaryRelation`;
   `dataset check` (the grouping's `time_on` is the sample index within a session, not a time to split on).

   [^2t1]: **SPLIT-32** (Should): a definition can name the use-case prototype it follows, with a `Time basis:` line
     stating the fact. `Timeless`: the target is a fixed property of the item, the same whenever it is measured (a
     material's strength, the outcome of a designed run); the split is random or grouped by item family.
     `StationaryRelation`: the target is a present state read through a relation that time does not move, measured on
     a dated source and argued from the source where time is lost.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the routine `Timeless` time
   issues with one mark?" The `Time basis: Timeless:` bullet is in `curation_comments`, ending with what the split
   cannot test (another motor); the split and `data_tags` are unchanged. The line keeps the drafted point that the
   undated sessions cannot show an ageing of the motor. The tag `Timeless` enters `data_tags` once PR #50 is in the
   working copy.

3. **Correct the record's collection facts: `Samples: No Time Dimension` for designed bench sessions?**

   * **Problem:**
     - The record's `Time: Dated` rests on `profile_time_index`, the sample number within each session, and an order found only within each entity does not count as dated time; the sessions themselves carry no date or order.
     - The sessions are designed driving cycles, the case `Samples: No Time Dimension` names, while within a session the samples do arise over time at 2 Hz.
     - Set `Samples: No Time Dimension`, or keep `Samples: Over Time` with `Time: Lost`?
   * **Background:** the record describes the source by independent collection facts, true whatever task is built on
     it[^3t1]. No fact names a stream inside designed runs, so either value leaves something out.
   * **Unknown:** whether the Kaggle page's version history dates the sessions coarsely (sessions added in a later
     version); not checked.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | `Samples: Over Time`, `Time: Dated` (implemented) | as now | none found | dated only by an order within sessions, which does not count |
     | B | `Samples: No Time Dimension` | both tags replaced | the sessions are designed runs, whose calendar time plays no role | hides the 2 Hz stream within a session |
     | C | `Samples: Over Time`, `Time: Lost` | `Time: Dated` replaced | the sessions were recorded over a period whose dates are gone | reads the bench sessions as a stream over calendar time |

   * **Recommendation:** B, with issue 2's B; C if issue 2 takes C. **Decision:** A, B or C?

   **Notes for the AI:** on B, the record's `tags` lose `Samples: Over Time` and `Time: Dated` and gain `Samples: No
   Time Dimension`; on C, `Time: Dated` becomes `Time: Lost`; a `CC (<date>, Andrej):` line with the reason, and
   `Andrej` in `checked_by`.

   [^3t1]: **SPLIT-32** (Should): the record's collection facts: `Samples: No Time Dimension` (designed runs, or a
     catalogue where it plays no role when an item was measured), `Samples: One Moment` or `Samples: Over Time`; for
     samples over time `Time: Dated` or `Time: Lost`, and a time order found only within each entity (a policy's
     terms) does not count.

   **Andrej (2026-11-06, discuss):** But there is a temporal component within a profile or session, right? Could this be
   another tag to add?

   **Answer (AI, 2026-11-09):** yes: inside each session the rows are a 2 Hz time series of one designed load profile,
   so time runs within a session and not across sessions. Record it as a fact of its own (b), or only in the
   definition's notes (a)?

   * **Problem:**
     - Each of the 69 sessions is one designed run on the test bench, recorded at 2 Hz: consecutive rows of a session
       are half a second apart, and the temperatures carry over from row to row.
     - The record's facts cannot say this. `Samples:` describes when the sessions arose (designed runs: `No Time
       Dimension`), and the `Time:` fact leaves out "an order found only within each entity".
     - The same shape recurs: a patient's visits (dementia_prediction), a customer's monthly snapshots
       (santander_transaction_value), a patient's admissions (sepsis_survival_minimal_clinical_records). Their facts
       issues argue between `Time: Dated` and `Time: Lost` today.
   * **What the order changes:** neighbouring rows of a session are near copies, which the split by session already
     holds out together; and a use case of online estimation may use the session's own past (lags), which the definition
     does not build. Neither changes the split. The fact would say why a split by session is needed and which features a
     use case could add.
   * **Options:**

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | a | Notes only (the issue's B) | `Samples: No Time Dimension` and `Entities: Recur`; the 2 Hz order inside sessions written in the definition | no new tag | the order is invisible in the facts; the other datasets keep their Dated-or-Lost question |
   | b | A fact for it | as a, plus `Time: Within Entity`: an order or timestamp that runs only inside each entity (a session's samples, a patient's visits) | the facts say it; dementia, santander and sepsis get the same answer | one more value in the vocabulary |

   * **Recommendation:** b: the shape recurs in at least four datasets, and the fact tells a reviewer that rows of one
     entity are a sequence, which the grouping and any lag features rest on. **Decision:** a or b?

   **Notes for the AI:** on b, `Time: Within Entity` goes into the vocabulary and into the `Time:` fact of SPLIT-32 in
   PR #50 ("an order found only within each entity is `Time: Within Entity`, not `Dated`"); this record's `tags` take
   `Samples: No Time Dimension`, `Entities: Recur` and `Time: Within Entity` in place of `Samples: Over Time` and `Time:
   Dated`; dementia_prediction 4, santander_transaction_value 3 and sepsis_survival_minimal_clinical_records then get
   answers proposing the same. On a, the issue's B plus `Entities: Recur`, and a curation bullet on the 2 Hz order.

   **Resolved (2026-11-09, Andrej):** b: the new fact `Time: Within Entity` is in the vocabulary and in SPLIT-32 (PR
   #50); the record's `tags` carry `Samples: No Time Dimension`, `Entities: Recur` and `Time: Within Entity`.

## Reference

@article{kirchgassner2020estimating,
  title={Estimating electric motor temperatures with deep residual machine learning},
  author={Kirchg{\"a}ssner, Wilhelm and Wallscheid, Oliver and B{\"o}cker, Joachim},
  journal={IEEE Transactions on Power Electronics},
  volume={36},
  number={7},
  pages={7480--7488},
  year={2020},
  publisher={IEEE}
}
