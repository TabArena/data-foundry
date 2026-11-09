# fpa_fod_wildfire_cause

**Outcome:** added as `fpa_fod_wildfire_cause_1m`. The general cause of a US wildfire (11 named causes of the NWCG
standard) from what the first fire report holds: date and hour, point of origin, state, county, land owner and the
reporting agency, unit and system. Built from the 7th edition of the FPA FOD (Short 2026, 1992-2024): 1,879,544 fires
with a named cause; test windows 2022, 2023 and 2024, each trained on a random million of all earlier fires; fallback
log loss. The AI recommends shipping it. The panel's changes are made, all to the text: the population sentence now gives the share left out (25-35% of labelled test fires coded "Other causes"; undetermined fires 15.0% in 2021 to 28.8% in 2023); per-column notes on missingness that differs by cause; the undetermined shares by year and quarter in the censoring note; the missing lightning and weather inputs in the fit reason; the recent-history scores in the split comment; and the record name (7th edition, 1992-2024).
Verdict: ship after changes (made); issues 1-3 stay at option (a) unless you choose otherwise.
Validity: SEL-1 holds. USE-1 holds, fit approximate: labels only from determined fires, no lightning or weather
inputs in the source, a reporting break in 2020-2021. LEAK-10 triggered and fixed (containment, final size, the fire's
name, the large-fire ids and the two other encodings of the cause dropped). LEAK-13 with the LEAK-25 amendment of
2026-11-02 triggered and fixed: "Other causes" left out. LEAK-24 checked, no censoring signature. SPLIT-14 holds;
SPLIT-20: the training history spans the reporting break (issue 1).
Value: TP no flags; linear log loss 1.449 against 1.884 for the class shares (23.1% better), 3 of 3 windows.
Quality: missingness that differs by cause (hour, county, owner) documented per column, no data change.
Weighed: size +, gap +, source +, use case 0, risk − (about half of each test year's fires have a named cause; the reporting break).

**Main points:** Where the training history starts (issue 1, a weighing call the panel split on); confirm leaving out "Other causes"
(2), keeping the reporting fields (3) and the map-service download (4).

**Issues for Lennart:**

1. **Start the training history in 1992, or later?**

   * **Problem:**
     - 92-97% of each training side comes from the federal and state reporting systems before 2021, while the test years are 99.9% from one interagency system (InFORM).
     - Recent years alone train a better model (see Experiments).
     - Before 2021 the land owner is missing for 37-64% of each year's fires and about 0% after; the hour 30-60% in the 1990s and 4-16% since 2020.
   * **Effect on the task:** a model that weights recent years gains 0.01-0.08; the date is a feature and the recent years are on the train side, so a participant can do that.
   * **Experiments:** split auditor (300k sampled training fires, untuned LightGBM): full history 1.363 / 1.461 / 1.353, since 2016 1.302 / 1.378 / 1.339, since 2020 1.340 / 1.446 / 1.437; task gamer (regularized LightGBM): the last 10 years only, 1.407 against 1.461 on average, better on 3 of 3 windows. A history from 2020 only leaves the 2022 window 88,503 of its 229,751 fires (38.5%).
   * **Consistency:** two cases cut the history at a break: aeolus (from 2023) and chicago_traffic_crashes (from citywide coverage, which removed an incomplete population, not an old recording system). Three cases kept the history with a note: chile_school_dropout_mineduc, noaa_afsc_bottom_trawl_survey_cpue and chicago's 2023Q4 step. Option a follows the kept cases, because after the break too little history is left. The history is decided on the reason, not the score[^s21].
   * **Panel:** the panel split and the mediator left it to you as a weighing call. The advocate keeps a (the break is noted, the date is a feature, a history from 2020 fails the training floor). The critic asks for d, a later start. The blind reviewer, independently, proposes starting in 2005 or later. The split auditor finds no fault in the split: recent-only training is better by 0.01-0.08, but the train side holds those years. The task gamer calls training on the last 10 years an honest choice (+0.055). No Must fails either way, and the choice rests on the reason, not on the scores.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | From 1992, with the note (implemented) | train sides are a random million of all earlier fires; `splits_comment` gives the numbers above | the long history the source offers; meets the training floor | 92-97% of training from systems the test years no longer use |
     | b | Cut the release at 2020 | test on 2018-2020, before InFORM | one recording regime | not the system agencies report in today; drops the newest four years |
     | c | From 2020 only | train on the interagency years | the test years' system | the 2022 window trains on 38.5% of its rows, under the floor[^s14] |
     | d | A later start (2005, 2010 or 2015) | train sides from that year on | closer to today's recording (owner and hour recorded more often); meets the floor (to be checked per start year) | gives up the oldest decades; the break in 2020-2021 stays inside any such history |

   * **Recommendation:** a, unless you hold one recording regime above long history: the rule leaves both open[^s20], and the choice rests on that reason, not on the scores above[^s21]. **Decision:** a, b, c or d?

   **Notes for the AI:** on d, filter `discovery_date` to the start year in `_clean` (after the cause filters), update `row`, `split`, `version_comment` and `splits_comment` (pool sizes per window, the share of each window's training floor), re-run `dataset check` and the task and leak probes; on b, change the test windows to 2018-2020 and drop 2021-2024.

   [^s20]: **SPLIT-20** (Should): decide what the train side holds from the use case: the history a model refit at each window would train on; check the history for breaks (a change of the data collection) and say why.
   [^s14]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less than 50% of the data.
   [^s21]: **SPLIT-21** (Must): decide neither the training history nor the windows from a comparison over a few test windows (aeolus, Lennart, 2026-10-12).

2. **Leave out the fires coded "Other causes"?**

   * **Problem:**
     - "Other causes", the standard's residual, holds under 1% of each year's fires until 2020 and 18-28% from 2021, mostly in a few states (Colorado, Michigan, Indiana, Kansas).
     - Kept as a class, it would be 34.6%, 27.6% and 25.3% of the labelled fires of 2022-2024, against 0.6% of the training years before 2021.
   * **Effect on the task:** kept, a model would score on a state's reporting habit; left out, the test years lose a quarter to a third of their labelled fires, which the population sentence of `task_summary` now says.
   * **Experiments:** builder: the state and date alone rank "Other causes" with ROC AUC 0.77-0.80, against 0.78-0.82 on every input; claim auditor: the share is 34.6/27.6/25.3% of the labelled fires of 2022-2024.
   * **Consistency:** follows noaa_storm_events_damage, where a recording convention that follows a reporting unit may be kept only when the task keeps a signal beyond unit, period and place; that condition fails here[^l25].
   * **Panel:** every agent agrees on leaving it out; only the rule cited was disputed (now cited as below)[^l13].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Leave it out in every year (implemented) | 11 named causes | no class that is a state's reporting habit | the score covers fewer of the recent fires |
     | b | Keep it as a 12th class | 12 classes | every labelled fire stays | 15-22% of the log loss would come from reading the state and year |

   * **Recommendation:** a. **Decision:** a or b?

   **Notes for the AI:** on b, remove `OTHER` from the filter in `_clean`, update `row`, `changes`, the curation note and the decision titles, re-run `dataset check` and the leak and task probes.

   [^l13]: **LEAK-13** (Must): class-specific recording conventions are harmonised; first measure how much the fix removes.
   [^l25]: **LEAK-25** (Must, amended 2026-11-02, Andrej, on noaa_storm_events_damage): a mix whose recording follows a reporting unit shipped as a feature may be kept, case by case, when the task keeps a measured signal beyond the reporting unit, the period and the place.

3. **Keep the reporting fields (system type, system, agency, units)?**

   * **Problem:**
     - The fields are on the report when it is filed, but older systems code different sets of causes (Georgia, Mississippi and South Carolina never code power lines, fireworks or firearms).
     - The test years are one system, and an untuned LightGBM scores better without the fields in 3 of 3 years (log loss lower by 0.029-0.125).
   * **Effect on the task:** if the fields were a proxy of a system's labelling habit, models would be ranked on conventions absent from the test years; the linear fit says they are not.
   * **Experiments:** the mediator's logistic regression (one-hot categories, 200k training fires), window 2022 only: all fields 1.4151, without the two system fields 1.4491, without all five 1.4501; dropping them costs the linear model 0.034, so the untuned LightGBM's gain is its instability (the task gamer saw 1.6-6.4 from such a model). Only the 2022 window finished within the 25-minute limit; 2023 and 2024 were not run. Running them would show whether the 0.034 loss holds on all three windows rather than on one.
   * **Consistency:** noaa_storm_events_damage kept the reporting office as an input. Columns were dropped only when they marked a single class (hepatitis_c_prediction, gallstone_disease), which these fields do not. Not deciding from the untuned LightGBM gain follows the rule on few-window comparisons[^s21b].
   * **Panel:** the critic asked for the linear run before deciding; the advocate, the column auditor and the domain practitioner keep the fields (who reports is known at discovery); the mediator recommends a on the strength of the run above (one window).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep all five (implemented) | the report's filer as inputs | known at discovery[^u6]; the linear model needs them | carry the older systems' habits in training |
     | b | Drop the two system fields | `source_system_type`, `source_system` out | they are one value in every test year | the linear model loses 0.034 |
     | c | Drop all five | agency and units out too | no filer's habit at all | the linear model loses 0.035; the unit is the strongest single input |

   * **Recommendation:** a: the fields are known when the report is filed[^u6], and the one linear fit (2022) points the same way; ask for the 2023 and 2024 runs if one window is not enough. **Decision:** a, b or c?

   **Notes for the AI:** on b or c, add the columns to a drop list in `_clean` and to `_feature_types`, update `known` and the curation note, re-run `dataset check` and the task probes. The mediator's script is `lin.py` in the run's scratch.

   [^u6]: **USE-6** (Must): anything known at the prediction point is a legitimate input.
   [^s21b]: **SPLIT-21** (Must): decide neither the training history nor the windows from a comparison over a few test windows.

4. **Keep reading the data from the Forest Service's map service?**

   * **Problem:**
     - The Research Data Archive behind the DOI answered HTTP 403 to this machine on 2026-11-08 and 2026-11-09.
     - The definition pages the same table from the USFS map service that serves the current edition and asserts its 2,661,383 records.
   * **Effect on the task:** none now; once the service moves to an 8th edition, the count check fails and the download must change.
   * **Consistency:** asserting the record count and noting when to revisit follows earlier practice; no contrary precedent[^p9].
   * **Panel:** no dispute.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep the map service (implemented) | 1,331 pages by OBJECTID, record count asserted | works today; the publisher's own service | serves only the current edition; no file checksum from the archive |
     | b | Switch to the archive's sqlite file | once it answers, compare and read that | the DOI's own file | not reachable now |

   * **Recommendation:** a; revisit when the archive answers or the service moves to an 8th edition. **Decision:** a or b?

   [^p9]: **PROV-9** (Must): the year is the year of the first publication; a source that grows over time takes the year of the snapshot we pin.

**Review panel:** ship after changes (mediator). Ten agents; the rebuttal round was skipped under the budget rule, since
the advocate's and the critic's briefs converged on everything but the reporting fields, which the mediator settled
with a linear fit on the 2022 window (all fields 1.4151, without the five reporting fields 1.4501; 2023 and 2024 not
run). Claims: none refuted, two wordings refined (LEAK-24 note, hour missingness), now applied. Blind review: include
with changes; its main concern, missingness that shifts with the reporting systems, feeds issue 1. Task gamer: barely
gameable, the best exploit (counts over all rows) gains 0.016-0.021, now a note. Precedent: consistent on all four
issues; it asked for the later-start option (now d in issue 1) and the corrected rule citation (issue 2), both made. Agreed: the drops, the split, the metric, leaving out "Other causes". Disputed: the start of the training
history (issue 1), the reporting fields (issue 3, settled by the fit).

<details><summary>Mediator: fpa_fod_wildfire_cause</summary>

```text
Mediator report: fpa_fod_wildfire_cause (folder fpa_fod_wildfire_cause_1m), 2026-11-09
No rebuttal round (budget rule); the briefs converge on everything except critic point 4, settled below by experiment.

JUDGMENT RECORD
Verdict: ship after changes (documentation now; issues 1-3 stay at option (a) unless the curator chooses otherwise).
Validity: SEL-1 holds; USE-1 holds, fit approximate (labels only from determined fires, reporting break, no
lightning/weather inputs); LEAK-10 triggered, fixed; LEAK-13 (with the 2026-11-02 LEAK-25 noaa amendment) triggered,
fixed ("Other causes" dropped); LEAK-24 checked, no censoring signature; SPLIT-14 holds; SPLIT-20 history spans the
2020-21 break (noted; later-start option to be offered).
Value: TP no flags; linear 1.449 vs dummy 1.884 (23.1% skill), 3/3 windows.
Quality: missing-by-class patterns (hour, fips_code, owner) documented, no data change.
Weighed: size +, gap +, source +, use case 0, risk - (population cut, reporting break).
For the curator: issue 2 (start year, a weighing call); issue 3 settled by experiment toward (a); issues 1 and 4 (a).

DECISIVE EXPERIMENT (critic 4 / issue 3)
Logistic regression (one-hot cats min_freq 20, scaled numerics + day of year, year, hour-missing flag), 200k-row train
sample, participant kit, OMP_NUM_THREADS=4. Window 2022 (the only one finished in the 25-min cap):
  all fields 1.4151 | without source_system(_type) 1.4491 | without all five reporting fields 1.4501.
Dropping the reporting fields costs the linear model 0.034; the untuned-LightGBM gain (0.029-0.125) is that model's
instability (gamer: untuned LightGBM gave 1.6-6.4), not a proxy leak. Script:
(local path)
Fields are known at report time (USE-6, "who I am"); LEAK-13 not failed. Keep (a). 2023/2024 not run; running them
would confirm.

CHANGES NOW (no decision needed)
1. Population sentence in task_summary/changes: test windows lose 25-35% of labelled fires to "Other causes"
   (34.6/27.6/25.3%, 2022-24); undetermined fires 15.0% (2021) -> 28.8% (2023) are not labelled (USE-3, USE-8;
   precedent noaa_storm_events_damage).
2. Issue 1 and its note: cite LEAK-13 plus the LEAK-25 noaa amendment and why its keep-condition fails (state+date
   AUC 0.77-0.80 vs 0.78-0.82 on all inputs) (LEAK-13, Must).
3. Issue 2: add option (d) a later start (2005/2010/2015, meets SPLIT-14) with numbers; put the split auditor's and
   gamer's numbers in splits_comment (since-2016: 1.302/1.378/1.339 vs 1.363/1.461/1.353; last-10-years +0.055)
   (SPLIT-20, SPLIT-21).
4. LEAK-24 note: add undetermined-alone shares per year and the quarterly 2024 check (Q4 < Q3, no fall-off) (LEAK-24).
5. Per-column notes: discovery_hour missing 2.8% (Natural) to 21.5% (Smoking), no gain from the flag; fips_code
   missing 13-90% by cause in federal records, 0-7% in test years; owner_descr/hour missingness falls with the
   system change (LEAK-13/LEAK-39, quality).
6. fit_reason: name the absent lightning/weather inputs and the dropped undetermined pool (USE-8).
7. Issue 3 text: add the linear result above (EV-6, SPLIT-21).
8. Record name: 7th edition, 1992-2024 (step 8).

ISSUES FOR THE CURATOR (ranked)
1. Start of the training history (SPLIT-20 Should vs SPLIT-14 Must; validity, weighing). Problem: 92-97% of training
   comes from pre-InFORM systems; tests are 99.9% InFORM. Effect: an honest recent-only model gains 0.01-0.08.
   Advocate: the date is a feature and the recent years are on the train side, so it is a modelling choice; 2020-only
   fails SPLIT-14. Critic: offer a later start; blind reviewer independently proposes 2005+ (owner missing 37-64%
   before 2021). Rules leave it open (Should, no Must fails either way). Decide: (a) from 1992 with the note, or
   (d) a later start. Settles it: SPLIT-21, choose on the reason (one recording regime vs long history), not the score.
2. "Other causes" (LEAK-13 Must): both sides and all agents agree on (a) drop; only the citation was disputed (fixed
   in changes 2). Confirm (a).
3. Reporting fields (LEAK-13, USE-6): settled toward (a) by the experiment; confirm, or ask for 2023/2024 runs.
4. Reproducibility of the download (procedure): (a) keep the map-service source with the asserted row count; revisit
   when the RDS archive answers. No dispute.
Cross-dataset calls kept open as asked: none of the four reserved topics (protected grounds, codes vs words, scoring
within groups, late-filled values) arises here beyond the codes-as-categories note.

TASK GAMER EXPLOITS
- n_loc_all (location count over all rows, +0.016-0.021): LEAK-16/LEAK-20 (statistics using test/future rows);
  participant-side, not a task flaw; new (no definition note). Below 0.021, near noise: a sentence in the notes, no fix.
- n_unit_day (same-day count, +0.002-0.013): LEAK-10 time-of-prediction; new, near noise; none.
- rank_in_day (+0.003-0.008): LEAK-19 row order; within noise; none.
- Recent-only training (+0.055): not an exploit; feeds issue 1 (SPLIT-20).
No "Potential leak, kept on purpose" note's measured gain is contradicted.

AGREED FACTS
- 1,879,544 fires 1992-2024 with a named cause; 1M temporal version, test years 2022/2023/2024; 11 classes.
- dataset check 0/0; no refuted claim; 12 features known at discovery; 0 copies across split; train max < test start.
- Linear 1.449 vs dummy 1.884, better 3/3; smallest test class 279 rows.
- "Other causes" 0.6% before 2021, 18-28% after, state+date AUC 0.77-0.80.
- Test years 99.9% InFORM; recent-only training helps 0.01-0.08; 2020-only start leaves 38.5% (< SPLIT-14 floor).
- Log loss fits (MET-1, MET-5..8); no agent disputes.
- Record name stale (6th edition).

CONSISTENCY
Precedent checker: all four issues consistent. Drop of "Other" follows noaa_storm_events_damage (LEAK-25 amendment,
its condition fails here); population sentence follows the same case; 654 large-fire-only drop consistent with
LEAK-10 practice. No departure from precedent.
```

</details>

<details><summary>Claim audit: fpa_fod_wildfire_cause</summary>

```text
Claim auditor: fpa_fod_wildfire_cause_1m (2026-11-09)
Verdict: no claim refuted on validity; two small wording refinements; issues 1-4 of the builder stand as drafted.
Scratch: the run folder (t1.py/t1.out raw-parquet checks, t2.py/t2.out in-memory container + scorer, t3.py/t3.out censoring and hour missingness). No container written to disk.

claim | source | test | result | evidence | rule
1,879,544 kept fires, 11 classes | claims 16, task_summary.row | replicate _clean on prepared parquet | holds | 1,879,544 | -
Windows 2024/2023/2022 = 46,707/44,931/49,610; pools 1,832,837/1,787,906/1,738,296 | claims 17, version_comment | count by year on kept rows | holds | identical | SPLIT-14
Splits temporal, no train date >= test start, train 1M | splits_comment, claims 28 | to_container in memory, read splits | holds | train max 2023-12-31/2022-12-30/2021-12-31 < test start; 1,000,000 each; frame 1,141,248 | SPLIT-1
Copies never cross the split | claims 18, curation notes | exact match of all 12 feature columns test vs train | holds | 0 / 0 / 0 | LEAK-16..20
Metric computable, every class in every test fold | claims 31, MET-2 | scorer on train-prior dummy per fold | holds | log loss 1.938 / 1.886 / 1.827 (matches builder's prior 1.937/1.886/1.826); 11/11 classes per fold; smallest class 279/400/385 | MET-2
Metric fallback justified | metric reason | searched once more: Pourmohamad 2025 abstract (DOAJ) | holds | overall >70%, natural/human 93%, 11 human classes 55%: several accuracies, no single deliberate one | MET-1, MET-5, MET-6
Discovery dates are dates (ms at 00:00 UTC) | _prepare_raw_files comment | non-midnight count; fire_year == date.year | holds | 0 non-midnight; 100% agree | -
No containment before discovery / no gap needed | claims 29 | cont_date < discovery_date | holds | 0 rows | SPLIT-10
Test years 99.9% InFORM | claims 30, fit_reason | source_system in kept test rows | holds | IA-INFORM 141,197 of 141,248 (ST-CACDF 51) | SPLIT-20
Other share of labelled test fires 25-35% | claims 14 | Other / (labelled incl. Other) per year | holds | 34.6% / 27.6% / 25.3% (2022/23/24) | LEAK-25
"No rise at the end" (LEAK-24) | curation notes, claims 11 | undetermined share by year and by quarter of 2022-2024 | holds, wording refined | combined undet+Other 49.1/48.4/46.7% as claimed, but undetermined alone rises 15.0% (2021) -> 22.2 -> 28.8 -> 28.7% (Other moving into undetermined as Kansas etc. stop using Other); no within-year fall-off: 2024 Q1-Q4 23.5/30.8/31.4/28.3% (Q4 below Q3), so no censoring signature | LEAK-24
Owner / FIPS missingness not class-dependent | claims 23, 25 | missing share by class in test years | holds | owner missing <=0.1%, fips 0% for every class | LEAK-13
Point precision follows system, not class | claims 24 | lat decimal count by class, test years | holds (weak) | 8-decimal share 28% (Firearms) to 51% (Debris); Firearms is the Idaho range; no class near-pure | LEAK-14
Hour missingness no shortcut | claims 22, 36 | missing share by class in test years; AUC human-vs-natural | holds as stated, refinement | missing 2.8% (Natural) to 21.5% (Smoking), 0% Firearms; AUC raw 0.545, within state 0.592: a weak class signal beyond the state, consistent with the builder's no-gain experiment (flag-only no better than no hour) | LEAK-13, LEAK-39
Features known at discovery | implied, claims 9, 27 | read of columns; post-discovery fields absent from feature_columns | holds | 12 features, none of the AFTER_DISCOVERY / encodings | LEAK-10, USE-3

Untested (why): reporting fields dropped with the linear family (issue 3; builder ran only untuned LightGBM) - left for the split/gamer roles, cost of a one-hot linear fit on 1M x high-cardinality not spent; whether the 7th edition recoded causes of earlier years (no 6th edition obtained, RDS 403); hash pin of the map-service pages (issue 4).

Ranked findings (none Must-level refuted)
1. (Should, LEAK-24 wording) The "no rise at the end" note cites only the combined undetermined+Other share; the undetermined share alone nearly doubled 2021->2023. Within-year it shows no censoring, so the conclusion stands. Mildest remedy: add the undetermined-alone shares and the quarterly check to the LEAK-24 note.
2. (Could, LEAK-13) Hour missingness differs by class (2.8% Natural to 21.5% Smoking; within-state AUC 0.59). The builder's experiment shows no gain from the flag; keep, and cite the per-class shares in the discovery_hour note.
3. Record `name` still says 6th edition 1992-2020 (builder already lists it). Remedy: fix the name at step 8.
Builder's issues 1-4 weighed: 1 (Other left out) confirmed by numbers (25-35% of test labels); 2 and 3 are curator calls, no counter-evidence found; 4 reproducibility unchanged.

Source looked up: https://doaj.org/article/31cc6c0340ca4e119108891a69f6d170
```

</details>

<details><summary>Column audit: fpa_fod_wildfire_cause</summary>

```text
Column auditor, fpa_fod_wildfire_cause_1m (2026-11-09)
Verdict: ship; no new leak; one question on fips_code missingness; builder's issues 1-3 endorsed as recommended.

Prediction point: discovery of the fire (first curation bullet). Raw: 39 attributes (FGDC layer metadata, Short 2026).

Column | meaning | known at prediction? | dtype and cleaning | verdict | rule
nwcg_general_cause (target) | general cause, NWCG 2020 standard | outcome | 11 classes after dropping Undetermined + Other | fine | LEAK-25, USE-5
discovery_date | date discovered | yes | datetime, temporal key | fine |
discovery_hour | local HHMM -> hour.fraction | yes | float, 31% missing by system; missing flag alone ROC 0.513 | fine | CLEAN-14, LEAK-14
latitude, longitude | point of origin NAD83 | yes | float; range includes PR/Guam/AK (13.2..70.3, -178.8..144.9), plausible | fine | 
state | state | yes | categorical, 55 | fine |
fips_code | 5-digit county FIPS | yes (report) | categorical, string with leading zeros kept (all len 5); 25% missing | question | LEAK-14
owner_descr | land owner at origin | yes | categorical; MISSING/NOT SPECIFIED -> NaN, Private->PRIVATE; keeps UNDEFINED FEDERAL, STATE OR PRIVATE (real coarse codes, not unknowns) | fine | CLEAN-10
source_system_type | FED/NONFED/INTERAGCY | yes | categorical | fine (issue 3) | USE-6, LEAK-13
source_system | reporting system (43) | yes | categorical | fine (issue 3) | USE-6
nwcg_reporting_agency | agency (11) | yes | categorical | fine |
nwcg_reporting_unit_id | NWCG unit (2,339) | yes | categorical; strongest single feature 0.752, a place/agency code | fine | SPLIT-13
source_reporting_unit | source system's unit code (6,795) | yes | categorical; dtype probe ordinal_like/open_end answered: a code, not ordinal | fine (20 codes collide across systems, disambiguated by state+unit) | CLEAN-14
Dropped, correctly: nwcg_cause_classification, nwcg_cause_age_category (target encodings, LEAK-10); cont_date/doy/time, fire_size(_class), fire_name, fire_code, complex_name, ics209 ids, mtbs id/name (post-discovery, LEAK-10); objectid, fod_id, fpa_id, local_fire_report_id, local_incident_id, globalid (ids, CLEAN-3); fire_year, discovery_doy, unit names, county, fips_name (copies, CLEAN-5). fips_name/county null exactly where fips_code null (0 exceptions).

Dtype probe: 2 flags (source_reporting_unit, fips_code), both codes, categorical by meaning: correct.

Problems ranked:
1. (Question, P4 LEAK-14, weak) fips_code missingness differs by cause within federal records: 13% (firearms) to 90% (minor), 79% arson/debris vs 48-52% natural/power/recreation. Likely the agency (BIA/FS/BLM) and region, not the outcome, but if the county is filled during the investigation it is outcome-caused. Interagency era (test years) missingness 0-7%, so test impact small. Builder's missing-indicator probe (max 0.513, discovery_hour) suggests fips missingness alone is weak. Mildest remedy: none; check missing-flag-of-fips AUC within FED conditional on agency, or note it.
2. Builder issue 3 (reporting fields): known at discovery, keep (a); source_system_type/source_system are near-constant in test years so their only effect is on training; agree with (a).
3. Builder issues 1, 2: agree with (a) each. No cleaning problem found.
```

</details>

<details><summary>Split audit: fpa_fod_wildfire_cause</summary>

```text
Split auditor: fpa_fod_wildfire_cause_1m (2026-11-09)

Verdict: right with notes.

Regime. The use case scores fires as they are reported, in units, counties and agencies the model has seen: a stream over
time with known entities. Declared: temporal on discovery_date, yearly windows 2024/2023/2022, expanding history from
1992, train side a random 1M of earlier fires (one order for all windows). Matches (SPLIT-1, SPLIT-13).

Measured on the built container (1,141,248 rows; script work_split_auditor/alt.py):
- Windows: 2024 n=46,707 (train max date 2023-12-31), 2023 n=44,931 (train max 2022-12-30), 2022 n=49,610
  (train max 2021-12-31). No overlap; the train side ends where the test window starts. Test windows are full calendar
  years, so no single-season window.
- Gap and late labels: the cause is set in the closed report; the builder counts 10-15 training fires per window
  contained after the window starts (0.001%). The date each cause was determined is not recorded, so a cause decided
  months later (arson investigations) can't be measured. The undetermined+Other share is 49.1/48.4/46.7% for
  2022-2024, so there is no rise at the release end that would mark open cases (LEAK-24). No gap needed. Note only.
- Hidden groups: temporal, no hits. Units, counties and FIPS recur (test rows seen in train 96-100%): known entities,
  which is right for this use. Exact copies across the split 0.0% (copies share a date). Near-copy clusters at 0.85
  (coarse 11-column profiles of place and season) put 47% of test rows in a cluster with training rows: neighbours, not
  copies, and consistent with the temporal regime. No grouped split is called for.

Findings, ranked:
1. P4, SPLIT-20 (Should), with SPLIT-14 (Must), builder issue 2: the training history spans the 2020-2021 reporting
   break. I tested this with an alternative training window (untuned LightGBM, 300 trees; test log loss per year
   2024/2023/2022):
     all history (shipped, 300k sampled): 1.363 / 1.461 / 1.353
     history since 2016 (168-211k):       1.302 / 1.378 / 1.339
     history since 2020 (51-99k):         1.340 / 1.446 / 1.437
   Recent history helps, by 0.01-0.08. But the shipped train side contains those recent years, and the date is a
   feature, so a learner can weight them, and the effect is a matter of modelling, not a broken split. Cutting the
   history to 2020 fails SPLIT-14 (38.5% on the oldest window) and scores worse in 2022. Mildest remedy: none to the
   split. Keep option (a) and state in splits_comment that recent-only training scores better (the numbers above).
   Caveat: the frame keeps only the sampled 1M, so the recent-only subsets are smaller than the full recent years.
2. P4, LEAK-13 / SPLIT (builder issue 3, as it bears on the split): the test windows are all one system (InFORM
   99.9%), while 92-97% of training comes from older systems. This shift is real in the application too: a model
   refit in 2024 would face the same mix. So it is consistent with the use case, not an artefact of the split. I agree
   with the builder's (a).
3. P4 (builder issue 1, Other causes): the exclusion applies in every year, train and test alike, so it causes no
   train/test asymmetry. Fine for the split.
4. Note: the random 1M train sample instead of the latest 1M. The version_comment justifies it, and it is defensible.
   The latest-1M alternative (about 1999 onwards) would sit closer to the test system. That is not required and is a
   matter of taste: given finding 1, a curator might prefer it, but it is optional.

No change to the split is required.
```

</details>

<details><summary>Domain practitioner: fpa_fod_wildfire_cause</summary>

```text
Domain practitioner report: fpa_fod_wildfire_cause (folder fpa_fod_wildfire_cause_1m), 2026-11-09

Actor played: an agency fire-prevention / fire-investigation coordinator (and, second, the prevention planner who
attributes causes to fires never determined), as in task_summary.use_case.

FIT: approximate (agree with the definition, USE-8). One sentence: the inputs are the first report's and the test
years follow training, but the labels come only from fires whose cause was determined, while the decisions served
(send an investigator; attribute undetermined fires) act mostly on fires whose cause is or stays unknown, and the
test era is one new reporting system.

1. Inputs at the moment (USE-3, USE-6)
- Have and shipped: discovery date and hour, point of origin, state, county, land owner, reporting agency/unit/system.
  All are on the initial report; keeping the reporting fields is right under USE-6 (my unit is who I am).
- Would have but missing (largest first): (a) lightning-detection strikes near the origin in the prior days (NLDN;
  the single strongest natural/human cue every agency checks); (b) weather and fire danger (dry lightning, wind,
  red-flag day, ERC); (c) the initial size and the dispatch narrative ("along railroad", "near powerline", "campfire
  reported"); (d) distance to roads, rail, power lines, campgrounds, which lat/lon only implies. None of these is in
  the FPA FOD, so their absence is a property of the source, not a curation error; it makes the model weaker than the
  one I would build, not invalid. Not a reason to change the dataset; worth naming in the fit_reason or notes.
- Would NOT have: nothing left in the features after the drops (containment, final size, fire name, ICS-209/MTBS ids,
  cause encodings all correctly removed, LEAK-10). The 654 ICS-209/MTBS-only records dropped: agree.

2. Target (USE-5)
- The general cause on the closed report is what I act on for attribution and prevention planning (prevention
  campaigns target debris burning, equipment, arson, railroads by class). For the investigator-dispatch decision I act
  on a coarser question (human vs natural, and "arson/power line/equipment" i.e. liability or criminal), which the
  11-class probabilities contain. A probability over classes is what I want: for attribution I sum probabilities over
  undetermined fires to get expected cause counts per unit. Class, not number: correct.
- Proxy aspects: the label is the investigator's/reporter's determination, mapped by Short from older code lists
  to the 2020 NWCG standard; older systems never code some classes (GA, MS, SC: no power line, fireworks, firearms).
  That is a known label-noise gap, named in the notes.

3. Row vs decision, test data
- One row = one fire report = one decision: matches.
- Test = the next calendar year, all fires of the year: matches a model refit after each season. But test years are
  99.9% InFORM while 92-97% of training is the older systems (SPLIT-20 issue 2); in practice I would face InFORM
  records too, so the test is the realistic one and the history is the gap. Agree with option (a).
- "Other causes" dropped (issue 1): as a practitioner in Colorado or Michigan I would meet those fires, but the class
  is a recording convention there, not a cause I act on; agree with (a). Undetermined dropped: correct, they are
  the scoring pool, not a class.

4. Would I use it?
- For attributing undetermined fires in prevention planning: yes, as a prior, if calibrated per region; Pourmohamad
  et al. 2025 do this with richer covariates (weather, lightning, infrastructure). Trust would come from calibration
  per state and per reporting system, and from checking that the model does not just learn the reporting unit
  (single feature nwcg_reporting_unit_id 1.481 vs linear 1.449: most of the signal is "who reports", issue 3).
- For investigator dispatch: no, not alone; without lightning and dispatch notes it is too weak (skill ~23% over the
  prior). Distrust: selection of determined fires; investigated fires (arson, equipment) are more often determined,
  so determined-only labels overstate those classes relative to the undetermined pool.
- Issue 3: keep the reporting fields (USE-6), agree with (a).

5. Metric (MET-1, MET-6 to MET-9)
- Declared: fallback multiclass log loss. Scores my decision: YES (largely). Attribution sums class probabilities,
  so a strictly proper rule on the full distribution is exactly what I would select by (MET-8). The papers' accuracies
  have no threshold or costs, so declining them is right (MET-6); no cost matrix exists (MET-7); no top-k is fixed by
  the source (MET-9 does not apply). For the dispatch use alone I would add ROC AUC of human-vs-natural or of arson
  as a secondary view, but not as the declared metric. Keep log_loss.

Gaps ranked by how much they change the task
1. Labels from determined fires only, used for undetermined fires (selection, USE-8 approximate). Large; unfixable in
   the source; named in fit_reason.
2. Reporting break 2020-2021 (history vs InFORM test era), plus older systems' missing classes. Medium; named.
3. Missing inputs every practitioner has (lightning strikes, weather, initial size, dispatch text). Medium for model
   strength, not for validity.
4. Signal dominated by reporting unit identity. Small for validity (USE-6), worth the note it has.

What an expert would change (none blocks shipping)
- Name the missing lightning/weather covariates in the notes as a known gap of the source.
- Fix the record's stale `name` (6th edition, 1992-2020) per the builder's report.
- Optionally state in the use case that the human/natural split is the dispatch question and the 11-class
  probabilities serve attribution.

Verdict: ship; fit approximate confirmed; metric yes (log_loss); agree with the builder on issues 1-3 (option a).

Sources: dataset.py and README.md of the folder; builder_report.md; use_case.md (USE-3, 5, 6, 8); metrics.md (MET-1,
6-9); Short 2014 ESSD 6:1-27 and the 7th edition RDS-2013-0009.7 (as cited in the definition); Pourmohamad et al.
2025, Earth's Future doi:10.1029/2024EF005187 (as cited); domain knowledge of NWCG cause determination practice
(NWCG Wildfire Origin and Cause Determination Handbook, PMS 412) and NLDN use in cause attribution. No web lookups
were run this pass.
```

</details>

<details><summary>Blind review: fpa_fod_wildfire_cause</summary>

```text
Blind review: FPA FOD wildfire cause (target nwcg_general_cause, 11 classes, 1.14M rows, temporal split)

Verdict: include with changes. Real, well-documented USFS dataset (Short, RDS-2013-0009.6/.7), real use (assign likely cause to fires whose cause is undetermined, prioritise investigation/prevention); signal is clear but not trivial.

Task: at/after discovery, predict general cause from location, date, hour, reporting agency/unit, land owner. Leaky post-fire fields (fire size, containment date, cause text) are absent - good.

Evidence (200k sample): LightGBM, train <2020, test 2020-2024: accuracy 0.517 vs majority 0.400. Top features: day-of-year, fips, hour, year, lat/lon, reporting unit. No column missing in target; 174 exact duplicate rows (0.09%).

Concerns, most to least serious:
1. Missingness regime shift over time. owner_descr missing 37-64% before 2021, ~0% from 2021 on; discovery_hour missing 30-60% in the 1990s vs 4-16% after 2020. Test windows sit in the regime-changed period, so the split tests a data-collection change as much as generalisation. Change: report it; consider starting the data in a later year (e.g. 2005+) or accept as realistic drift.
2. Selection: no "Missing/Undetermined" class, so those fires were dropped (inferred; could not confirm counts). That is the population the model would actually be used on, and it differs (more remote/unknown agencies). Fine for benchmarking, but document it.
3. High-cardinality IDs (source_reporting_unit 3,865 levels, reporting unit 1,461, fips 2,845) as categoricals; fips_code is a category with 26% missing (state+county code, could be derived from lat/lon). Reporting-unit/agency codes encode which agency's cause-coding practice applies - legitimate at prediction time but a source of label-convention signal. Redundant columns (source_system vs source_system_type vs reporting agency; state vs fips) - acceptable.
4. Coordinates include longitude up to +144.85 (Guam/Pacific territories) and lat up to 70 (Alaska) - plausible, not errors.
5. Heavy class imbalance (firearms 0.3%, fireworks 1.2%); use log-loss / balanced metrics, not accuracy alone.
6. Small: 174 duplicate rows - likely genuine distinct fires same place/day, harmless.

Could not check: full 1.14M table (only 200k sample), exact test window boundaries, how many undetermined-cause rows were removed, whether multi-source duplicate records (the FOD dedup process) leaked across splits.
```

</details>

<details><summary>Task gamer: fpa_fod_wildfire_cause</summary>

```text
FPA-FOD wildfire cause -- task gamer report
Verdict: barely gameable. The best exploit (statistics over all rows, test included) gains 0.018 log-loss. An honest choice, training only on the last 10 years, gains three times as much (0.055).

Setup: LightGBM (300 trees, lr 0.05, 63 leaves, min_child 200, lambda 5, probabilities clipped at 1e-4). Fitted on 300k rows sampled from each train side; features() plus day of year, year and weekday. Script: work/gam.py, log: work/gam.log.
Splits r0/r1/r2 test on 2024/2023/2022.
Baseline: [1.4350 1.5262 1.4226], mean 1.4613. Noise (baseline + a random column): [1.4362 1.5150 1.4144], mean 1.4552, so the spread is about 0.006-0.011 per split.
(Note: an untuned lr 0.1 / 127-leaf model gave unstable log-loss of 1.6-6.4, because overconfident probabilities hit near-zero.)

Exploits ranked by gain:
| # | Exploit | Honest | Exploited | Gain per split | Deployed has it? | Fix |
| 1 | n_loc_all: count of fires at the same lat/lon (rounded to 2 decimals) over ALL rows, test and future years included | 1.4613 | 1.4431 | 0.016 / 0.021 / 0.017 | Partly: the count of past fires is legitimate, the future and test part is not. Not separated. | Nothing needed in the task. A participant who wants to stay honest uses past-only counts. |
| 2 | n_unit_day: fires of the same reporting unit on the same day, counted over all rows | 1.4613 | 1.4527 | 0.002 / 0.013 / 0.011 | Mostly no: it includes fires found later that day. A same-day count so far would be legitimate. | Near noise level; none needed. |
| 3 | rank_in_day (row position within the date) | 1.4613 | 1.4559 | 0.003 / 0.008 / 0.005 | No | Within noise. Shuffling rows within a day would make it impossible. |

Flaw that hurts an honest model:
- The training sides reach back to 1992, and the cause mix drifts. Debris burning rose from 0.24 (1992) to 0.44 (2022); arson fell from 0.21 to 0.11; power lines rose from 0.00 to 0.05.
- Training only on the 10 years before each test window: [1.3738 1.4553 1.3912], mean 1.4068.
- Against the baseline's 1.4613 that is 0.055 better, on every split. This is honest, since a deployed model may choose its own window. Recency weighting or a year feature fitted on recent years also captures it.
- Possible fix: none required. Optionally note the drift in task.md.
- Also: the test years (45-50k rows each) carry about twice the yearly row density of the training years (24-50k). The train side seems to be a 1M-row subsample of all earlier rows. This is harmless but worth knowing.

Found nothing:
- Coordinate formats: lat_dec gave 1.4590 and lon_dec 1.4620, both within noise. Decimal count does vary by class, but that is a source-system effect and a deployed model has it too.
- Missing discovery_hour: hour_na gave 1.4613, no gain. Missingness is class-informative (Natural 0.23 when present vs 0.08 when missing), but LightGBM already sees NaN, and it is known at report time.
- Row order: next-row label agreement is 0.296 vs 0.196 by chance. It is explained by same-day, same-place clustering (0.53 when the same unit), not by sorting; rank_in_day is within noise.
- No identifiers are left: no FOD_ID, fire name or local incident ID. Unit and source codes are legitimate at report time.
- Copies across the split: the regime is temporal. Earlier fires at the same place are legitimate history and were not tested as a separate exploit.
Not checked:
- Web forums and magic features: the known Kaggle "188 million fires" leaks (fire size, containment date, cont_time) are absent from this kit, so they cannot be used.
- Past-only versions of the count features.
- A train-vs-test adversarial classifier.
- Lookup in the published source (it would work, since every row is public; not ranked).
```

</details>

<details><summary>Precedent check: fpa_fod_wildfire_cause</summary>

```text
Precedent checker: fpa_fod_wildfire_cause (folder fpa_fod_wildfire_cause_1m), 2026-11-09

Verdict: consistent with precedent on all four draft issues; one rule citation to correct (issue 1), one option missing
(issue 2). No real pair of similar cases decided differently; no drift; no third exception of one kind.

Sources read: builder_report.md, register.json (decisions with LEAK-25, LEAK-13, SPLIT-20, SPLIT-14), Cases tables of
leak_checks.md (LEAK-13, LEAK-25 and its amendments of 2026-10-21 and 2026-11-02) and splits.md (SPLIT-20/21).
Sibling fpa_fod_attributes_wildfire_size has no v2 folder, so no sibling call to compare.

1. Issue 1, "Other causes" left out (builder: a). CONSISTENT, with a stated distinguishing fact; citation fix.
   - Closest precedent: noaa_storm_events_damage (LEAK-25 amended 2026-11-02, Andrej): a recording convention that
     follows a reporting unit shipped as a feature may be KEPT, but "only when the task keeps a measured signal beyond
     the unit, the period and the place". Here the state and date alone rank "Other" at ROC AUC 0.77-0.80 against
     0.78-0.82 on all inputs: almost no signal beyond unit/period/place, so the amendment's condition fails and the
     drop follows it. The convention also appears only at the test era (0.6% -> 18-28%), which noaa (spread 7-91%
     across the whole history) did not have. Both facts set the case apart.
   - Citation: "Other causes" is not "no event mixed with not recorded" (LEAK-25's mechanism); it is a class-specific
     recording convention by unit (LEAK-13 family) handled by the reasoning of the LEAK-25 2026-11-02 amendment. Cite
     LEAK-13 plus "by analogy to the LEAK-25 amendment of 2026-11-02 (noaa_storm_events_damage)" in the issue and notes.
   - Follow noaa's USE-3 point: the population sentence in task_summary must say that the test windows lose 25-35% of
     their labelled fires to the dropped class (noaa: "events with a damage entry").
2. Issue 2, full history across the 2020-2021 break (builder: a). CONSISTENT, with a reason (SPLIT-14 Must bars c).
   - Precedents that cut the history at a break: chicago_traffic_crashes (2026-11-04, training from citywide coverage,
     SPLIT-20), aeolus (2026-10-12, from 2023). Precedents that kept with a note: chile_school_dropout_mineduc (COVID
     years), noaa_afsc_bottom_trawl_survey_cpue (tow era on the training side only), chicago 2023Q4 step (2026-11-05).
     The distinguishing fact for keeping: after the break there is too little history (option c gives 38.5% for the
     oldest window, under SPLIT-14), and Short mapped the old systems' causes to the 2020 standard; chicago's cut
     removed an incomplete population, not a recording system. Holds.
   - Missing option for the curator (SPLIT-20 asks for "a recent stretch ... and say why"): a later start that still
     meets SPLIT-14 (e.g. 2010 or 2015), a middle path like aeolus. Should be listed as an option even if not chosen.
   - SPLIT-21 respected: the recommendation is not taken from test-window scores.
3. Issue 3, reporting fields kept (builder: a). CONSISTENT. noaa_storm_events_damage kept the reporting office as a
   feature; LEAK-13 cases (hepatitis_c_prediction, gallstone_disease) drop a column only when it is a one-class
   artefact, which these fields are not. Not deciding from the untuned-LightGBM gain follows SPLIT-21/EV-6.
4. Issue 4, map service instead of the DOI archive (builder: a). CONSISTENT with PROV-9 practice (count assert, revisit
   note); no contrary precedent found.
Other calls: ICS-209/MTBS-only records dropped by source system (a rule that does not read the label) follows the
LEAK-25 amendment of 2026-10-21 (caracas_cervical_cancer, account_debt_south_africa). Log loss fallback (MET-1/5)
follows the usual fallback. Codes categorical (CLEAN-14) consistent.

No reflection prompts needed: no departure without a reason.
```

</details>

<details><summary>Advocate: fpa_fod_wildfire_cause</summary>

```text
Advocate, opening brief: fpa_fod_wildfire_cause (folder fpa_fod_wildfire_cause_1m), 2026-11-09
Position: ship as defined (issues 1-4 at option a), plus documentation edits that need no decision.

1. No leak survives, and every check that could fail was run (P4, LEAK-10/LEAK-16..20, Must).
   Evidence: claim auditor finds no refuted claim. 12 features, all known at discovery. 0 exact copies across the split on 3/3 windows.
   No containment before discovery. Missing flags alone reach ROC AUC 0.513 at most. Task gamer: the best exploit
   (counts over all rows) gains 0.016-0.021 log loss, and the rest are within noise (0.006-0.011). Outranks: any
   "leakage" objection. This is a Must, and it is measured as met.

2. Dropping "Other causes" is right and follows precedent (P4, LEAK-13 plus the LEAK-25 amendment of 2026-11-02, Must).
   Evidence: "Other" went from 0.6% of fires to 18-28% after 2021. The state and the date alone rank it at AUC 0.77-0.80, against 0.78-0.82 on all inputs.
   noaa's condition for keeping a recording convention (signal beyond unit, period and place) fails here. Column, domain and precedent agents all agree.
   Real problem conceded: citation and population wording. Mildest fix, no decision needed: cite LEAK-13 with the noaa analogy, and
   add the population sentence ("test windows lose 25-35% of their labelled fires to the dropped class").

3. The split is right. The reporting break is a Should, and it cannot outrank SPLIT-14 (Must) (SPLIT-1, SPLIT-13, SPLIT-14, SPLIT-20).
   Evidence: train max date < test start on every window. Units are known entities (96-100% seen), which fits the use. A cut to 2020 leaves 38.5%
   for the oldest window, under SPLIT-14's floor, and scores worse in 2022 (1.437 vs 1.353). Recent-only training helps 0.01-0.08,
   but the shipped train side holds those years and the date is a feature. That is a modelling choice, not a broken split
   (split auditor, gamer: "honest, a deployed model may choose its own window"). Also, test = InFORM is the system agencies
   report in today, so the shift is the deployment's own shift (domain, split auditor).
   Fix on the remedy ladder: note, not cut. Put the split auditor's and gamer's numbers into splits_comment. Add the later-start option
   (2010/2015) to issue 2 for completeness (precedent checker). The recommendation stays (a).

4. Clear, stable value over baselines (P6, TP-1..9).
   Evidence: linear 1.449 vs dummy 1.884, which is 23.1% skill, SE 0.017-0.024, better on 3/3 windows. The smallest class has 279 test rows per window.
   1.88M real labelled fires make a large multiclass environmental task, and the gap is filled (builder's weighing).

5. The metric fits the decision (P6, MET-1, MET-5..MET-8).
   Evidence: the domain practitioner attributes causes by summing class probabilities over undetermined fires, so a strictly proper rule
   on the full distribution is what they would select by. The papers report several accuracies, with no threshold or cost (claim auditor
   re-checked Pourmohamad 2025). Fallback log loss holds. No agent disputes it.

6. The use case is real and its fit is honestly "approximate" (P3, USE-1, USE-3, USE-5, USE-6, USE-8).
   Evidence: the source's authors pose cause attribution (Short 2014, Pourmohamad 2025). One row is one report is one decision. Reporting
   fields are "who I am" (USE-6), and the domain, column, split and precedent agents all keep them (issue 3 (a)). The untuned-LightGBM
   gain from dropping them is not a basis to decide (EV-6, SPLIT-21).
   Real problems conceded: labels come only from determined fires (selection), and lightning and weather inputs are missing. Both are properties of the source. They are
   already in or belong in fit_reason. Mildest fix: name the missing lightning/weather covariates and the dropped
   undetermined pool in the notes (blind reviewer 2, domain 1/3). This is "approximate" under USE-8, not an exclusion.

7. The remaining concerns are documentation, not validity (P4, LEAK-13/LEAK-14/LEAK-24, Should/Could).
   - LEAK-24: undetermined alone rises 15.0% -> 28.8%, but there is no within-year fall-off (2024 Q4 < Q3), so there is no censoring signature.
     Fix: add the per-year and per-quarter shares to the note.
   - Hour missingness by class is 2.8-21.5%. The flag gives no gain (builder, gamer: hour_na 1.4613 = baseline). Fix: cite the shares.
   - fips_code missingness is 13-90% by cause in federal records only, and 0-7% in test years. Fix: a note. Optionally check it within agency.
   - owner_descr/hour missingness falls over time (blind reviewer). That is the same system break as point 3, and it is noted, not cut.
   - Record name says "6th edition 1992-2020". Fix at step 8.
   These are independent failures, not conflicts: none blocks a Must, and each has a no-decision remedy.
```

</details>

<details><summary>Critic: fpa_fod_wildfire_cause</summary>

```text
Critic, opening brief: fpa_fod_wildfire_cause (folder fpa_fod_wildfire_cause_1m), 2026-11-09
Verdict: ship only after changes 1-4 (definition text and the curator's options); no point calls for exclusion.
No panel agent found a Must that fails, so none of this is a case for exclusion.

1. The labelled population is cut hard and the task text does not say so (P3, USE-5/USE-8 Must; USE-3 population).
   Problem: the test windows lose 25-35% of their labelled fires to the dropped "Other causes" (claim auditor 34.6/27.6/25.3%,
   2022-24), and undetermined fires are another 22-29% of each year (claim auditor: 15.0% in 2021 -> 28.8% 2023). task_summary.row
   says only "with a named cause"; changes names the drop but not its size. Effect: a reader takes the score for "US fires",
   while it is about half of each test year, skewed towards investigated classes (domain: arson/equipment overstated).
   Remedy: add the 25-35% and the undetermined share to the population sentence (precedent noaa_storm_events_damage, as the
   precedent checker asks).

2. Issue 1 cites the wrong mechanism (LEAK-13 Must, LEAK-25 by analogy). "Other causes" is a unit recording convention,
   not "no event mixed with not recorded" (precedent checker). Effect: the precedent set drifts if LEAK-25 is cited bare.
   Remedy: cite LEAK-13 plus the 2026-11-02 LEAK-25 amendment (noaa) and its failed condition (state+date AUC 0.77-0.80 vs
   0.78-0.82 all inputs) in the issue and the note.

3. Issue 2 leaves out the option SPLIT-20 asks for (SPLIT-20 Should, SPLIT-14 Must). Only "from 1992", "cut at 2020",
   "from 2020" are offered; the last fails SPLIT-14. A later start (2005/2010/2015) that meets SPLIT-14 is missing. Evidence:
   split auditor, since-2016 history beats the shipped history by 0.01-0.08 on 3/3 years (1.302/1.378/1.339 vs 1.363/1.461/
   1.353); gamer, last-10-years +0.055 on 3/3; blind reviewer independently proposes 2005+ (owner missing 37-64% before 2021,
   ~0% after; hour missing 30-60% in the 1990s). Also the random 1M sample puts 92-97% of training in pre-InFORM systems.
   Remedy: add option (d) a later start (or latest-1M sample) to issue 2 with these numbers, and put them in
   splits_comment whichever option is chosen (SPLIT-21: decide on the reason, not the test score).

4. "Who reports" carries most of the signal (USE-6, LEAK-13; issue 3). nwcg_reporting_unit_id alone 1.481 vs linear 1.449
   (domain, builder); untuned LightGBM better without the reporting fields in 3/3 years (0.029-0.125). Older systems never code
   some classes (GA, MS, SC). The linear family was never fit without them (claim auditor: untested). Effect: the benchmark may
   rank models on unit-level label conventions learned from systems absent at test time. Remedy: keep (a) but run the linear
   probe without source_system/source_system_type before the curator decides; if it gains, offer (b) as recommended.

5. LEAK-24 note reads too reassuring (LEAK-24, Should). It cites only undetermined+Other combined (49.1/48.4/46.7%); the
   undetermined share alone nearly doubled 2021->2023 (claim auditor). Quarterly check shows no censoring, so the conclusion
   holds. Remedy: add the undetermined-alone shares and the quarterly 2024 numbers to the note.

6. Missing-by-class patterns not documented (LEAK-13/LEAK-39 Could, quality). Hour missing 2.8% (Natural) to 21.5% (Smoking),
   within-state AUC 0.59 (claim auditor); fips_code missing 13-90% by cause in federal records (column auditor). No gain shown,
   so no change to data. Remedy: a note per column with the shares. Quality only, not a reason to exclude.

7. Record `name` still says 6th edition 1992-2020 (builder, claim auditor). Remedy: fix at step 8. Also name the absent
   lightning/weather inputs as a gap of the source in fit_reason (domain).

Dropped: gamer exploits (<=0.021, near noise); copies, splits, metric (all held).
```

</details>
