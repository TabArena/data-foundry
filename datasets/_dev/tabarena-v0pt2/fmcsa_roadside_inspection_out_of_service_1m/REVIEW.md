# fmcsa_roadside_inspection_out_of_service

**Outcome:** added as `fmcsa_roadside_inspection_out_of_service_1m`. FMCSA's roadside inspections of December 2024 to October 2026 (5,518,542 rows from the national inspection database, downloaded 2026-11-09), with "was the driver, the vehicle or the load put out of service" as the target, the carrier's and the vehicle's history of the year before as inputs, and August, September and October 2026 as monthly test windows (each train side a random 1M of the earlier inspections); the AI recommends shipping it after a rebuild that freezes the history at each window's start (issue 1), with test labels that have had less time for corrections shipped under a note and a re-download condition (issue 2).

**Main points:** Rebuild so a later test row cannot reveal an earlier one's outcome through the carrier history (issue 1); ship with test labels less corrected than training labels (issue 2); keep or drop the free-text site (issue 3).

**Record judgment:** valid with a direct fit. Picking which truck to inspect is a decision FMCSA's Inspection Selection System supports; the panel moved the prediction point from the start of the inspection to the selection, so the level performed (worth 0.057 ROC AUC, partly set by what the inspector saw) and the two enforcement flags of unknown timing were dropped. The history is built only from inspections in the database before the inspection date. Value: about 0.73-0.74 ROC AUC without the level, against 0.58-0.59 for the carrier's past out-of-service share; 5.5M real rows from a federal source. Quality: cargo-tank codes and blanks cleaned. Weighed: size and source for, the rolling source and label maturity against. Open: the carrier history lets one test row reveal another's outcome (issue 1, a rebuild); the newest months' labels have had less time for corrections (issue 2); keep the free-text site (issue 3).

**Issues for the curator:**

1. **Rebuild so that each test window's history is frozen at the window's start?**

   * **Problem:**
     - Every history count is correct at its own row's date, but a later test row of the same carrier counts an earlier test row's outcome, so the change of its counts reveals that outcome.
     - The panel's task gamer showed this for the vehicle's history (+0.010 to +0.034 ROC AUC); the vehicle's days since its last inspection, which made the chain easy, is dropped and a protocol line forbids using other test rows.
     - A check run after the panel (the finisher's) found that the carrier's history links test rows the same way, and its gain is far above noise, so the protocol line alone does not close it.
   * **Effect on the task:** a participant who links test rows of one carrier gains about 0.01 ROC AUC from outcomes a deployed model would not have; the protocol line forbids it, but nothing in the data prevents it.
   * **Experiments:** the finisher, on the shipped rows with the level, the two flags and the vehicle's days since dropped: each test row was matched to the carrier's next test row (same carrier state, interstate flag, docket flag and reporting state; that row's last carrier inspection on this row's date; one more carrier inspection in the year). 10-13% of test rows match; they are out of service at 35-37% when the next row's out-of-service count rose against 15-17% otherwise. LightGBM (300 trees, a random 300k of each train side):

     | Window | Baseline | With the carrier chain | Gain | Random noise column |
     |---|---|---|---|---|
     | October 2026 | 0.7299 | 0.7384 | +0.0085 | -0.0001 |
     | September 2026 | 0.7327 | 0.7437 | +0.0110 | -0.0001 |
     | August 2026 | 0.7243 | 0.7367 | +0.0124 | -0.0001 |

     The match uses only shipped columns; a participant with the carrier's DOT number from the public file would match more rows.
   * **Consistency:** the precedents of this kind (github_pull_request_acceptance, medical_facility_operational_data, sepsis_prediction, 5g_energy_consumption) shipped with the protocol line alone[^leak9]; the mediator made it a condition here: if the carrier gain is above noise, freeze the history at the window start. Freezing makes the test rows' history what a model refit at the window's start would hold, which is also how the monthly refit of the use case works.
   * **Panel:** the task gamer found the vehicle chain; the mediator made the carrier check a condition of closing the leak, and no agent argued for keeping a measured chain. The check ran after the panel, so no agent has seen the number.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Protocol line only (implemented) | test rows keep their history to their own date; a participant may not use other test rows | no rebuild; history as fresh as the inspector's lookup | the gain stays in the data; follows the protocol-line precedents but not the mediator's condition |
     | B | Freeze the test rows' history at the window's start | a rebuild: for a test row, count only inspections in the database before its window began (training rows unchanged) | closes the chain in the data; matches a monthly refit | needs a per-window history, so test rows of one window and the same rows as training rows of a later window differ; up to a month staler history for test rows |

   * **Recommendation:** B: the gain is about 20 times the noise, so the mildest step (the protocol line) does not close the leak, and a model refit monthly would see the same frozen history. **Decision:** A or B?

   **Notes for the AI:** on B, build the history per window: in `prepare_inspections` compute, for each window start s, the carrier and vehicle sums with `query_day = min(day, s)` for the window's test rows (and `window_sums` / `last_event_before` on `add < s`), store them as extra columns `<col>@<window>` in the prepared file, and pick the window's set for its test rows if the v2 API lets a row take different values per split. If it does not, the alternative is to freeze every row's history at the start of its month (one value per row, valid for all splits): count only inspections added before the first day of the row's month. Then re-run the carrier-chain check (the finisher's `carrier_chain.py` in the run's panel folder), `dataset check` and the probes.

   [^leak9]: **LEAK-9**: an evaluation leak, where one test row reveals another's outcome, is closed by the mildest step that works: a protocol line, then coarsening the column, then a rebuild. Mediator: 'This is a check, not a weighing. The rule (LEAK-9) settles it once the number is in.'

2. **Ship with test labels less corrected than the training labels?**

   * **Problem:**
     - The view holds each record as last changed, and the share of changed records falls from 12-16% in the months of 2025 to 10.4% (August 2026), 6.2% (September) and 3.9% (October), the three test months.
     - Changed records are out of service at 29.2% against 18.0% for unchanged ones, so test labels and training labels sit at different stages of correction.
     - No rule settles fresh test months against settled labels; every earlier case cut or replaced the unsettled period before shipping[^leak24].
   * **Effect on the task:** a model learns from labels that had a year or more to be corrected and is scored on labels that had weeks; which way the test labels are biased is unknown, since a correction (a DataQs challenge) can add or remove an out-of-service order. The carrier's and the vehicle's history columns also read past outcomes as corrected later.
   * **Experiments:** the claim auditor, from the transaction code of every task row: changed share 12-16% (2025), 8.2% (June 2026), 6.8% (July), 10.4% (August), 6.2% (September), 3.9% (October); the curve does not flatten within the history the view covers, as August is back near 2025 levels. The rise of the out-of-service share (16.5% to 21.5%) also holds among records never changed (11.5% and 15.1% early to 20.9%), so it is drift, not an artefact of corrections. The notes now give these numbers (the old note said the changes "cannot be located", which the claim auditor refuted).
   * **Consistency:** sf_permit_time and tunisian_fraud_detection_challenge cut their unsettled newest period and consumer_complaints re-sourced it; none shipped a measured unsettled period with only a revisit. Option A would depart from them and needs its fact written as an exception: the changed share does not level off within the three years the view holds, so no older window is settled either. Whether the label-revision rule should depend on how much a revision measurably moves the labels is an open across-datasets item (raised from wioa_employment_after_exit)[^leak24]; this issue follows whatever it settles.
   * **Panel:** the advocate, the builder, the split and claim auditors and the domain practitioner would ship with the note and a re-download condition (the label exists at upload; this is a revision, not censoring); the critic and the precedent checker would move the windows earlier, following the precedents; the mediator leans to A with the revisit written as a condition, and finds no conflict of rules, only a weighing.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship with the note and a re-download condition (implemented) | the notes give the changed share per month and the drift fact; a second download in about three months is compared on the August to October 2026 labels and the windows move if they changed materially | fresh windows; full training history; the test months are what a monthly refit faces | departs from three precedents; the size of the label shift is unknown until the second download |
     | B | Move the windows earlier | test months where the changed share has levelled off | follows the precedents | the share does not clearly level off before early 2026 or 2025; staler windows and less training history; the first task months lose their full year of history |
     | C | Wait for the second download | hold the dataset until a download about three months from now measures how much the newest labels move | settles the question with a measurement | blocks the dataset for months; the view will have dropped December 2023 by then, so the history of the first task months can only come from this download |

   * **Recommendation:** A, recorded as an exception with its fact (no settled window inside the three years the view holds), with the re-download as a written condition. **Decision:** A, B or C?

   **Notes for the AI:** on A, add to the record a `CC` line with the exception: "LEAK-24 exception: the changed share does not level off within the view's three years (12-16% in 2025, 10.4%/6.2%/3.9% in Aug/Sep/Oct 2026), so no older window is settled; ship with the note and re-download about 2027-02, compare the Aug-Oct 2026 labels, move the windows if the out-of-service share of a test month changes by more than about a point." Add the revisit sentence to the changed-records note in `curation_comments`. On B, compute the changed share by months of upload age on the full download first and set `TASK_END` and the windows to the first months past the flat point; re-run `dataset check` and the probes. On C, set the record's status to wait and note the date.

   [^leak24]: **LEAK-24** (Must): a newest period whose labels a later download revises is cut or re-sourced; test by comparing two downloads. Precedents: sf_permit_time (cut), consumer_complaints (re-sourced), tunisian_fraud_detection_challenge (2026-11-04, newest year cut). **LEAK-10** clause 2: values recorded after the prediction point leave.

3. **Keep the free-text site `location_desc`?**

   * **Problem:**
     - `location_desc` is the site as the inspector wrote it, free text with about 24,000 distinct values among the shipped rows.
     - The county, a coarser place column, ships as well.
     - It carries no outcome: one row of the shipped data has text that reads like an out-of-service note.
   * **Effect on the task:** it lets a model tell sites apart within a county; site rates differ, so it can help a pooled score. As a string column it tests text handling.
   * **Experiments:** the column auditor searched it for out-of-service wording (one row); the task gamer's count of rows sharing a date and site gave no gain (0.7861/0.7920/0.7868 against 0.7865/0.7926/0.7873; scores of the task gamer's model, which still had the inspection level).
   * **Consistency:** free-text place columns ship as strings elsewhere when known at the prediction point, with no leak found[^clean].
   * **Panel:** the blind reviewer would drop it and keep the county; the advocate and the critic say it does not change the verdict; the mediator leaves it to you.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as a string (implemented) | the site as written | known when the vehicle is picked; finer than the county | many spellings of one site; most models treat it as a high-cardinality category |
     | B | Drop it | the county stands for the place | simpler table | loses the site within a county |

   * **Recommendation:** A, as known at the prediction point with no leak found. **Decision:** A or B?

   **Notes for the AI:** on B, remove `location_desc` from `RAW_COLUMNS`, `_clean`, the `string` feature types and the "Kept as known" note, then re-run `dataset check`.

   [^clean]: **CLEAN-10**: a column known at the prediction point stays unless it is an identifier or carries the outcome; **CLEAN-12**: codes and free text are cleaned to what the source means.

**Review panel:** ship after changes (mediator). Claim audit: the claims hold except "the changed records cannot be located" (the transaction code locates them by month; corrected, issue 2). Column audit: no new leak; `cargo_tank` NON and blanks cleaned. Split audit: right with notes (monthly windows, 7-day gap for the upload delay). Domain practitioner: a real selection task once the level performed is dropped. Blind review: would benchmark; would drop `location_desc` (issue 3). Task gamer: later test rows of the same vehicle reveal earlier outcomes (+0.010 to +0.034 ROC AUC); the vehicle's days since its last inspection dropped and a protocol line added; a check after the panel found that the carrier history links test rows too (+0.009 to +0.012, issue 1). Applied: the level, the two enforcement flags and the vehicle's days since dropped, the pooled-score note, the cleaning, the corrected-labels note; the raw CSVs archived in the local warehouse, with their sha256 in the notes (the view drops a day each day and the bulk export ends 2026-12-22); the two partial bulk downloads in the warehouse were deleted on 2026-11-09 with the curator's OK. Debate: the advocate's and the critic's opening briefs converged, so the rebuttal round was skipped; agreed: the drops and the notes; disputed: ship with less-corrected test labels or move the windows (issue 2), keep `location_desc` (issue 3).

<details><summary>Mediator</summary>

Mediator report: fmcsa_roadside_inspection_out_of_service_1m (2026-11-09). There were no rebuttals; I worked from the seven phase-A reports, both opening briefs and builder_report.md. I ran no new experiment. One cheap check is still needed before the leak can be called closed: whether the carrier history chains the same way as the vehicle history (change 2).

JUDGMENT RECORD
Verdict: ship after changes. There is one open curator issue (the corrected-labels gap), and it does not block shipping.
Validity: SEL-1 holds. USE-1 holds; the fit is direct once inspection_level is dropped, because the prediction point then becomes the selection decision. LEAK-10 cl.2 is triggered: inspection_level (0.057 AUC, about 28 SE) is fixed by dropping it, and the enforcement flags are dropped too. LEAK-9 is triggered (vehicle chaining, +0.010/+0.023/+0.034 AUC): fixed by dropping vehicle_days_since_inspection plus a protocol line, pending the carrier check. LEAK-24 / LEAK-10 cl.2 (labels at different correction stages) is open and goes to the curator. SPLIT-1/6/10/13 hold. LEAK-16 is fixed (2,234 copies).
Value: no TP flags. Expected about 0.73-0.74 AUC without the level, against 0.58-0.59 for the carrier's past share and 0.757 for the linear model with all features.
Quality: CLEAN-10/12 items below.
Weighed: size +, source +, gap 0, risk - (rolling source, label maturity).

CHANGES TO MAKE NOW (no decision needed)
1. Drop inspection_level (Must, LEAK-10 cl.2). The advocate concedes. Keeping it would depart from distribution_transformers (2026-10-21); medical_facility does not cover it because 0.057 is not within noise. The prediction point becomes the selection, which is the decision ISS supports. Update the task_summary and the notes to match.
2. Drop vehicle_days_since_inspection, or bucket it by month (LEAK-9, mildest step of the remedy ladder). Add the LEAK-9 protocol line: a model may not use other test rows. Then run the check: chain on carrier_days_since_inspection / carrier_*_1y with the carrier key the features allow, and measure the gain against the 0.0005 noise.
   - If the gain is above noise: freeze each window's history at the window start (a rebuild).
   - If not: keep, and write a `Potential leak, kept on purpose:` note that gives the measured gain.
   This is a check, not a weighing. The rule (LEAK-9) settles it once the number is in.
3. Drop size_weight_enf and traffic_enf (LEAK-10). They are worth 0.0008-0.0024, about one SE, and their timing is undocumented. Both sides accept dropping them. Keeping them with a note would also follow precedent (medical_facility), but dropping costs nothing and removes the question.
4. Metric: keep the fallback roc_auc (MET-1/MET-10). Add a note that pooled AUC may reward between-site base rates. Opening a within-site metric would need a measurement (AUC of the site-month OOS rate alone) and a MET-5 amendment as the third case; that stays a cross-dataset question for the review page.
5. Cleaning (CLEAN-10/12):
   - map cargo_tank "NON" (8,677 rows) to none,
   - encode NaN in hazmat_placard_req and cargo_tank as not applicable,
   - cast unit1_model_year to float.
6. Correct claim 30 in the README: "cannot be located" is wrong, because transaction_code locates the changes per month. Give the change share per month in the note. Record that the Yes-rate rise also appears in never-changed rows (11.5%/15.1% to 20.9%), so it is real drift (writing.md; EV-2).
7. Archive the raw CSVs (about 4.5 GB) before the merge. This is procedure, not a gate: the view drops a day every day and the bulk export ends on 2026-12-22. The .partial bulk files can be deleted once the curator agrees (warehouse deletions need the curator's OK).

ISSUES FOR THE CURATOR (ranked)
1. Test labels are less corrected than training labels (validity; LEAK-24, LEAK-10 cl.2; P4).
   - Problem: changed records are 12-16% of the 2025 months, 8.2% (Jun 2026), 6.8% (Jul), 10.4% (Aug), 6.2% (Sep) and 3.9% (Oct). Changed rows are out of service at 29.2% against 18.0% for unchanged ones.
   - Effect: train and test labels sit at different correction stages, and the history columns read past outcomes as later corrected. Which way the test labels are biased is unknown, because a DataQs correction can add or remove an OOS order.
   - For moving the windows earlier (critic, precedent checker): every LEAK-24 precedent acted before shipping (sf_permit_time, consumer_complaints, tunisian 2026-11-04). None shipped a measured unsettled period with only a revisit.
   - For a note plus a revisit (advocate, builder, split and claim auditors, domain practitioner): this is a revision, not censoring. The label exists at upload, and LEAK-24's own test is "compare two downloads". The curve does not level off cleanly: Aug 2026 (10.4%) is near 2025 levels, so moving earlier means going back to roughly early 2026 or 2025 and losing freshness and training history.
   - Not a conflict between rules. The rules leave this as a weighing (freshness against maturity), so it is yours to decide.
   - What would settle it, cheaply: the change share by month of upload age on the full download, to find the age where it flattens. Better: a second download about 3 months from now, compared on the Aug-Oct labels.
   - Decision needed:
     - (a) ship now with the note and a written re-download condition,
     - (b) move the windows to months where the change share has levelled off,
     - (c) wait for the second download.
   - My lean: (a) with the revisit written as a condition. The rules leave this open, and the measured gap is moderate against strong drift. If you take (a), record the fact that sets this case apart from tunisian (the change curve does not flatten within the history the view covers) as an exception.
   - The general late-values rule question stays on the review page as a cross-dataset issue.
2. location_desc (Weigh; CLEAN): free text with 24k levels. Only one row has OOS-like text, and county is a coarser place column. The blind reviewer would drop it; the advocate and critic say it does not change the verdict. Your call: keep it or drop it.

AGREED FACTS
- 5,518,542 task rows; 19.45% are Yes. The three windows hold 255,902 / 263,507 / 246,280 rows. Each train side is a 1M sample of 4.69M-5.21M rows.
- Upload lag: median 2 days, p90 7. With the 7-day gap, 0.06-0.16% of train rows are not yet uploaded. October is about 2.1% incomplete, which moves its rate by less than 0.1 points.
- History uses only rows added before the inspection day. A check of 300 rows re-derived by hand found 0 mismatches.
- Copy groups all fall on one day, so none crosses the split.
- 94.5-94.9% of test carriers appear in training. New carriers are out of service at 37-39%.
- Ablation (AUC per window):

| Features | AUC |
|---|---|
| All | 0.794 / 0.802 / 0.794 |
| Without inspection_level | 0.737 / 0.744 / 0.737 |
| Without history | 0.773 / 0.781 / 0.765 |
| Without enforcement flags | 0.0008-0.0024 lower |

- inspection_level is the level performed. Out-of-service rates by level: L1 27.8%, L2 27.4%, L3 6.6%, L5 3.9%.
- Gamer, vehicle chaining: +0.010/+0.023/+0.034 AUC on 6%/14%/19% of test rows. Carrier chaining was not tested.
- Yes-rate drift: 16.5% to 21.5%, and it is present in never-changed rows too.

CONSISTENCY WITH PRECEDENT
- Dropping the level follows distribution_transformers (LEAK-10 cl.2).
- Dropping the flags is consistent; keeping them would also have matched medical_facility.
- Pooled roc_auc matches every classification precedent. A within-site metric would need a MET-5 amendment.
- Corrected labels: option (b) follows tunisian and sf_permit_time. Option (a) departs from them. It needs the distinguishing fact written as an exception, or your explicit decision.
- Gamer exploit: it is new. No `Potential leak, kept on purpose:` note or accepted warning covers it, and the leak is not closed until the carrier chain is checked.
- The precedent checker found no drift in how LEAK-10 cl.2 has been decided.

Files: panel reports in (the run folder) and the builder report at (the run folder)

</details>

<details><summary>Claim audit</summary>

Claim auditor: fmcsa_roadside_inspection_out_of_service_1m (2026-11-09)
Data: inspections_with_history.parquet (the builder's prepared file), polars, task rows 2024-12-01..2026-10-31. No container built.

Verdict: ship with notes. No claim refuted outright; one claim (30, "14.3% changed, not locatable") is sharpened into a
measurable train/test label-version gap; metric claims hold as a documented fallback (scorer not re-run: no container).

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 9 | target OOS_TOTAL>0, 19.5% of 5,518,542 rows | claims.md 9, README | recount on prepared file | holds | 5,518,542 rows, 0.19453 | USE-5 |
| 31 | windows 246,280..263,507 rows; train sides 4.69M..5.21M | README front matter | count by month and date < window-7d | holds | Aug 255,902, Sep 263,507, Oct 246,280; train 4,689,962 / 4,944,198 / 5,211,900 | SPLIT-6/10 |
| 34 | train side 85-94% of task rows | claims 34 | same counts / 5,518,542 | holds | 85.0% .. 94.4% | SPLIT-14 |
| 30 | 14.3% change transactions, OOS 28% vs 17%, not locatable | claims 30, notes | change share and OOS rate by month | holds pooled (C 703,671 rows, OOS 29.2% vs A 18.0%), but locatable by month: C share 12-16% in 2025, 8.2% Jun 26, 6.8% Jul, 10.4% Aug, 6.2% Sep, 3.9% Oct 2026 | in-run query | LEAK-24, LEAK-10 |
| 13 (Yes-rate drift) | rise 16.5% -> 21.5% is drift, not censoring | builder probe 13 | Yes rate within A (never-changed) rows by month | holds: A-only rate also rises 11.5%/15.1% -> 20.9%; level 1/2 share rises 0.59 -> 0.65 (explains part) | in-run query | LEAK-24 |
| 15/23 | gross weight is a declared weight, kept | notes | OOS by weight missing; missing by level | holds as harmless: missing 97,620 rows, OOS 13.9% vs 19.6%; missing 1.4-2.1% at levels 1-3, so not a "weighed only when inspected" marker | in-run query | LEAK-10/13 |
| implied | unit_count / VIN known at start, not set by findings | definition | missing by level; OOS by unit count | holds: VIN missing <0.05% at every level incl. driver-only 3; unit_count 1 vs 2 OOS 16.1% vs 21.2% (tractor-trailer, plausible) | in-run query | LEAK-10 |
| implied | no copies across the split | definition | same VIN same day; same carrier/day/start time | holds: 34,430 VIN-day groups (69,449 rows) and 15,644 carrier-day-time groups (32,847 rows; 84% label-pure) all lie on one day, so never straddle train/test (7-day gap); the history excludes same-day rows | in-run query | LEAK-16..21 |
| 29 | level is the level performed, worth 0.057 | claims 29 | level table | holds: OOS 27.8% (L1), 27.4% (L2), 6.6% (L3), 3.9% (L5) | in-run query | LEAK-10 |
| 11 | fallback ROC AUC, no source metric | dataset.py metric, README | ISS doc still 403 per builder; not re-fetched | untested (source unreadable); fallback reason names where looked | - | MET-1 |
| metric computability | roc_auc scorable per fold | MET-2 | dummy score per fold needs container (not built) | untested here; both classes plentiful in each window (>=52k positives by month counts) | counts above | MET-2 |
| 3/4 | rolling view, deprecated export | claims 3-4 | needs second download | untested | - | PROV-9 |

Ranked findings
1. (Validity, LEAK-24/LEAK-10 second clause) Label version differs by window age: training months carry 12-16% change
   transactions (OOS 29% when changed), the October 2026 test window 3.9%, September 6.2%. The leak part is no longer
   "not locatable": the transaction_code column shows it per row. Direction of the label effect is unknown (a change
   can add or remove OOS). Mildest remedy: keep, but rewrite the note with the per-month change share and make the
   builder's issue 2 option (b) (re-download in ~3 months, compare Aug-Oct labels) a revisit condition; option (c) of
   moving windows earlier would trade freshness for maturity.
2. (Note accuracy) Claim 30's "cannot be located" is wrong as written; also note the Yes-rate rise is present among
   never-changed rows (A: 11.5% Dec 2024 -> 20.9% Oct 2026) and partly from more level 1/2 inspections, so drift is
   real and not an artefact of corrections.
Everything else tested holds.

</details>

<details><summary>Column audit</summary>

COLUMN AUDITOR: fmcsa_roadside_inspection_out_of_service_1m
Verdict: ship as is; no new leak found. Three builder issues confirmed; two minor cleaning notes.
Prediction point: start of a roadside inspection (vehicle and level picked). Measurements on task rows (5,518,542) of inspections_with_history.parquet.

COLUMN TABLE (column | meaning | known at prediction? | dtype and cleaning | verdict | rule)
out_of_service | OOS_TOTAL>0 | target | cat Yes/No | fine | -
inspection_date | INSP_DATE | yes | datetime, split key | fine | -
start_minute_of_day | INSP_START_TIME HHMM -> minutes | yes; no nulls/9999 in task rows | numeric | fine | CLEAN
report_state | reporting state | yes | cat | fine | -
county | state FIPS + county | yes | cat (string concat; NA if either missing) | fine | -
location_desc | site free text | yes; 1 row contains "OOS"-type text (checked regex OOS/OUT OF SERV/PLACED) | string | fine | LEAK-10 checked
inspection_level | level performed | mostly yes; may be raised after seeing defect | cat, decoded, 9 missing | potential leak kept (builder issue 1) | LEAK-10
facility | fixed/roadside | yes | cat decoded | fine | -
size_weight_enf, traffic_enf | done with enforcement action | timing undocumented | cat Y/N, U missing | potential leak, weak (0.0008-0.0024 AUC) (builder issue 3) | LEAK-10
local_enf_jurisdiction, post_acc_ind, hazmat_placard_req | flags | yes | cat Y/N | fine | -
cargo_tank | cargo-tank spec code (406, 407, 331, NON, OTH...; 41 codes) | yes | cat, raw codes not decoded; "NON" (8,677 rows) means none and could equal blank (97% blank) | minor cleaning question | CLEAN (codes vs meaning)
gross_comb_veh_wt | declared GCW lb | yes | numeric, 0 and 999999 missing (97,620 null/0, OOS 13.9% vs 19.6%) | fine | CLEAN
carrier_state, carrier_interstate, carrier_has_docket | carrier as recorded | yes | cat; NA/UK/ZZ missing | fine | -
unit_count | units recorded | yes (units are present at start) | numeric count; 1,001 missing | fine | -
unit1_type, unit2_type | unit type codes decoded | yes | cat, 13/15 missing | fine | -
unit1_make | make, 19 spellings merged | yes | cat; dtype-probe flag ordinal_like false | fine | CLEAN
unit1_license_state | plate state | yes | cat; unknown states missing | fine | -
unit1_model_year | from VIN char 10 | yes | numeric | fine | -
carrier_*_1y, carrier_days_since_inspection | history from inspections added to MCMIS before the day | yes (add_date+1 <= day; same-day excluded) | numeric counts, -1 -> NaN | fine, but labels as later corrected (builder issue 2) | LEAK-10/LEAK-24
vehicle_*_1y, vehicle_days_since_inspection | same by valid VIN | yes | numeric | fine (issue 2 applies) | -
vehicle_decals_90d | decals issued to the VIN in prior 90 days | yes (decal physically on vehicle; window uses insp day, not add date, defensible) | numeric | fine; monotone OOS 19.8% (0) -> 12.8% (1) -> 10% (2) | -

PROBLEMS RANKED
1. (P4, LEAK-10) inspection_level is level performed; AUC 0.057 drop; unlocatable. Mildest remedy: keep with note (builder option a). Agree.
2. (P4, LEAK-24) history and labels as later corrected (14.3% change transactions). Keep with note; re-download revisit. Agree.
3. (P4, LEAK-10) traffic/size-weight flags timing; negligible strength. Keep or drop; curator call.
4. (cleaning, minor) cargo_tank keeps raw spec codes; "NON" vs blank may be the same meaning (none). Remedy: map NON to a "None" level or leave; optionally a codebook decode. Question for curator, low weight.
No dropped-column error found: end time, registration date, decal of this inspection, alcohol/drug/search, violation counts all dropped as builder states.

</details>

<details><summary>Split audit</summary>

Split auditor: fmcsa_roadside_inspection_out_of_service_1m
Verdict: RIGHT WITH NOTES.

Regime. Use case is an inspector or the ISS ranking vehicles at the start of an inspection, applied to a live stream
with recurring carriers (known-entity, USE-10/SPLIT-13). Declared: temporal, 3 monthly windows (Aug, Sep, Oct 2026),
gap 7 days, train from 2024-12-01. Matches.

Numbers checked (prepared parquet, all rows before sampling):
- Window sizes 255,902 / 263,507 / 246,280: match the definition.
- Test inspections whose carrier (DOT) appears in the train side: 94.5% / 94.6% / 94.9%. The ~5% new carriers are
  out of service at 37-39% vs 20% for known ones, so the cold-start slice is present in its natural share; a grouped
  split by carrier would misstate the use case (the ISS reads the carrier's record). No re-split needed.
- Hidden-group probe: location_desc / county are places seen in train for 97-98% of test rows (features, SPLIT-4);
  no entity-like hit; near-copy clusters cross the split for 2.6% of test rows; exact copies 0 (probe 5).
- Gap vs label delay: label = outcome at end of inspection; delay = MCMIS upload lag (median 2 d, p90 7, p99 56).
  A 7-day gap leaves 0.06-0.16% of train rows not yet uploaded at window start (builder's measure). Fine (SPLIT-10).
- History features use only records added to MCMIS before the inspection date, within 365 d: no future rows.
- Training history 20 months, covers every season; train side holds 85-94% of task rows; random 1M sample of it, one
  order for all windows (not a recency sample) - acceptable under the v2 protocol.

Notes (ranked by principles.md):
1. P4 / LEAK-24 (kept, builder's issue 2 endorsed): the view holds corrected (DataQs/change) versions; 14.3% of records
   are change transactions, OOS 28% vs 17%. Train labels and history have had more time to be corrected than the
   Aug-Oct 2026 test labels, so train and test labels differ in maturity. Mildest remedy: keep with the note now; revisit
   by re-downloading in ~3 months and comparing Aug-Oct labels; if the drift is material, move the windows one or two
   months earlier (a larger effective gap for the test labels).
2. P4 / SPLIT-10 (minor): the October window is ~2.1% incomplete (late uploads, less often OOS); effect on the rate
   under 0.1 pt. No action.
3. Seasonality: three consecutive late-summer/autumn months; the base rate drifts upward (16.5% Dec 2024 -> 21.5%
   Oct 2026). Acceptable for a monthly refit; note only.
No alternative-split fit run: no doubt about the regime.

</details>

<details><summary>Domain practitioner</summary>

Domain practitioner: fmcsa_roadside_inspection_out_of_service_1m (2026-11-09)
Actor: a roadside/weigh-station inspector (or FMCSA's Inspection Selection System, ISS) choosing which truck to pull in and how deep to inspect it.

FIT: approximate (USE-1). The rows, target and monthly refit match a real screening task, but the moment of decision the actor actually faces (pull in or wave through, and at which level) comes BEFORE the level is known, and the level as recorded is the level performed. This is also the strongest feature.

1. Inputs at the moment of decision
- I have: date/time, site, state, the plate, the USDOT number (so the carrier's record), the unit types, make, the model year (from the VIN once I am at the truck), hazmat placard, cargo tank. The rebuilt carrier and vehicle history stands in fairly for what ISS reads (it reads CSA BASIC percentiles, which are not public: USE gap, documented).
- I would NOT have: the inspection level as performed (issue 1). ISS recommends a level *as part of* the selection (inspect / optional / pass, and the level). A driver-only level 3 cannot produce a vehicle OOS order (0.7%), so most of its 0.057 AUC is structural: "we did not look at the vehicle". The model learns "deeper inspection finds more" more than "this truck is risky". I would prefer (b) dropping it as the main task framing (the prediction point becomes the selection, which is the decision ISS supports), or at least an explicit task_summary saying the level is fixed by design. I disagree with the builder's recommendation (a) because the README's "judged when the inspection starts" is only true for a planned level.
- Enforcement flags (issue 3): a traffic stop comes before the inspection in practice (the reason for the stop). A size/weight action can follow the scale. The value is tiny. Keep or drop, whichever is cheaper. Dropping it is safer.
- Missing that I would always have: the carrier's CSA/ISS score and out-of-service status orders. These are not public, so accept it.

2. Target: OOS_TOTAL>0 is what I act on (pulling a vehicle off the road), a good direct target. I would want a probability to rank trucks within the queue at my site. The driver vs vehicle split matters for the level choice, but a single binary target is acceptable.

3. Row/decision/test: one row = one inspection = one decision. That is right. Next-month test windows match a monthly refit. Selective labels (only inspected trucks) are acceptable per selection.md. Note that ISS-selected trucks are already enriched (USE gap, low impact). Issue 2 (labels corrected after upload, DataQs) slightly deflates the newest month's OOS. Keep (a) with re-download as the revisit (LEAK-24). Issue 4 (archive the raw files) is a procedure issue, not a fit issue, but it is needed.

4. Would I use it? Yes, as a screening aid alongside ISS, if it ranks trucks well among those passing MY site on a given day. I would distrust it if its lift came from the level, the state or the site base rates (where enforcement intensity differs) rather than from the truck and carrier.

5. Metric: partly (MET-1, MET-8). A pooled national ROC AUC ranks across sites and states whose OOS rates differ widely (inspection culture). Much of the score can come from "which state/site" rather than "which truck here". My decision is a ranking within a site-day queue, with a capacity of k inspections. I would choose roc_auc averaged within site (or state) by month, or log_loss if probabilities feed a threshold policy (MET-8; no source cost or k, so MET-7 does not apply; imbalance 19.5% gives no reason for PR AUC, MET-9). Pooled roc_auc is an acceptable fallback (MET-10). Record the within-group concern in the notes.

Ranked gaps: (1) level performed vs chosen, a 0.057 structural signal at the wrong prediction point; (2) pooled AUC rewards between-site base rates; (3) no CSA scores (proxy history); (4) post-upload label corrections; (5) enforcement-flag timing.
Expert change: frame the task as the selection decision without the level (or with only the planned level, if it were recoverable), and score within site/state.
Sources: dataset.py/README.md of the folder, builder_report.md (ablation, probes), use_case.md USE-1/5, metrics.md MET-1/7/8/9/10, FMCSA ISS description as cited in the definition (ISS_Algorithm.pdf, unread by the builder). No new web lookups (effort medium).

</details>

<details><summary>Blind review</summary>

Blind review: fmcsa_roadside_inspection_out_of_service (clean room)

FMCSA roadside inspection out-of-service (blind review)
Verdict: include with changes. It is a real, large regulatory task with moderate signal and no leakage I could find.
Task: predict whether a roadside commercial-vehicle inspection ends in an out-of-service order, using inspection context, the vehicle, and the carrier's and vehicle's history over the prior year. Real users: inspector triage and site selection (as in FMCSA ISS/PRISM), and carrier risk scoring.
Data: 200k-row sample of 1.78M rows, Dec 2024 to Oct 2026. OOS rate is 20.0%. No exact duplicate rows. Values look plausible: gross weights, Freightliner as the top make, model years.
Signal: LightGBM, train before 2026-05 and test after. AUC is 0.778 with all features, 0.755 without the history features, and 0.649 with inspection_level alone. Not trivial, and there is headroom.
Concerns, most serious first:
1. inspection_level is fixed partly during the stop. Driver-Only has 7% OOS, Full/Walk-Around 28%. Officers often escalate the level after they see a problem. It is legitimate only if the level is chosen before the inspection. I could not verify this from the source. Consider documenting it, or offer a variant without it.
2. History features (carrier_*_1y, vehicle_*_1y, days_since): I could not verify that they exclude the current and same-day inspections. Indirect checks look fine: no oos>inspections, 38% have vehicle_inspections_1y=0, and the quarterly medians are stable from the first month, so the windows seem to reach back before 2024-12. Confirm the cutoff is strictly before inspection_date.
3. Drift: the OOS rate rises from 16.9% (2024Q4) to 21.6% (2026Q4). The temporal split is right for this, but expect calibration shifts between windows.
4. Preparation: location_desc is free text with 24k levels. Drop it, or keep county (2.8k levels, 2.4% missing) instead. Very sparse columns: hazmat_placard_req is 95% NaN and cargo_tank 97%; NaN probably means "not applicable" and should be encoded that way. unit1_make has 650 levels with dirty spellings. unit1_model_year is a nullable Float64 and should be cast to float.
5. Repeated carriers appear across train and test (there is no carrier ID column, but the history features act as one). This is fine for the stated use.
Not checked: the full 1.78M rows, how the source tables were joined, whether out_of_service covers driver and vehicle OOS together, and whether the history features are as-of correct.

</details>

<details><summary>Task gamer</summary>

Task gamer: fmcsa_roadside_inspection_out_of_service_1m (participant kit)

Verdict: the task can be gamed by roughly +0.01 to +0.03 AUC. The test window holds later inspections of the same vehicle, and their history counts already include the outcome of earlier test rows.

Setup: LightGBM with 300 trees and 63 leaves, trained on 300k rows sampled from each 1M-row training set, scored on the full test windows. 
Honest baseline AUC: r0f0 0.7865, r1f0 0.7926, r2f0 0.7873.
Random-noise column: 0.7862, 0.7920, 0.7871. Noise spread is about 0.0005.

| # | Exploit | Script | Honest | Exploited | Gain per split | Deployed model has it? | Fix |
|1| Next-row vehicle history: match each row to the same vehicle's later row and take the change in vehicle_oos_1y | (A) | 0.7865/0.7926/0.7873 | 0.7966/0.8154/0.8213 | +0.010/+0.023/+0.034 | No | see below |

Exploit 1, mechanism:
- Rows carry no vehicle id. A vehicle can still be rebuilt from make, model year, plate state and carrier state.
- A later row of the same vehicle has inspection_date - vehicle_days_since_inspection equal to this row's date, and its vehicle_inspections_1y is this row's count + 1.
- On that later row, vehicle_oos_1y has gone up by this row's label.
- About 14% of all rows find a unique match. Within the test windows, coverage is 6%, 14% and 19%; the latest window gets the least because it has the fewest later rows.
- On matched test rows, P(OOS) is 0.59-0.68 when the delta is >0 and 0.05-0.07 when it is 0. The base rate is about 0.21.
- The same trick should work on the carrier_*_1y counts with a better carrier key. I did not build that, so the gain above is a lower bound.

Exploit 1, fix (mildest first):
- Drop vehicle_days_since_inspection, or bucket it coarsely (for example by month), so a row cannot be chained to an exact earlier date.
- Or round the *_1y counts.
- Or compute each test window's history features only from rows before the window starts. This needs the build pipeline.

Flaws that hurt an honest model: none found. Each training set is a 1M-row sample. I did not test dropping old rows.

Attacks that found nothing (AUC per split, r0f0/r1f0/r2f0):
- Row order:
  - Correlation of row index with the label is 0.03, which only follows the date order.
  - Next-row label agreement is 0.680, against 0.679 by chance.
  - Position within the day as a feature: 0.7867/0.7922/0.7868, no gain.
- Test-set statistics: number of rows on the same date and location_desc, 0.7861/0.7920/0.7868, no gain.
- Format artefact: gross_comb_veh_wt being a multiple of 1000, 0.7867/0.7926/0.7875, no gain.
- History counts include only earlier days: the days_since columns have minimum 1, so no same-day leak.
- Missing values: a missing carrier history (first inspection) has OOS rate 0.34. This is real signal that a deployed model also has.

Not checked:
- Exact or near copies of rows across the split.
- Carrier-level chaining.
- Web forums: this source has no competition or known "magic feature".
- Lookup of the rows in the published DOT files. This should work, but it is not a flaw of the task.

</details>

<details><summary>Precedent check</summary>

Precedent checker: fmcsa_roadside_inspection_out_of_service_1m (2026-11-09)
Sources: register.json (5,664 decisions), .claude/skills/knowledge-curation/references/leak_checks.md (LEAK-10 text and
Mechanisms table rows 477, 488, 489; LEAK-24), metrics.md (MET-5 Cases rows 323, 328, 329, 342), principles.md
Tensions (row 102), sibling records chicago_food_inspections, osha_inspection_violations, labour_inspection_compliance.

VERDICTS
1. inspection_level kept with a note (builder (a), column auditor): DEPARTS WITHOUT A STATED REASON from LEAK-10 clause 2.
2. Labels corrected after upload, newest months less corrected: the keep (a) + re-download revisit is CONSISTENT with
   LEAK-24's "compare two downloads first" (sf_permit_time), but the issue is filed under the wrong mechanism: these are
   revisions, not censoring, and the history columns are LEAK-10 clause 2 values read at a later pull. Departs only
   partly: see 2 below.
3. Within-site/state AUC (domain practitioner): would be the THIRD exception of the MET-5 "context within-group metric"
   kind (after protein_model_quality_rf_pcp and huesken_sirna_efficacy, both 2026-11-04, Lennart): an amendment is due
   if it is taken. Pooled roc_auc (fallback) is consistent with every classification precedent.
4. Enforcement flags (issue 3) keep-with-note: consistent with medical_facility_operational_data (worth within noise:
   0.0008-0.0024 vs SE 0.002), so (a) follows precedent; dropping is also fine.
5. Selective labels with no marker, 7-day gap, Oct 2026 newest window: consistent (selection.md granted-loan; SPLIT-10).

1. INSPECTION LEVEL
Facts that matter: the value is the level performed; it can be raised after the inspector sees a defect; the raised rows
cannot be located; whole-field worth 0.057-0.058 AUC against an SE of about 0.002 (ablation.json).
Precedents:
- distribution_transformers_at_cauca_department (Lennart, 2026-10-21; Mechanisms row 477): changed values not locatable,
  a gain may sit on them -> dropped, "no amendment for a gain that may sit on the changed rows".
- onlinenewspopularity (Lennart, 2026-10-26; row 488): kept with a note only because the traceable part shows no gain.
- medical_facility_operational_data (Lennart, 2026-11-05; row 489): final schedule instead of the plan, kept because the
  whole-field worth is within about two seed SDs, an upper bound on the late part. Closest in kind (final vs planned),
  opposite in size: here the upper bound is ~28 SEs.
- bank_marketing `campaign` (LEAK-10 clause 3): a value recorded after the prediction point goes; "the size of the
  worth alone never decides" (2026-11-08, X4) cuts both ways.
- Siblings: chicago_food_inspections and osha_inspection_violations keep inspection TYPE (complaint/canvass/programmed),
  which is fixed before the visit; no sibling keeps a scope that the visit can widen.
The builder's reason "the leak part cannot be located" is, under these precedents, the reason to drop, not to keep. The
fact that could set this case apart (not yet written down): most of the worth is structural by design (a driver-only
Level 3 cannot produce a vehicle OOS order: 0.7% vs 23-25%) and ISS recommends the level before the stop, so the level is
mostly the plan. No measurement shows that the raised part carries no gain; a diagnostic would be needed (e.g. AUC of the
level within carriers/units whose history predicts a planned Level 1/2, or the share of Level 1/2 inspections at sites
that only run one level). Without it, (a) breaks a Must (LEAK-10) and is not reasonable under the ranking.

2. CORRECTED LABELS
Measured (split/claim auditors): changed records 12-16% of 2025 months vs 6.2% (Sep 2026) and 3.9% (Oct 2026); changed
records are OOS at 28% vs 17%. Precedents: sf_permit_time (two downloads compared, cut), consumer_complaints (re-sourced
from settled archive), tunisian_fraud_detection_challenge (newest year cut, Lennart, 2026-11-04). In every one the
curator acted before shipping where the newest period was measurably less settled; none shipped a known gap with a
revisit only. Here the gap is measured (change share 2-4x lower in test months), so "cannot be located without a second
download" is half true: the less-settled months are located, only the rows are not. Option (c) (windows earlier, e.g.
months whose change share has levelled off) has precedent (tunisian); (a)+(b) does not yet. Also: the history columns
read corrected past outcomes, a LEAK-10 clause 2 "later pull" case; since corrections cluster on OOS rows (28% vs 17%),
a gain may sit on them (distribution_transformers again). The direction matters: if DataQs corrections mostly remove
OOS orders, test labels are biased up relative to train, which matches the pooled z +3.6 rise in probe 13 and would
mean the "no fall, no censoring" reading of probe 13 does not clear this mechanism.

3. WITHIN-GROUP AUC
Precedents: numerai_v5_2_1m (source's own per-era CORR, MET-4), blogfeedback (source's Hits@10 per day), protein and
huesken (context exceptions: the use case ranks within a group and pooled loss rewarded the group mean, measured: group
means beat LightGBM / cut RMSE 0.158 -> 0.138). Here: no source metric; the group (site, state) is a feature, not a
scoring column; no measurement yet that pooled AUC is driven by between-site base rates (would need: AUC of the
site-month OOS rate alone, and the ranking of models pooled vs mean within site-month, Kendall tau). Also the first
classification case and no `mean_group_roc_auc` in the library (MET-12/13 would need a new metric checked).
Recommendation: keep the fallback; record the concern in the notes; open it only with the measurement, and then as an
amendment to MET-5/MET-11 (third case), not a silent exception.

DRIFT: none found; the same curator (Lennart) has decided LEAK-10 clause 2 consistently (drop when a gain may sit on the
unlocatable part; keep when within noise).

REFLECTION PROMPT (decision 1)
Should inspection_level stay as a feature when the recorded level is the level performed and the raised part cannot be
located?
**Problem:**
- The level can be raised after a defect is seen; worth 0.057 AUC (SE ~0.002), the strongest feature.
- LEAK-10 clause 2 precedents drop such values when a gain may sit on the unlocatable part (distribution_transformers,
  2026-10-21) and keep them only when the whole worth is within noise (medical_facility, 2026-11-05).

| Option | Pro | Con |
|---|---|---|
| (a) keep with a note, naming as the distinguishing fact that the level is mostly planned by design (ISS recommends it before the stop; Level 3 cannot give a vehicle OOS) | keeps the task the inspector runs; most of the worth is structural | no measurement shows the raised part carries no gain; an exception to a Must |
| (b) drop the level; prediction point = selection | follows distribution_transformers; the decision ISS supports (domain practitioner) | loses the design signal; AUC 0.794 -> 0.737 |
| (c) keep only after a diagnostic shows the raised part carries no gain (onlinenewspopularity's test) | follows clause 2 as written | needs a proxy for the planned level that may not exist |

Recommendation: (b), unless (c)'s diagnostic can be run; (a) only with that fact written down as an exception.
[1]: LEAK-10 (clause 2), LEAK-1, LEAK-6; P4.

REFLECTION PROMPT (decision 2)
Should the Aug-Oct 2026 windows ship while their labels are 2-4x less corrected than training's?
**Problem:**
- Changed records 12-16% of 2025 months vs 6.2% / 3.9% of Sep / Oct 2026; changed rows OOS at 28% vs 17%.
- Every LEAK-24 precedent acted before shipping (sf_permit_time, consumer_complaints, tunisian 2026-11-04).

| Option | Pro | Con |
|---|---|---|
| (a) keep with note, re-download in ~3 months as revisit (builder) | newest data; label exists at upload (revision, not censoring) | no precedent ships a measured unsettled period |
| (b) move windows earlier to months whose change share has levelled off | follows tunisian / sf_permit_time | older test months, shorter train side |
| (c) compare a second download now-ish and decide | LEAK-24's own test | delay; view rolls off early history |

Recommendation: (b) if the change share levels off by a month the history still covers; else (a) with the revisit
written as a condition. The late-values rule question stays for the review page.
[2]: LEAK-24, LEAK-10 (clause 2), SPLIT-10.

</details>

<details><summary>Advocate</summary>

Advocate opening brief: fmcsa_roadside_inspection_out_of_service_1m (2026-11-09)
Position: ship. Two changes, both the mildest remedy for a real problem: (A) drop or coarsen vehicle_days_since_inspection (gamer), (B) a README note on corrected labels plus a re-download revisit. The inspection_level question goes to the curator, but the dataset ships either way.

1. Real task, direct target, right split. One row is one inspection decision. OOS_TOTAL>0 is the action the inspector takes (domain: "a good direct target"). The split uses monthly windows Aug-Oct 2026 with a 7-day gap, which covers the upload lag (median 2 d, p90 7; 0.06-0.16% of train rows not yet uploaded). 94.5-94.9% of test carriers were seen in train, the natural known-entity share (split auditor: RIGHT WITH NOTES). Rules: USE-1, USE-5, SPLIT-6/10/13 (ranked above the objections below, which are about features). Every auditor ships it: claim "ship with notes", column "ship as is", split "right", blind "include with changes".
2. Value. LightGBM 0.79 vs linear 0.757, vs the carrier's past share 0.58-0.59 (TP-10 holds). 0.755 without the history features, so there is headroom. 5.5M real rows from a federal source that updates over time. No TP flag.
3. Leakage was handled at the source. 8 outcome counts, end time, alcohol/drug checks and decal were dropped (LEAK-10). 2,234 copies were removed (LEAK-16). Copy groups (34k VIN-day, 15.6k carrier-day-time) all fall on one day, so none crosses the 7-day gap. The history counts only rows added before the inspection day, and same-day rows are excluded (column auditor, claim auditor). gross weight, VIN and unit_count were checked and are not outcome markers.
4. The gamer's exploit is real (+0.010/+0.023/+0.034 AUC on 6-19% of test rows), and it has a cheap fix. Chaining works only through the exact date in vehicle_days_since_inspection. Dropping that column, or bucketing it by month, breaks the chain without touching the target, rows or split (LEAK-9, mildest step of the remedy ladder). This is a change that needs no decision. Note in the README that the carrier key is weaker (no carrier id), so it is the lower-bound case.
5. Corrected labels (12-16% of 2025 months changed vs 6.2%/3.9% of Sep/Oct 2026) are a label-maturity gap, not a leak. The A-only (never-changed) Yes rate rises too, 11.5-15.1% -> 20.9%, so the trend is real drift. The kept-with-a-revisit approach matches LEAK-24's "compare two downloads first" (sf_permit_time; precedent checker: CONSISTENT). Mildest remedy: a note now, a re-download in about 3 months, and move the windows earlier only if the labels drift. Concede: file it under revisions (LEAK-10 cl.2), not censoring.
6. inspection_level: I concede the precedent case. 0.057 AUC is about 28 SE, which departs from LEAK-10 cl.2 (cauca transformers dropped it), and the domain practitioner prefers drop (b). This is a column choice, and independent failures are not conflicts: dropping it keeps the task at 0.73-0.74 AUC (0.794-0.057). So it argues for a column change, not against shipping. My recommendation is (b), drop it, unless the curator wants it as a diagnostic. Enforcement flags are worth 0.0008-0.0024, within the noise. Keeping them follows precedent (medical_facility); dropping them costs nothing either way.
7. Cleaning items need no decision (CLEAN): cargo_tank "NON" -> none, NaN = not applicable, cast unit1_model_year to float. location_desc (24k levels): only one row has OOS-like text, and county is there as a coarser place. Keep it, or drop it as the blind reviewer prefers; this does not change the verdict. Pooled roc_auc stays. A within-site metric would be a 3rd MET-5 exception and needs an amendment (precedent), so it is not taken here.

</details>

<details><summary>Critic</summary>

Critic opening brief: fmcsa_roadside_inspection_out_of_service_1m (2026-11-09)
Position: ship only changed. The task is real (one row = one inspection decision, direct target, right split), so I do not ask to exclude it. Three changes are needed before it ships (points 1-3). Points 4-6 are notes and cleaning.

1. inspection_level is the level performed, a post-outcome value worth 0.057 AUC (Must, LEAK-10 clause 2; validity).
   Problem: the file records the final level, and an inspector can raise a driver-only check to a full one after seeing a defect. The raised rows cannot be located. Effect: the strongest feature (0.652 AUC alone) teaches "a deeper inspection finds more", not "this truck is risky". At the decision the actor actually makes (ISS selection: pull in, and at which level) the level is not known yet (domain practitioner, fit only approximate).
   Evidence: ablation 0.794 -> 0.737 (about 28 SE); L3 OOS 6.6% vs L1 27.8% (claim auditor); precedent checker: keeping it DEPARTS from distribution_transformers (2026-10-21: "no amendment for a gain that may sit on the changed rows"); medical_facility was kept only because its worth was within noise. Under that precedent, "cannot be located" is a reason to drop, not to keep. The README's "judged when the inspection starts" holds only for a planned level, so the note is wrong.
   Remedy: drop the column (option b). The task stays at 0.737-0.744 AUC. Keep it only if the diagnostic of option (c) shows the raised part carries no gain.

2. Chaining exploit through the test window's history (Must, LEAK-9; validity).
   Problem: a later test row of the same vehicle carries vehicle_oos_1y, which already counts the outcome of an earlier test row. The rows are linked by exact date arithmetic on vehicle_days_since_inspection.
   Evidence: task gamer +0.010/+0.023/+0.034 AUC (noise 0.0005). It covers 6-19% of test rows, and matched rows reach P(OOS) 0.59-0.68 vs 0.05-0.07. The gamer calls this a lower bound, because the carrier_*_1y counts can be chained the same way with a better carrier key.
   Remedy: drop vehicle_days_since_inspection, or bucket it by month. Also add the LEAK-9 protocol line (a model may not use other test rows). If the carrier chain is also shown to work, freeze each window's history at the window start (a rebuild). Dropping one column is not enough to call the leak closed until the carrier chain is checked.

3. Test labels less corrected than train labels (LEAK-24 / LEAK-10 clause 2; validity).
   Problem: the view holds the last version of each record. Change transactions make up 12-16% of the 2025 months but 6.2% of Sep 2026 and 3.9% of Oct 2026, and changed rows are OOS at 29.2% vs 18.0%. So train and test labels are at different correction stages, and the history columns read corrected past outcomes.
   Evidence: claim auditor (claim 30's "cannot be located" is wrong: the transaction_code column locates it by month); precedent checker: every LEAK-24 precedent acted before shipping (sf_permit_time, consumer_complaints, tunisian 2026-11-04), and none shipped a measured unsettled period with a revisit only.
   Remedy: move the windows earlier, to months whose change share has levelled off (tunisian precedent). If no such month exists inside the history the view covers, keep with a note that gives the change share per month, and make the re-download in about 3 months a written revisit condition. Either way, correct claim 30 in the README.

4. Pooled ROC AUC rewards between-site base rates (Should, MET-8 / MET-5; value).
   Domain practitioner: the decision ranks trucks within a site-day queue, and enforcement culture varies by state and site. This is not measured, and a within-group metric would be a third MET-5 exception (precedent checker). Remedy: keep roc_auc and add a note. Before any metric change, run the measurement (AUC of the site-month OOS rate alone).

5. Enforcement flags have undocumented timing (LEAK-10; low weight).
   They are worth 0.0008-0.0024, about one SE. A size/weight action can follow the scale reading (domain). Remedy: drop them. It costs nothing and removes a question. Keeping them with a note also matches precedent (medical_facility).

6. Cleaning (quality, not a reason to hold the dataset back; CLEAN-10/12).
   Map cargo_tank "NON" (8,677 rows) to none. Read NaN in hazmat and cargo_tank as "not applicable". Cast unit1_model_year to float. location_desc (24k levels of free text): drop it or keep it with county; this is the curator's call.

7. Reproducibility: the raw files cannot be downloaded again (procedure).
   The view drops a day every day, and the bulk export sunsets on 2026-12-22. Remedy: archive the ~4.5 GB of CSVs before the merge. This is a procedure item, not a reason to keep the dataset out.

</details>
