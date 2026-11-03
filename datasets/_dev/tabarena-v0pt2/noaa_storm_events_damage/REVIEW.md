# noaa_storm_events_damage

**Outcome:** added. The AI recommends shipping it as changed: you amended LEAK-25 on 2026-11-02 so the $0 entries
stay, and `Data Quality Issue` left the record. NOAA NCEI's Storm Events Database,
2007-2025: 999,757 entries of the property damage an NWS office entered for one event in one county or zone, 73% of
them $0, for an emergency manager ranking a storm's counties for damage-assessment teams; tested on the calendar years
2023-2025 with a 3-month gap, scored by RMSLE (by context; the source has none).

Changed after the panel, no decision needed: the fixes listed below; the target bullet now quotes your call of
2026-10-30 in place of the AI's gloss ("a cleaning choice") and marks the reading of the blank as the "no information
available" box as an inference. On the changed definition untuned LightGBM scores RMSLE 2.42, 2.63 and 2.58 (2025,
2024, 2023) against 3.82, 4.01 and 3.87 for a constant. The numbers in the issues are the panel's runs, made with a
2-month gap and before the double entries were dropped (its full model scored 2.41, 2.63 and 2.59, and put 41-49% of its
error on the $0 entries, against 37-47% now).

Validity:
* SEL-3 holds on your `Yes` of 2026-10-30; the check against us_accidents is settled with LEAK-25's amendment
  (2026-11-02).
* USE-5 was broken and is fixed: the insurer's catastrophe desk and "what to reserve" are dropped from the use case.
  Storm Data's 2024 total is $15.7B against $182.7B for NCEI's billion-dollar events, and hail is 11% of the rows but 1%
  of the dollars, so the label is another quantity than an insurer's loss. USE-8: fit approximate; `fit_reason` now
  names the gaps.
* USE-3: the prediction point is the first report, before any damage figure exists; the real-time Local Storm Reports
  were used to check the inputs against it.
* LEAK-25 triggered, not recovered; kept under the rule as amended on 2026-11-02.
* LEAK-10 triggered three times and fixed. The wind speeds the office estimated from the damage (EG, ES) are blank
  (94.4% of the 2024 ones were missing from the real-time first reports); the tornado durations are blank (they track
  the dropped surveyed path); `hurricane_category` is dropped (set per zone, partly after the event). In the panel's run
  the three fixes moved RMSLE from 2.50 to 2.56 over the 3 windows, against 3.90 for a constant. LEAK-37: strong wind,
  lightning and weaker thunderstorm wind enter Storm Data only with damage (3.5-4.0% of the test rows); `known` now says
  that the first report tells whether damage was seen.
* SPLIT-1, SPLIT-6, SPLIT-9, SPLIT-13, SPLIT-14 and SPLIT-20 hold: known counties and offices, no storm crosses a
  window, later releases change 0-0.17% of the labels, and the 2007 start sits on a measured change of entry format.
  SPLIT-10 was departed from and is fixed: the gap is now 3 months, since NCEI's public files lag 75-80 days and
  October is not public on 1 January (cost +0.02-0.03 RMSLE, an edge effect).

Value: TP-2, a real signal: RMSLE about 2.55 against 3.90 for a constant; 62% of that gain comes from the office (the
LEAK-25 note). MET-11: RMSLE by context, since the damage spans nine orders of magnitude and on raw dollars 0.1% of the
entries hold 99.96% of the squared deviation. MET-1: the reason now names Diaz and Joseph (2019, Weather and Climate
Extremes 25:100216; several metrics, tornadoes only, a random split, so no source metric) and says that 37-47% of the
error falls on the $0 entries (issue 3).

Quality: LEAK-19 (1,072 double entries dropped), CLEAN-21 (`magnitude` split into wind speed and hail size), CLEAN-11
(24 impossible wind speeds, all estimated ones, now blank).

Weighed: size +; the NWS directive and a public-domain source +; an honest temporal split +; approximate fit -; the
office's $0 convention in the label -.

Not adopted: county exposure from the Census, an outside join; the 40% zone rows would need the NWS zone-county
file (practitioner).

For the curator: issue 2 (drop the hazards nobody assesses, a weighing
call), issue 3 (RMSLE or a within-storm score, a weighing call), issue 4 (the storm's size as an input, a probe first).

**Main points:** all issues resolved on 2026-11-03: the unassessed hazards dropped (2), RMSLE stays (3), no
storm-size input (4).

**Issues for Andrej:**

2. **Drop the hazards nobody sends an assessor for?**

   * **Problem:**
     - With the use case narrowed to the emergency manager's triage, about a fifth of the rows are hazards with no
       assessment decision behind them, nearly all at $0.
     - Every row filter is checked against the use case, so this is a weighing of which rows the decision covers[^a1].
   * **Background:** The hazards: marine zones, drought, heat, cold, fog, rip current, funnel cloud, waterspout and
     high surf. They are 19.8% of the 2024 rows, 99.7% of them at $0, with 0.07% of the dollars.
   * **Effect on the task:** the event type alone predicts these zeros, so they make the task look easier and RMSLE
     rewards predicting 0 on them; the rows the manager decides on are the others.
   * **Consistency:** no precedent.
   * **Panel:** the domain practitioner and the critic suggest dropping them. No one argues for keeping them (the
     advocate calls the drop optional). Which hazards an emergency manager assesses is a domain judgement, and the list
     is the practitioner's.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | All 54 event types (implemented) | every hazard stays | no domain list to defend | about 20% of rows are zeros the event type predicts; RMSLE rewards predicting 0 on them |
     | B | Drop the listed types | the rows of the nine hazard types (marine zones, drought, heat and six more) go, about 20% of the rows | the rows match the manager's decision | the list is one practitioner's domain judgement |

   * **Recommendation:** B, drop them: no one argues for keeping them, and the rest are the rows the manager decides
     on. **Decision:** A (keep) or B (drop)?

   **Notes for the AI:** the types to drop on B: marine zones, drought, heat, cold, fog, rip current, funnel cloud,
   waterspout, high surf (the practitioner's list); the rule is USE-1 (Must, P3).

   [^a1]: **USE-1** (Must, principle P3, a real use case): a use case is an actor, a moment and a decision; every
     column, filter, target and split choice is checked against it.

   **Andrej (2026-11-03, change):** I go with your suggested change

   **Resolved (2026-11-03, Andrej):** B. Every marine type and drought, heat, excessive heat, the two cold types, the
   two fog types, rip current, funnel cloud, waterspout and high surf are dropped: 156,767 entries (15.7%), 99.1% at
   $0, 0.5% of the dollars. 843,144 rows and 34 event types remain, 68% at $0. RMSLE rises to 2.67, 2.93 and 2.94
   (constant 4.05, 4.28, 4.20), as the easy zeros are gone. `dataset check` clean (Slurm).

3. **Keep RMSLE, or score within each storm?**

   * **Problem:**
     - RMSLE scores every row on its own; the manager ranks the counties of one storm.
     - Switch to a within-storm score (`mean_group_pearsonr`), which holds the reporting office fixed so the $0 habit
       counts less?
     - This is a weighing call.
   * **Background:** `mean_group_pearsonr` is the correlation between predicted and entered dollars inside each storm,
     averaged over storms, with the storm id `EPISODE_ID` shipped as a scoring column and never as a feature. It holds
     the office fixed since one office enters each storm. The metric has to score the decision of the use case at the
     unit the actor acts on[^b1]; RMSLE was chosen from the context of the task[^b2].
   * **Experiments:** on 2024, RMSLE and the within-storm score pick the same model. The insurance siblings'
     normalized Gini picks a model that ranks a storm's counties worse, so it is no option here. RMSLE's reason in the
     definition says that 37-47% of the error falls on the $0 entries.
   * **Effect on the task:** under the within-storm score, storms whose rows are all $0 drop out (59.9% of the 2024
     storms with five or more rows), and so do storms where a model predicts one value for every row, so a model can
     skip hard storms.
   * **Consistency:** diamonds and onlinenewspopularity score RMSLE by context; neither had a mass at zero.
   * **Panel:** the advocate and the critic keep RMSLE; the domain practitioner prefers the within-storm score.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | RMSLE (implemented) | scores every row on its own | picks the same model as the within-storm score on 2024; every storm counts | 37-47% of the error falls on the $0 entries |
     | B | `mean_group_pearsonr` by `EPISODE_ID` | scores the ranking of counties inside each storm | the manager's unit; holds the office fixed, so the $0 habit counts less | all-$0 storms (59.9% of 2024 storms with 5+ rows) and constant-prediction storms drop out, so a model can skip hard storms |

   * **Recommendation:** A, keep RMSLE: both scores pick the same model on 2024, and the within-storm score lets a
     model skip hard storms. **Decision:** A (keep RMSLE) or B (switch)?

   **Notes for the AI:** on B, ship `EPISODE_ID` as a scoring column (never a feature) and declare
   `mean_group_pearsonr` grouped by it; the rules are MET-1 (Must, P6) and MET-11 (context).

   [^b1]: **MET-1** (Must, principle P6, worth benchmarking): the declared metric scores the real task, the decision
     of the use case at the unit the actor acts on, the way a practitioner would choose a model for it.
   [^b2]: **MET-11** (Must), origin "context": the source defines no metric but the task makes one obvious, and the
     reason says why (Lennart, 2026-10-21, diamonds: a price's error matters relative to the price, so `rmsle`).

   **Resolved (2026-11-03, Andrej):** A, RMSLE stays.

4. **Add the storm's size as an input?**

   * **Problem:**
     - Once a storm has passed, the manager knows how many counties it hit.
     - The domain practitioner proposes the number of events and counties per storm (`EPISODE_ID`); the mediator did not
       take it up.
     - We build an input the actor reads at the prediction point from other rows of the same release[^c1].
   * **Effect on the task:** Storm Data's county segments and which events get entered depend on the damage (domain
     practitioner; some types enter only with damage), so a count per storm partly carries the label. A feature must
     never give the target away[^c2].
   * **Unknown:** not measured; a leak probe on the counts would settle whether they carry label signal.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No storm-level input (implemented) | no column on the storm's size | no risk of a label carried by the counts | the manager knows the storm's size and the model does not |
     | B | Add the counts now | adds two columns: events and counties per `EPISODE_ID`, counted over all entries including the blanks | an input the actor has | the counts partly carry the label; not measured |
     | C | Probe first | add the counts of B only if a leak probe shows no label signal | settles the leak before adding | a probe to run |

   * **Recommendation:** A for now, and C to add it: only after a leak probe shows the counts carry no label signal,
     since the leak rule comes before the rule on building features[^c3]. **Decision:** A (not), B (add) or C (probe
     first)?

   **Notes for the AI:** on B or C, count events and counties per `EPISODE_ID` over all entries including the blanks;
   for C, run a leak probe on the two counts before adding them (LEAK-10 before CLEAN-19).

   [^c1]: **CLEAN-19** (Should, amended 2026-10-26, Lennart, on rain_in_australia): we build a feature when it is an
     input the actor reads at the prediction point from other rows of the same release, kept only where known by then.
   [^c2]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target
     away; a part, a consequence or another encoding of the target is out.
   [^c3]: **LEAK-10** (Must) is checked before **CLEAN-19** (Should): a built feature must first pass the leak rule.

   **Andrej (2026-11-03, discuss):** If the counts partially carry the label, is this a leak or signal?

   **Answer (AI, 2026-11-03):**

   * **Problem:**
     - Both, in different parts: the storm's real size is a signal the manager has, but some entries exist only
       because there was damage, and counting those counts the label.
     - Measured, neither part matters: the counts change RMSLE by about 0.01 either way, so they add nothing.
     - So the safe call is no storm-level input.
   * **Background:** Storm Data enters strong wind, lightning and thunderstorm wind under 50 kt only when they did
     damage (3.3% of the entries). A count over all of a storm's entries rises with them, so part of it is a
     consequence of the damage; a count over the other types follows the storm's size, which the first reports show.
   * **Experiments:** untuned LightGBM on log1p, RMSLE per test year (lower is better), on the rows left after issue 2:

     | Input | 2025 | 2024 | 2023 |
     |---|---|---|---|
     | no storm size (implemented) | 2.671 | 2.931 | 2.940 |
     | entries and counties of the storm, all types | 2.661 | 2.928 | 2.941 |
     | entries and counties of the types entered whatever the damage | 2.659 | 2.948 | 2.951 |

     The label part is too small to show, and the size adds no measurable signal either.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | No storm-level input (implemented) | as now | nothing that can carry the label | none measured |
     | B | Counts over the types entered whatever the damage | two columns per storm | the storm's size as the manager sees it | no gain measured; still counts entries finalised after the storm |

   * **Recommendation:** A: the counts add nothing measurable, and the all-types count carries part of the label.
     **Decision:** A or B?

   **Notes for the AI:** script `noaa_storm/storm_size.py` in the run folder of 2026-11-03 (Slurm job 1342406).

   **Resolved (2026-11-03, Andrej):** A, no storm-level input; the notes give the measurement.

5. **Is the task real, or did we make it up?**

   * **Problem:**
     - The data and the label are real, and so is predicting the label: Diaz and Joseph (2019, Weather and Climate
       Extremes 25:100216) predict exactly this field from these entries, "for science-informed tornado disaster
       planning".
     - The moment is ours: no source names an emergency manager ranking a storm's counties by the NWS figure.
     - So the task is real as a damage model for planning and approximate as the triage we wrote; the `fit_reason`
       names the gaps of the second.
   * **Background:** local managers triage from 911 calls and their own reports, and the NWS figure comes back weeks
     later, partly built from those reports (domain practitioner; NWSI 10-1605 Sec. 2.7).
   * **Consistency:** basque_offshore_ctd_chlorophyll went `No` as a made-up task today: there no source named any use
     for predicting the channel and no one had predicted it for a use[^5a]. Here a peer-reviewed study predicts the
     same label, and the published loss records built from it (SHELDUS, behind FEMA's National Risk Index) are used
     for planning. That is the fact that sets this case apart.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship with the triage use case (implemented) | as now; fit approximate | a concrete actor and moment, and the split and inputs follow it; the label is modelled in the literature | the triage moment is our framing; the manager decides from other sources |
     | B | Ship with the planning use case | the use case becomes the published one: a planner estimates the damage of an event of this type and size in a county; split and inputs unchanged | the use case of the literature, nothing ours | a planner uses aggregate losses more than an estimate per event |
     | C | `No` with `No Good Target / Scientific Discovery` | retire as basque_offshore_ctd_chlorophyll | no framing of ours | the published use of this label is not weighed |

   * **Recommendation:** B: the same data, split and score, with the use case the literature gives, so nothing in the
     task is ours; the `fit_reason` keeps the gaps. **Decision:** A, B or C?

   **Notes for the AI:** on B, rewrite `task_summary.use_case`, `fit_reason` and `known` (the inputs a planner has
   are the same entries), and check that `splits_comment` reads with a planner refitting each year. On C, retire as
   records.md says.

   [^5a]: **USE-1** (Must): a use case is an actor, a moment and a decision. **USE-2** (Must): a task no decision fits
     is out, marker `No Good Target / Scientific Discovery`. basque_offshore_ctd_chlorophyll, Andrej, 2026-11-03: "it
     seems like this is a made up task".

   **Andrej (2026-11-03, dataset note):** One last question before we ship: Is this even a real task opr did we make it
   up?

   **Andrej (2026-11-03, change):** I go with your change

   **Resolved (2026-11-03, Andrej):** B: `use_case` is the planner's (Diaz and Joseph 2019), `fit_reason` names the
   gaps for a planner; data, split and metric unchanged. `dataset check` clean (Slurm).

**Review panel:** ship after changes if LEAK-25 is amended, otherwise `No` (mediator). Claim audit: 44 claims, 29 hold
(3 with a caveat), 11 refuted (2 in part; all fixed in the definition, the LEAK-25 part is issue 1), 4 untested (older
label revisions and a forum post open; the other two now a note and issue 3). Blind review: would include with changes;
its main concern is that the zero label is mostly an office reporting convention that drifts over time. Debate: agreed
on the temporal split with a 3-month gap, the three LEAK-10 fixes, the narrowed use case, `rmsle` with its reason
repaired and the quality fixes; disputed at the end: only the amendment's wording (issue 1); the critic withdrew the
us_accidents objection.

<details><summary>Mediator</summary>

**Mediator: noaa_storm_events_damage (2026-11-01)**

**Recommendation**

```text
Verdict: ship after changes, on one condition: the curator amends LEAK-25 (issue 1). Under the rule as written: don't
  ship (`No`, LEAK-25).
Validity: SEL-3 holds on the curator's `Yes` (2026-10-30), consistency check against us_accidents open (issue 1);
  USE-1 holds once narrowed to the emergency manager's triage; USE-5 triggered (the insurer half), fixed (dropped);
  USE-8 approximate, reason rewritten; LEAK-25 triggered, not recovered (issue 1); LEAK-10 triggered three times,
  fixed (EG/ES speeds blanked, tornado durations blanked, `hurricane_category` dropped); LEAK-37 holds for the types
  entered only with damage (said in `known`); SPLIT-1, SPLIT-3, SPLIT-6, SPLIT-9, SPLIT-13, SPLIT-14, SPLIT-20 hold;
  SPLIT-10 departure, fixed (gap 3 months).
Value: TP-2, a real signal after the fixes (RMSLE about 2.55 against a dummy at 3.90, 3 windows), 62% of the gain from
  the office; MET-11 `rmsle` kept, reason repaired (MET-1).
Quality: LEAK-19 (1,072 double entries), CLEAN-21 (`magnitude` holds knots and inches), CLEAN-11 (24 impossible wind
  values) fixed; text corrections.
Weighed: size +, source (NWS directive, public domain) +, honest temporal split +, approximate fit -, office
  convention in the label -.
For the curator: issue 1 (LEAK-25: amend or `No`, with the us_accidents check), issue 2 (drop the hazards nobody
  assesses, a weighing call), issue 3 (`rmsle` or a within-storm score, a weighing call).
```

The debate narrowed to LEAK-25. Both debaters concede every other point to the other side's evidence, and both say the
dataset ships only if the curator amends LEAK-25. I ran three checks (mediator scratch: `m1_blank_drift`,
`m2_beyond_subsets`, `m3_ablation`; untuned LightGBM, the advocate's parameters, the shipped windows, the three LEAK-10
fixes applied).

**Agreed facts**

1. 1,000,829 entries 2007-2025 with a damage figure; the 18.3% of 1,225,290 events left blank are dropped; 73% of the
   entries are $0 (test windows 74.2%, 74.0%, 76.3%).
2. The split is right: county_zone seen in train for 99.2% of test rows, office and state 100%; 0 of 167,629 episodes
   span two months; later releases change 0 of 64,921 Jan-Oct 2025 values and 0.17% of 2024's; a random split
   overrates by 0.16-0.36 RMSLE.
3. NCEI's public files lag 75-80 days (C00510: "up to a 120 day delay possible"), so the 2-month gap gives each training
   side one month (0.15-0.21% of rows) the actor would not have; gap 3 costs 0.02-0.03, an edge effect.
4. Three columns hold values written after the first report: 94.4% of the 2024 EG speeds were absent from the real-time
   Local Storm Reports ("TSTM WND DMG", no speed), against 92.7% carry-over for measured gusts and 97.9% for hail; ES is
   the same estimate (1,164 entries); tornado duration tracks the dropped path length (Spearman 0.83); the hurricane
   category is set per zone (Michael's Cat 5 is the April 2019 reanalysis; 483 rows, none in 2025).
5. After the three fixes: RMSLE 2.54-2.56 (mean of 3 windows) against a dummy at 3.90. Event type and time give 3.55,
   the office 2.71: 62% of the gain is the office.
6. A $0 mixes "no damage" with "no estimate made": 13 of 121 EF4/EF5 tornado segments and 17.3% of EF2+ are at $0;
   the Thunderstorm Wind $0 share runs 7%-91% across offices. The mix sits in the events entered by a criterion (severe
   wind, hail); in the types entered only with damage, a $0 without casualty or crop damage is 0.3-3.1%.
7. The 2007 break is a change of entry format: in 2006, which holds both, the old PDS rows are 71.3% blank (floods
   63.3%, which the directive forbids) and the CSV rows 0.1% (floods 0 of 710).
8. Strong Wind, Lightning and Thunderstorm Wind below 50 kt enter Storm Data only with damage (94-98% positive, 3.5-4.0%
   of test rows); the first report says whether damage was seen (LEAK-37).
9. The insurer half of the use case fails USE-5: Storm Data's 2024 total is $15.7B against $182.7B for NCEI's
   billion-dollar events; hail is 11.1% of the rows and 1.4% of the dollars.
10. Metric: on raw dollars the top 0.1% of entries hold 99.96% of the squared deviation; `normalized_gini` picks the
    model that ranks a storm's counties worse; 41-49% of RMSLE's squared error sits on the $0 rows; Diaz and Joseph
    (2019) exist (several metrics, tornadoes only, random split: no source metric, MET-5).
11. Every storm (episode) is entered by one office. 1,072 rows are exact copies of another in every published column.
12. LEAK-25 is a Must and takes no exception; re-targeting to the positive amounts is withdrawn (rows selected on the
    label; whether an office enters a figure is not known at the prediction point).

**Changes to make now** (no decision needed)

1. LEAK-10 (Must; located late cells are blanked): blank `magnitude` where `magnitude_type` is EG or ES, keep
   `magnitude_type`; the EG bullet becomes a drop bullet with the LSR numbers. Follows zillow_prize and
   melbourne_housing_market, and this definition's own `TOR_F_SCALE` drop.
2. LEAK-10, LEAK-2 (Must): blank `duration_hours` on every Tornado row (by type, not by `SOURCE`, which would leave the
   survey marker).
3. LEAK-10, LEAK-6 (Must): drop `hurricane_category`; remove the Built bullet's Saffir-Simpson reading.
4. USE-5 (Must): narrow `use_case` to the emergency manager ranking a storm's counties for damage-assessment teams;
   drop "an insurer's catastrophe desk" and "what to reserve".
5. USE-8 (Must): rewrite `fit_reason` to name the gaps: Storm Data entries made weeks later stand in for the first
   reports; tornado types come from surveys; one row per event and county segment against a decision per county and
   storm; the $0 convention differs by office and drifts; no exposure.
6. LEAK-37 (Must), USE-3: `known` and the prediction-point bullet say that the first report tells whether damage was
   seen, with the 3.5-4.0% share; "once the event has ended" in the prediction point (long floods and fires).
7. SPLIT-10 (Should): `gap=3`; `splits_comment` cites C00510 and the measured 75-80 day lag; `task_summary.split` reads
   "every event published by the refit". The default of the rule, so no exception is needed.
8. MET-1 (Must): the metric reason names Diaz and Joseph (2019) and says that 41-49% of the error falls on the $0
   entries. `rmsle` stays.
9. Text on the target (who decides; EV-2): quote the curator's call of 2026-10-30 in place of "coded zeros are a
   cleaning choice" and label that gloss as the AI's; mark "blank = the 'no information' box" as an inference
   (floods have no blanks from 2008 on) and add the within-office shift (disputed point A); the same in the first
   `Decision` text; accept `task_target_value_dominant` as "zero-inflated; part of the zeros are unestimated damage
   (LEAK-25, REVIEW issue 1)".
10. LEAK-19 (Should): drop the 1,072 exact copies; correct the duplicates note.
11. CLEAN-21 (Should): split `magnitude` into `wind_speed_kt` and `hail_size_in` (lossless: 2.6125 against 2.6007).
12. CLEAN-11 (Should): 22 Thunderstorm Wind entries of 1-10 kt and 2 Strong Wind entries of 0 kt become missing.
13. Text (EV-7, EV-8): flood blanks are 26, all in 2007; no episode spans two months (drop "except at New Year"); the
    2024 file comparison leaves out 907 events (1.3%) added or removed; the office practice drifts (r 0.958 from 2024
    to 2025, 0.575 from 2007-2016; 30.5% of offices moved by more than 0.2); scratch numbers on the shipped features
    (base 2.582), recomputed after the fixes; the `SOURCE` bullet loses "(REVIEW issue)" (the drop follows kick and
    expresso_churn_prediction, and no one disputes it).
14. Record: an `Assessment (AI, 2026-11-01)` line: Diaz and Joseph (2019) found; the screening's R^2 0.48 on the
    positives had `SOURCE` and the EG speeds (0.28-0.45 with the fixed features, critic's c02).

**Issues for the curator** (ranked)

1. **LEAK-25 (Must, P4) with the SEL-3 consistency check against us_accidents (P2): amend or `No`.**
   - Problem: a $0 means "no damage" or "no estimate made", depending on the office and the period. The blank drop
     removes the source's own mark only where and when an office uses it. No label-free rule locates the rest.
   - Effect: the score rewards learning each office's habit (62% of the gain); a manager would see counties ranked down
     where the office rarely enters dollars.
   - For keeping (advocate): the curator's call of 2026-10-30 ("We don't care. We want to add any relevant predictive
     task, independent if it is zero inflated or not") covers it; the habit follows a shipped feature and is stable a
     year ahead (r 0.958); with office, period and place given, the other features still lower RMSLE by 0.17-0.21 and
     double the R^2 on the positive amounts in 2025 (disputed point B).
   - For `No` (critic, under the rule as written): the mix is not recovered, and the office's coding moves inside an
     office over time (disputed point A), as us_accidents' codes moved inside a feed.
   - Decision: amend LEAK-25 (wording under disputed point C; it names the fact that sets the case apart from
     us_accidents), or `No`. My recommendation: amend, since the curator's call already points there and the signal
     beyond the habit is measured; the curator should see the 62% before doing so.
2. **USE-1 (Must, P3), a weighing call: drop the hazards nobody sends an assessor for.** Marine zones, drought, heat,
   cold, fog, rip current, funnel cloud, waterspout, high surf: 19.8% of the 2024 rows, 99.7% $0, 0.07% of the
   dollars. Practitioner and critic: drop (the rows lie outside the narrowed decision and are easy zeros). Advocate:
   optional. Which types an emergency manager assesses is a domain judgement. My recommendation: drop.
3. **MET-1 (Must, P6), a weighing call: `rmsle` or a within-storm score.** `mean_group_pearsonr` by `EPISODE_ID` (a
   scoring column) holds the office fixed, so the $0 habit counts less. Against it: all-$0 storms drop out (59.9% of
   the 2024 storms with five or more rows), and so do storms where a model predicts one value, so a model can skip hard
   storms. Advocate and critic keep `rmsle`; the practitioner prefers the within-storm score. On 2024 both pick the
   same model. My recommendation: keep `rmsle`.

**Disputed points**

A. *What the 2007 shift from blanks to $0 means.* The critic first read it as "the 'no information' entries became
$0". The advocate's 2006 table (both formats in one year; fact 7) shows a change of entry format, and the critic
conceded. The live question was then whether, in the CSV format, the blank is the box and the $0 is a real zero (the
advocate's amendment wording rests on it). Decisive check (`m1_blank_drift`): per office, 2007-2010 against
2022-2025, when an office's blank share rose, what fell?

| event type | offices | slope of $0 change on blank change | slope of positive change | offices with blank +0.2 or more: blank, $0, positive |
|---|---|---|---|---|
| Hail | 91 | -1.00 | 0.00 | 32: +0.55, -0.50, -0.05 |
| Thunderstorm Wind | 98 | -0.70 | -0.30 | 21: +0.58, -0.32, -0.26 |
| Winter Storm | 50 | -1.01 | +0.01 | 15: +0.61, -0.54, -0.07 |
| High Wind | 51 | -0.79 | -0.21 | 14: +0.58, -0.35, -0.23 |

All types: blank 7.3% (2007) to 22.7% (2025), $0 70.1% to 57.4%. For hail the trade-off is partly arithmetic
(positives are 7-9%, so a blank can only come out of the $0 entries; the same holds for the critic's -0.83 across
offices). Thunderstorm Wind and High Wind, where positives are about half and a quarter of the entries, show it is not:
70-79% of an office's rise in blanks came out of its $0 entries. So the same office codes the same kind of event $0 in
one period and blank in another. If the blank is the box (the flood fingerprint says so), the early $0 entries held
unestimated events; if it is not, the drop removes no-damage events by habit. Either way the line between $0 and blank
is a convention of office and period. Settled: the advocate is right that 2007 is a format change; the critic is right
that the mix is not recovered, within the CSV years too.

B. *How far the signal beyond type, office and time carries the us_accidents comparison.* Lennart's reason named
"feed, period, location"; the advocate's comparison left location out. Decisive check (`m2_beyond_subsets`,
`m3_ablation`):

| features | RMSLE 2025 / 2024 / 2023 | R^2 on positives | AUC any damage | Pearson within a storm (storms scored) |
|---|---|---|---|---|
| dummy | 3.820 / 4.010 / 3.872 | | | |
| type + office + time | 2.562 / 2.792 / 2.767 | 0.18 / 0.38 / 0.37 | 0.935-0.945 | 0.27-0.32 (945-1,046) |
| + place (state, county/zone, lat/lon) | 2.592 / 2.800 / 2.797 | 0.15 / 0.39 / 0.36 | 0.932-0.941 | 0.23-0.25 (1,184-1,261) |
| all features, fixed | 2.406 / 2.632 / 2.592 | 0.37 / 0.46 / 0.45 | 0.945-0.954 | 0.31-0.34 (1,193-1,276) |

Place adds nothing over the office. Beyond office, period and place, the rest lowers RMSLE by 0.17-0.21 (about 14% of
the gain), mostly from the hail size and measured gusts (2024: 0.14 of 0.17; the report type adds nothing once the
magnitude is there), and raises the ranking within a storm by 0.08-0.10 on nearly the same storms. The advocate's
within-storm figures compared models scored on different storms and understated that gap. us_accidents' honest split
left log loss 0.48 against a 0.53 prior. So the signal beyond the subsets is real and larger than us_accidents had, and
the label is a dollar estimate the narrowed actor ranks, not a delay code; but the office still carries most of the
score and its code drifts (point A). The facts set the case apart in degree, not in kind. That is a weighing the rules
leave open: the curator's (issue 1).

C. *The amendment's wording.* The advocate's draft ("a mix whose unrecorded part the source flags and the definition
drops") claims a recovery point A refutes. The critic's form fits the data. Proposed, adding the us_accidents fact:
"A mix whose recording follows a reporting unit shipped as a feature may be kept, case by case, with a note giving the
unit's spread and drift and fit approximate, when the task keeps a measured signal beyond the reporting unit, the
period and the place; the source's own 'not recorded' flag is dropped where it is used (Andrej, <date>,
noaa_storm_events_damage)."

**Consistency with precedent**

- LEAK-25: no dataset has kept an unrecovered mix. ghanas_indigenous_intel was retired (rows not located, and `Too
  Small`); caracas_cervical_cancer, account_debt_south_africa and fraud_detection_in_electricity_and_gas_consumption_1m
  were recovered by label-free rules. Keeping needs the amendment; it changes nothing for ghanas.
- us_accidents (`No`, Lennart, 2026-09-23): a similar mechanism; the separating facts are in point B, and the call is
  the curator's (issue 1).
- EG speeds blanked: follows zillow_prize and melbourne_housing_market (located late cells) and this definition's
  `TOR_F_SCALE` drop. thailand_road_accident_register_2019_2022 kept the officer's cause under LEAK-10's case-by-case
  clause because its traced part showed no gain; here the late cells are located and carry a gain (2.504 to 2.538), so
  the two follow the same clause.
- The prediction point: thailand_road_accident_register_2019_2022 reads its register as a severity screen after the
  crash is recorded. The fact that separates them: here the decision (where to send assessors) comes before any damage
  figure exists, and a real-time first-report stream exists to check the inputs against (the Local Storm Reports,
  used in fact 4); the Thai register has no first-report snapshot and its agency acts after the record.
- `SOURCE` dropped: kick, expresso_churn_prediction. History from 2007 on a measured break: aeolus,
  fraud_detection_in_electricity_and_gas_consumption_1m. Gap set to the release lag: mortgage, sberbank (lag to
  release). `rmsle` by context: diamonds, onlinenewspopularity; no decided context case had a mass at zero (the
  Thai register's RMSE fallback is on a count of a few deaths, not nine orders of magnitude). Markers on a `Yes`:
  5g_energy_consumption and others. `Two-Regime Zeros` stays (an exact-zero spike in a continuous amount, unlike the
  Thai death count).
- USE-9 considered: the blind reviewer's other reading, imputing the figures left blank, would put the survey fields
  back as inputs, and its test rows (entered figures) would not stand for the blanks it fills. Not adopted.

</details>

<details><summary>Claim audit</summary>

**Claim audit: noaa_storm_events_damage (claim-auditor, 2026-11-01)**

**Verdict:** ship after changes. 44 claims audited: 29 hold (3 with a caveat), 11 refuted (2 in part; claims 5 and 8 restate 3, 4 and 23), 4 untested. Three refutations are
LEAK-10 (P4, Must) and come from columns that the notes say are first-report values but that the preparer writes after
the event: the EG wind speeds, the tornado `duration_hours` and `hurricane_category`. Each can be fixed in the
definition (blank or drop it). The metric is computable on every fold and its main argument holds on the data. Its
reason says no paper exists, but one does. The task survives the fixes: LightGBM RMSLE goes from 2.504 to 2.556 (mean
of the 3 shipped windows) against a dummy at 3.90.

How I tested: the shipped frame and splits come from the definition (`make_splits`), and the raw 2000-2025 files from
the local copy of the source. Models are untuned LightGBM (400 trees, the builder's parameters)
on the 13 shipped features, with `begin_time` turned into month, hour and days since 2007. All scores are RMSLE through
`data_foundry.v2.metrics.score(spec)` on the 3 shipped windows unless a row says otherwise. To check first-report
values I downloaded the Local Storm Reports (LSR) that NWS offices issue in real time, for all of 2024, from the Iowa
Environmental Mesonet archive. Scripts and outputs stay in the local run folder.

**Claims**

| # | claim | source | test | result | evidence | rule |
|---|---|---|---|---|---|---|
| 1 | Row: one event per county, forecast zone or marine zone, 2007-2025, 54 event types, with a damage entry | task_summary.row | count the rows, EVENT_ID uniqueness and the event types | holds | 1,000,829 rows; 1,225,290 unique EVENT_IDs in the raw 2007-2025 files; 54 types | USE-3 |
| 2 | 73% of the entries are $0 | task_summary.predicted | zero share of the shipped target | holds | 72.99%; test windows 74.2%, 74.0%, 76.3% | - |
| 3 | Known: "the wind speed or hail size reported" | task_summary.known | match the 2024 county Thunderstorm Wind and Hail events to the real-time LSRs (same office, within 15 min, within 10 km) | **refuted for wind**, holds for hail | EG: 12,498 of 13,211 events matched; for 94.4% the first report was "TSTM WND DMG" with no speed, and only 4.4% carried the speed Storm Data shows. MG: 92.7% same speed. Hail: 96.8% matched, 97.9% same size | LEAK-10 |
| 4 | Known: "a hurricane's category" | task_summary.known; Built bullet | how CATEGORY varies within a storm | **refuted** | It is set per zone: 23 of the 95 episodes with a category carry more than one value. Michael 2018 has values 1 to 5 over 14 Florida zones, and Ian 2022 has 1, 2 and 4 although its landfall was Cat 4 (see 25) | LEAK-10, EV-2 |
| 5 | "The features are what the first reports hold" | task_summary.fit_reason | 3, 4 and 23 | **refuted** for three columns | EG speeds, tornado duration and hurricane category | LEAK-10 |
| 6 | Split: a later calendar year; training events certified by the start of that year | task_summary.split; splits_comment | NWSI Sec. 3 text; windows from the definition | holds | "certified ... no later than 60 days after the end of the month" (NWSI 10-1605, Sec. 3); windows 2025/2024/2023, train ends 31 Oct of the year before | SPLIT-6, SPLIT-9 |
| 7 | Changes: the narratives, tornado rating and path, end point, casualties, crop damage and reporter are all dropped | task_summary.changes | list the shipped columns | holds | 13 features, none of these among them | LEAK-10 |
| 8 | "Every column is checked against" the prediction point | notes, prediction-point bullet | 3, 4 and 23 | **refuted** | three columns written after the first report | LEAK-1, LEAK-10 |
| 9 | Scratch numbers: untuned LightGBM, trained on 2007 to Oct 2023, tested on 2024 | notes, prediction-point bullet | read the builder's scratch script | holds, with a caveat | The base (2.560) includes `SOURCE` and `year`, which the shipped frame does not have. The shipped-feature base on 2024 is 2.582 | EV-8 |
| 10 | Target parsing ("10.00K" means $10,000; a value without a letter is dollars) | notes, Target bullet; `_dollars` | list the values without a letter | holds | 133 such values: 124 "0", 1 "0.00" and 8 Illinois/Indiana tornado amounts such as "2000000"; no unparsable value | CLEAN |
| 11 | 18% of the 1,225,290 events are blank and dropped; NWSI Sec. 2.7 p. 11 quote | notes, rows bullet | count; grep the NWSI text | holds | 18.32%; quote on page 11 of NWSI 10-1605 | LEAK-25 |
| 12 | "Flood and Flash Flood have no blanks" | notes, rows bullet; record | count the blanks by year | **refuted (minor)** | 26 blanks, all in 2007 (18 Flood, 8 Flash Flood); none from 2008 on | EV-7 |
| 13 | A $0 mixes "no damage" with "no estimate made" | notes, Anomaly bullet | $0 share among tornado segments rated from damage | holds (new evidence) | 13 of 121 EF4/EF5 segments are at $0, all from an NWS storm survey (for example a 33.7-mile EF5 in Alabama, 2011); 518 of 2,989 EF2+ segments (17.3%) | LEAK-25 |
| 14 | Office $0 share for Thunderstorm Wind: 7% to 91% (10th-90th percentile, 107 offices); 4% to 98% at screening (2018-2024) | notes; record | recompute | holds | 0.073/0.913 (107 offices); 2018-2024: 96 offices, 0.042/0.984 | - |
| 15 | "a model can learn the practice" (`wfo` is a feature) | notes, Anomaly bullet | each office's $0 share in 2007-2021 against 2023-2025 | holds in part | Pearson 0.72 over 82 offices, but 30.5% of them moved by more than 0.2 | SPLIT-20 |
| 16 | History: 70-72% blank in 2000-2005 (69.6% in 2003), 61% in 2006 (PDS to CSV), 7-24% from 2007; Thunderstorm Wind median $5,000 in 2007-2017, $2,000 in 2025 | notes, History bullet | blank share and DATA_SOURCE by year | holds | 0.696-0.722; 2006 0.614 (PDS 48,562 + CSV 7,838 rows); 2007-2025 0.073-0.236; medians as stated | PROV |
| 17 | Dropped under LEAK-10: the EF quote (format doc p. 4), the swath quote (Sec. 46.1, A-68), and RMSE 2.560 to 2.542, 2.457 and 2.496 | notes, Dropped bullet | grep the documents; read the builder's scratch output | holds | format document p. 4; NWSI 10-1605 p. A-68; the numbers are in the scratch output | LEAK-10 |
| 18 | `SOURCE`: "NWS Storm Survey" 23,703 rows, 72% with damage, no missing values, "Unknown" 1,428; 2.565 merged, 2.608 dropped | notes, SOURCE bullet | counts; scratch | holds | 23,703 rows, 0.720; 0 missing; 1,428; 16,043 of the survey rows are tornadoes | LEAK-10 |
| 19 | EG numbers: 229,191 Thunderstorm Wind entries, AUC 0.433, median 52 kt, 62.5% against 10.8% with damage; blanking costs 2.560 to 2.589 | notes, EG bullet | counts; shipped splits | holds | 229,191; 0.625 against 0.108. On the shipped splits, blanking costs 2.504 to 2.538 (mean of 3) | - |
| 20 | EG kept because "which values the preparer set later cannot be located" | notes, EG bullet | the LSR match (3) | **refuted** | The preparer-set values can be located: 94.4% of the matched EG speeds were not in the first report, which was a damage report with no speed. Among those events with damage, the value tracks the dollars (Spearman 0.51). 62% of them are the conventional 50 or 52 kt | LEAK-10 (late-pull clause) |
| 21 | `DATA_SOURCE` is constant from 2007 | notes, identifiers bullet | values by year | holds | CSV only from 2007 | - |
| 22 | `duration_hours`: none negative; the longest are 31-day entries such as Drought | notes, Built bullet | quantiles | holds | 0 negative; maximum 743.98 h, mostly Drought (19,519 rows) | - |
| 23 | Implied by 8: the end time (through `duration_hours`) is known at the first report, while the end point was dropped as the surveyed path | notes, Dropped and Built bullets | correlation with the dropped path length; blank the tornado durations | **refuted** | Spearman(duration, TOR_LENGTH) = 0.83 on tornadoes. NWSI Sec. 47.7: the path "generally excludes sections without surface damage". Blanking the tornado durations raises tornado-row RMSLE 4.51 to 4.67 (2025), 4.60 to 4.83 (2024) and 4.15 to 4.33 (2023), against 0.27 for all dropped survey columns in the builder's scratch | LEAK-10 |
| 24 | `county_zone` has 8,135 codes; zones are 40% of the rows; 37% of the rows lack a begin point | notes | counts | holds | 8,135; 40.46%; 37.29% (92.1% of zone rows, 0.03% of county rows) | - |
| 25 | `hurricane_category` is "the hurricane's Saffir-Simpson category, which the National Hurricane Center issues before landfall" (marked as an inference) | notes, Built bullet | values by zone; Michael's zones; the NWSI tables | **refuted** | Set per zone (4). Michael's Coastal Bay zone is Cat 5 with $6B, which matches NOAA's April 2019 upgrade to Cat 5 at landfall, not the operational Cat 4. NWSI Table A4 pairs each category with "Types of Damage Due to Hurricane/Typhoon Winds". The $0 share is 29% at Cat 1 and 0% at Cat 4-5. Dropping the column: hurricane rows 5.29 to 5.64 (2024, 50 rows), 2.37 to 3.84 (2023, 12 rows) | LEAK-10, EV-6 ("maybe" on the timing) |
| 26 | Duplicates: 0.6% of the rows, mostly zone entries "which the source entered as separate events with their own narratives"; never on both sides of a window | notes, duplicates bullet; info | compare every raw column (event narrative included) except EVENT_ID/EPISODE_ID | **refuted in part** | 6,388 extra copies. 1,072 of them (16.8%) are exact copies of another raw row in every published column, narrative included, in every year and type (248 Thunderstorm Wind, 228 Hail). 0% across the split once `begin_time` is counted | LEAK-19 |
| 27 | One storm system appears as several events; windows keep an episode on one side "except at New Year" | notes, episodes bullet | episodes with rows in both train and test, per split | holds (conservative) | 0 in each of the 3 splits; no episode spans more than 61 days, so with the 2-month gap none can straddle New Year either | SPLIT-13 |
| 28 | The 2024 file of 17 Mar 2025 and of 28 Jul 2026 agree on 99.83% of the 69,545 events in both, so 2025 is settled | notes; builder's probe 13 | the builder's comparison of the two 2024 files | holds | 121 changed (107 blank to value, 6 $0 to positive, 8 positive to another positive). Not said: 907 events (1.3%) were added or removed | LEAK-24 |
| 29 | Licence and C00510 quotes | notes, Licence bullet | search C00510 | holds | "Cite dataset when used as a source"; "may be unverified by the NWS" | EV-4 |
| 30 | Offices and counties recur (99.2%, 100%) | splits_comment | the builder's hidden-groups probe | holds | county_zone 99.2% (98.5-99.7%); wfo and state 100% | SPLIT-13 |
| 31 | Metric `rmsle` is computable on every fold, with `target_transform="log1p"` and no scoring columns | `metric = Metric.from_context` | score a dummy and LightGBM through `score(spec)` on each window | holds | Dummy 3.820/4.010/3.872 and LightGBM 2.388/2.582/2.543, both equal to RMSE on log1p. 24-30% of the LightGBM predictions are negative on the log1p scale; their expm1 is above -1, which sklearn 1.7.2 accepts | MET-2, MET-3 |
| 32 | "no competition or paper on this target was found" | metric reason; record's screening line | one more search (MET-1) | **refuted** | Diaz & Joseph 2019, Weather and Climate Extremes 25:100216 (read): tornado property damage from the Storm Events Database, 1997-2018. A classifier (accuracy 0.821, AUROC 0.872) plus the amount given damage by MSE on log damage; a random 60/20/20 split; tornado length and width among the inputs. Several metrics on a subset task, so no unique original (MET-5), but it scores on the log scale | MET-1, MET-11 |
| 33 | On raw dollars the largest 0.1% of the entries hold "all of" the squared deviation, so RMSE would score a few hurricanes and floods | metric reason | full frame; per test window, the LightGBM's dollar error | holds | 99.96% for the top 0.1% (97.0% for the top 100 rows). Per window, the top 0.1% hold 99.1-99.98% of the model's squared dollar error, and its dollar RMSE beats predicting $0 everywhere by only 0.2%, 3.8% and 0.2% | MET-11 |
| 34 | The damage spans nine orders of magnitude ($0 to $17 billion) | metric reason | smallest and largest positive value | holds | $10 to $17B, 9.23 orders | - |
| 35 | "An estimate of damage is judged relative to its size", hence RMSLE | metric reason | how RMSLE splits its error | untested (a weighing call) | 41-49% of the model's squared log error falls on the true-$0 rows (74-76% of the rows), so RMSLE largely scores whether a figure above $0 was entered. "What to reserve" in the use case is a dollar sum | MET-1, MET-11 |
| 36 | Warning `task_target_value_dominant` accepted as "zero-inflated by nature" | builder's proposed acceptance | 13 | **refuted in part** | Part of the zeros are unestimated damage (13 of 121 EF4/EF5 segments, 17.3% of EF2+) | LEAK-25 |
| 37 | Info: 453 conflicting rows "never both sides of a window" | builder; info | the same begin time puts them on one side | holds | by construction; 0% exact copies across the split | LEAK-20 |
| 38 | Screening: 468,514 events x 51 columns in 2018-2024, 21.4% blank, 75.8% $0, direct injuries 0 for 99.5% | record | recompute | holds | 468,514; 0.2139; 0.7582; 0.9953 | - |
| 39 | Earlier probe: AUC 0.950 for any damage, 0.934 from event type and office alone (train 2018-2022, test 2023-2024) | record | LightGBM classifier on the shipped features | holds | 0.952 (all shipped features) and 0.933 | EV-5 |
| 40 | NWSI Sec. 1 p. 3: "the primary purpose of Storm Data is to accurately describe events" | record | search the directive | holds | NWSI 10-1605, p. 3 | SEL-3 |
| 41 | No other record of this database | record | search the records | holds | only this record names Storm Events or tornadoes | PROV-6 |
| 42 | Rows exist independently of the outcome (implied by "known" and the use case) | implied | $0 share of the event types and magnitudes whose Storm Data entry requires damage | untested ("maybe", see ranked item 4) | Strong Wind 94.2% with damage, Lightning 83.9%, Thunderstorm Wind below 50 kt 97.5% (above: 54.3%). NWSI Sec. 29, 45, 46: entered only when "resulting in a fatality, injury, or damage". These are 3.5-4.0% of the test rows and give 8-10% of the model's gain over the dummy | LEAK-10, LEAK-22, LEAK-37 |
| 43 | Training labels are those known at the refit | implied by the split | 2024 two-download comparison only | untested for older years | Sec. 3 allows recertification for 18 months. The 2012 file was rewritten on 26 Oct 2026 and no older copy was compared | SPLIT-9, LEAK-24 |
| 44 | A StormTrack post says a printed dash became a 0 | record | - | untested | a third-party page, not read | EV-2 |

**Refuted and untested, ranked (validity first, Must first)**

1. **EG wind speeds (P4, LEAK-10 Must; claims 3, 5, 20).** The note keeps them because the late values "cannot be
   located". The LSR match locates them: 94.4% of the 2024 EG speeds were not in the first report, which was a damage
   report with no speed. The preparer then wrote a speed from the damage (NWSI Sec. 46.3), mostly the conventional
   50 or 52 kt (62%), and among events with damage the value tracks the dollars (Spearman 0.51). The check works:
   measured gusts carry over 92.7% of the time and hail sizes 97.9%. LEAK-10's late-pull clause says to blank cells
   that can be located. *Changes:* an input that is not known at the prediction point. *Mildest remedy:* blank
   `magnitude` where `magnitude_type == "EG"` and keep `magnitude_type`, since the report type (damage against
   measured gust) is in the first report (positive share 0.64 against 0.20). Cost on the shipped splits: 2.504 to
   2.538. This settles the builder's draft issue 2 with a measurement; the curator still decides.
2. **Tornado `duration_hours` (P4, LEAK-10 Must; claim 23).** The definition drops the tornado end point and path as
   survey products but keeps the end time inside `duration_hours`. That duration follows the surveyed path (Spearman
   0.83 with the dropped `TOR_LENGTH`; Sec. 47.7). Blanking it costs 0.16-0.23 RMSLE on tornado rows, about two thirds
   of what all the dropped survey columns gave. *Mildest remedy:* blank `duration_hours` for Tornado rows (LEAK-7), or
   keep it with a "Potential leak, kept on purpose" note that gives these numbers.
3. **`hurricane_category` (P4, LEAK-10 Must; claims 4, 25).** It is not the storm's NHC category. It is set per
   zone, it varies within a storm, it is linked to damage (no $0 at Cat 4-5), and Michael's Cat 5 zone matches the
   reanalysis of April 2019 (the timing is circumstantial: "maybe" written after certification, EV-6). It covers 483
   rows (0.05%), and 0 rows in the 2025 window. *Mildest remedy:* drop the column, or keep it with a corrected
   description and a potential-leak note. With 2, the score goes from 2.538 to 2.556.
4. **Outcome-defined rows (P4, LEAK-10 against LEAK-37; claim 42, untested).** Strong Wind, Lightning and sub-severe
   Thunderstorm Wind exist in Storm Data only when they did damage or hurt someone, and are 94-98% positive. In 2024
   the offices also issued 24,673 real-time non-thunderstorm gust reports, most of which never become Storm Data rows.
   This is known at the prediction point only if the first report says damage was seen. The builder's prediction
   point implicitly accepts that (its EG argument), but `task_summary.known` does not say it. *Mildest remedy:* write
   into `known` and the prediction-point bullet that the first report says whether damage was seen (a damage report
   against a measured gust), with the 3.5-4.0% share. The curator decides whether that is the moment.
5. **The warning's "zero-inflated by nature" (P4/P5, LEAK-25 Must; claim 36).** Zeros on EF4/EF5 tornadoes prove
   that some $0 entries are unestimated damage. *Changes:* the acceptance reason, and it adds evidence to the
   builder's draft issue 1 (exception or amendment of LEAK-25). *Mildest remedy:* accept the warning with "part of the
   zeros are unestimated damage (13 of 121 EF4/EF5 segments, 17.3% of EF2+ at $0); LEAK-25 question in REVIEW".
6. **The metric reason (P6, MET-1/MET-11 Must; claim 32).** "No paper found" is wrong: Diaz & Joseph 2019 exists.
   It does not overturn `rmsle`: it reports several metrics on a tornado-only, randomly split task (MET-5), and it
   scores on the log scale, which supports the context call. *Mildest remedy:* name the paper in the reason. Claim 35
   (RMSLE against the use case's "what to reserve") stays a weighing call for the curator: about 45% of RMSLE is
   spent on whether a $0 was entered.
7. **Exact copies (P7, LEAK-19 Should; claim 26).** 1,072 rows are identical to another row in every published
   column, narrative included: double entries, not separate events. They never cross the split, but they weigh some
   rows twice. *Mildest remedy:* drop them (LEAK-19), or correct the note.
8. **Minor wording (P7/EV).** "Flood and Flash Flood have no blanks": 26 blanks, all in 2007 (claim 12). The scratch
   base includes `SOURCE` and `year`, so give the shipped-feature base of 2.582 (claim 9, EV-8). For "a model can
   learn the practice", add that 30% of offices shifted by more than 0.2 (claim 15). Claim 28 leaves out the 1.3% of
   events added or removed between the two 2024 files.
9. **Untested:** whether training labels moved for older years (claim 43; 2012 rewritten in Oct 2026, no older copy
   compared); the StormTrack post (claim 44).

Sources read: NWSI 10-1605, the bulk CSV format document, C00510, Diaz & Joseph 2019
(<https://arxiv.org/abs/1807.03456>), NOAA's April 2019 Michael upgrade (news reports, e.g.
<https://www.wuga.org/local-news/2019-04-24/hurricane-michael-upgraded-to-a-category-5-at-time-of-u-s-landfall>),
and IEM's LSR archive (<https://mesonet.agron.iastate.edu/cgi-bin/request/gis/lsr.py>, 2024).

</details>

<details><summary>Column audit</summary>

**Column audit (column-auditor, 2026-11-01): noaa_storm_events_damage**

**Verdict: ship after changes.** Most of the cleaning is sound, and the builder's drops (narratives, EF rating, path, end point, casualties, crop damage, `SOURCE`) are right. The column-by-column pass finds three columns that carry survey or post-event content the definition says it removed:
1. `duration_hours` on tornado rows is the length of the surveyed path.
2. `hurricane_category` is a per-zone value, and at least one value was written after the event.
3. The estimated (EG) wind speeds get new evidence that favours blanking them.

On the quality side, `magnitude` mixes two units in one column.

Prediction point checked against: "a storm has passed and its events are logged from the first reports (type, place, begin and end time, the reported wind speed or hail size), before any damage survey, claim or damage estimate" (first `curation_comments` bullet).

Evidence comes from the definition's own frame (1,000,829 rows, loaded through `dataset_io.from_definition`), with the raw columns joined back by row index. Model numbers come from untuned LightGBM, the builder's setup without `SOURCE`: 400 trees, trained on 2007 to October 2023, tested on 2024, RMSE on log1p, one window. On the shipped features the RMSE is 2.6007 overall.

How much these numbers move by chance: a lossless re-encoding (run F) moved the overall RMSE by 0.012, tornado rows (1,774) by 0.05 and hurricane rows (50) by 0.20.

Scripts and outputs stay in the local run folder.

**Column table**

| Column | Meaning (codebook) | Known at prediction? | Dtype and cleaning | Verdict | Rule |
|---|---|---|---|---|---|
| `log1p_property_damage_usd` (target) | `DAMAGE_PROPERTY`, "the estimated amount of damage to property" (format doc p. 4), parsed from "10.00K" | the outcome | float. Parse checked: K 991,979, M 8,654, B 63, and 133 values without a letter, read as dollars ("0", "2000000"); no value fails to parse. Blanks dropped. | fine as parsed. $0 mixes "no damage" with "not estimated" (builder's issue 1; not repeated here) | CLEAN-15; LEAK-25 elsewhere |
| `event_type` | one of the 55 permitted Storm Data events (NWSI Table 1) | yes, as the report's type. Two caveats: (1) some types exist only when there was damage or a casualty: Strong Wind (94.2% of rows with damage), Lightning (83.9%), Dust Devil, and Thunderstorm Wind under 50 kt (96-98%); (2) tornado against thunderstorm wind is often settled by the survey (Sec. 47.6) | category, 54 levels | fine. Selection by impact is part of what a first report says (a report of damage); note only | USE-3 |
| `state` | state name, or marine area ("GULF OF MEXICO", "LAKE MICHIGAN") | yes | category, 69 levels, no variant spellings | fine | |
| `cz_type` | C county, Z zone. The doc lists M for marine, but the files code marine zones as Z | yes | category: C 595,895, Z 404,934 | fine | |
| `county_zone` | state FIPS + type + county or zone number | yes | category, 8,135 levels. 294 codes carry more than one name after case-folding (renamed or renumbered zones; 3,377 rows, 0.34%, are under a non-majority name, e.g. `01Z066` DALE 26 rows against BALDWIN COASTAL 1). 303 codes (1,567 rows) occur first in 2023-2025 | fine. A meaningful identifier processed into a place code; the renumbering is minor | CLEAN-3, CLEAN-14 |
| `wfo` | the forecast office whose area the event is in | yes | category, 123 offices, the same set in every period | fine (also carries office practice on $0) | |
| `magnitude` | knots for wind events, inches for hail (doc p. 4) | measured gusts (MG, MS) and hail sizes: yes. Estimated speeds (EG, ES): set by the preparer "based on observed structural or tree damage" (Sec. 46.3), with Table A7, "Estimating Wind Speed from Damage" | float64. **Two units in one column** (knots and inches). 22 Thunderstorm Wind entries of 1-10 kt and 2 Strong Wind entries of 0 kt are impossible for a wind entered because it did damage | EG part: leak, curator's call, lean blank (problem 3). Units: cleaning problem (problem 5). Impossible values: cleaning problem (problem 6) | LEAK-10, LEAK-2; CLEAN-21; CLEAN-11 |
| `magnitude_type` | EG, ES, MG, MS (doc p. 4); blank for hail and non-wind events | yes: whether a wind report is a measured gust or a damage-based estimate is in the first report | category | fine (the builder's reasoning holds) | LEAK-10 |
| `flood_cause` | "reported or estimated cause of the flood" | yes | category, 7 values; filled for 100% of Flood and Flash Flood, 83.5% of Debris Flow | fine | |
| `hurricane_category` | `CATEGORY`, which the doc calls unknown. In the data it is filled for Hurricane (Typhoon) rows only, values 1-5, and **varies by zone within one storm** | **no, at least in part**: it is a per-zone value, and Michael's Cat 5 (2018) is the NHC upgrade of April 2019 | float64, ordinal kept numeric (dtype fine) | leak, weak in effect, strong in mechanism (problem 2) | LEAK-10, LEAK-6 |
| `begin_lat`, `begin_lon` | "begin point of the event or damage path" | approximately, yes. For surveyed tornadoes it is the start of the surveyed path, but the place is known from the first reports | float. Ranges are valid (American Samoa lat < 0, Guam lon > 0; no CONUS row off the map; no 0/0). Missing for 91.7% of zone rows, driven by event type and not by damage (land zone types never have a point, marine types always do) | fine | CLEAN-10, CLEAN-11 |
| `begin_time` | built from `BEGIN_YEARMONTH`, `BEGIN_DAY`, `BEGIN_TIME`; local standard time | yes | datetime. Local clocks from HST-10 to AST-4, with 327 rows tagged with a daylight-time zone; the hour is local, as documented | fine | CLEAN-12 |
| `duration_hours` | end minus begin. NWSI: Thunderstorm Wind "when damage first occurred ... when damage ended"; Tornado "when the sub-cloud vortex first contacted the ground ... lost contact"; Flood "when flood waters receded" | Most types: yes. **Tornado: no**; it is the surveyed path (68% of tornado rows have `SOURCE` "NWS Storm Survey", 80% in 2024-2025). Flood and Wildfire: the end comes days to weeks later (a question) | float, 0 to 744 h, none negative | Tornado rows: leak (problem 1). Flood and Wildfire: question (problem 4) | LEAK-10, LEAK-2, LEAK-7; USE-3 |

**Problems, ranked (P4 first, then P7)**

**1. LEAK-10 / LEAK-2 (Must): `duration_hours` on tornado rows carries the dropped surveyed path.** Strength: moderate, about the size of the block the definition dropped. Remedy: blank `duration_hours` for Tornado rows.
- **The sibling sweep.** The definition drops `TOR_LENGTH` and the end point as "the path from the damage survey". It keeps the end *time* of the same path. NWSI Sec. 47 defines a tornado's begin and end as ground contact of the vortex. 16,043 of the 23,620 tornado rows (68%; 80% in both 2024 and 2025) have `SOURCE` "NWS Storm Survey".
- **How closely duration tracks the dropped columns.** Spearman with `TOR_LENGTH` is 0.831, and with the EF rating 0.461. The median duration rises with the rating: EF0 2 min, EF1 5, EF2 9, EF3 15, EF4 19.5, EF5 20. Among tornado rows with damage, duration ranks the dollars at 0.434, close to `TOR_LENGTH`'s 0.466.
- **Measured.** With duration in the model, adding `TOR_LENGTH` moves tornado RMSE only from 4.629 to 4.618: the path is already there. Blanking duration on tornado rows raises tornado RMSE to 4.894 (+0.26, five times the noise), and overall from 2.601 to 2.622. For scale, the builder's whole block (rating, path, end point) is worth 4.429 to 4.156 on the same rows.
- **The mildest fix that leaves no marker.** Blank by event type (every tornado row), not by `SOURCE`. Blanking only the surveyed rows would make a missing duration the survey marker that the `SOURCE` bullet already rejects. `begin_time` stays.

**2. LEAK-10 / LEAK-6 (Must): `hurricane_category` is a per-zone intensity, at least partly written after the event.** Strength: the effect cannot be measured (50 hurricane rows in the 2024 test; dropping the column moves their RMSE from 5.56 to 5.73, inside the noise), but the mechanism is confirmed by one case. Remedy: drop the column; the event type still separates Hurricane from Tropical Storm. The alternative is a join of NHC's operational landfall category per storm (CLEAN-19), more work for 483 rows. Either way, the `Built:` bullet's reading ("the hurricane's Saffir-Simpson category, which the National Hurricane Center issues before landfall") does not hold and should be corrected.
- **The data contradicts that reading.** Of the 61 hurricane episodes with two or more zones, 22 have more than one category. Within those episodes, the category ranks the zone's damage: Spearman 0.504 on episode-demeaned values, 212 rows.
- **Hurricane Michael** (episode 130185, 14 Tallahassee-office zones) runs from category 1 to 5. Coastal Bay is 5 ($6.0B). NHC's operational landfall intensity was Category 4; the Category 5 is the post-storm upgrade of April 2019 ([WSLS](https://www.wsls.com/weather/hurricane-michael-upgraded-to-a-category-5-upon-post-storm-analysis), [Air & Space Forces](https://www.airandspaceforces.com/noaa-upgrades-hurricane-michael-to-category-5-the-4th-in-us-history/); secondary sources). That is six months after the event and after the 60-day certification. NWSI's own Saffir-Simpson table (Sec. 25.3) pairs each category with "Types of Damage Due to Hurricane/Typhoon Winds", so a preparer can set a zone's category from damage, as with Table A7.
- **Strength of the evidence.** Circumstantial but strong. Under LEAK-6, a confirmed late value goes even when small.

**3. LEAK-10 clause 2 / LEAK-2 (Must, a case-by-case call for the curator): EG wind speeds.** This is the builder's issue 2, with new evidence that leans towards blanking. Remedy: blank `magnitude` where `magnitude_type` is EG (keep `magnitude_type`). Without `SOURCE` this costs 2.601 to 2.654 overall and 2.767 to 2.931 on EG rows (builder, with `SOURCE`: 2.560 to 2.589). Otherwise keep the note, but then the note should cite the survey measurement below and explain why clause 2 does not apply.
- **For blanking: the same mechanism as the EF rating.** Table A7 is titled "Estimating Wind Speed from Damage" and refers to the EF-Scale damage indicators 27 and 28. That is the mechanism the definition cites to drop `TOR_F_SCALE`; treat like cases alike (LEAK-2).
- **For blanking: the traceable late part carries a gain.** By the definition's own prediction point ("before any damage survey"), EG values set by a survey are late. There are 6,114 Thunderstorm Wind EG entries from "NWS Storm Survey": median 65 kt, 55% at 65 kt or more, and 60% of all EG entries at 80 kt or more. Blanking just those raises their RMSE from 3.246 to 3.448 (533 test rows, against noise of about 0.04 on them). They cannot be blanked alone, because an EG with no value would become the survey marker. Clause 2 then reads: late cells that cannot be located without a marker "go when they may carry a gain and stay with a note only when the part that can be traced shows none".
- **For blanking: the builder's ROC AUC figure measures the wrong thing.** The figure (0.433, any damage) comes from the sub-50-kt damage entries (96-98% with damage) and the 50 kt default (90,626 entries). Among entries with damage, the EG speed ranks the dollars at Spearman 0.462 (143,238 rows). The median positive damage rises from $3,000 at 50 kt to $75,000 at 78 kt and above.
- **For keeping (the steelman).** Measured gusts (MG) rank the dollars among damaged entries at the same Spearman, 0.462 (3,501 rows), with a similar rise ($5,000 to $61,000). So the EG gradient is no steeper than a physical measurement's. The actor reading a first report sees the damage description the estimate is made from.
- **My lean is to blank.** The rule's wording and the EF precedent decide it. With problems 1 and 2 also applied, the overall RMSE is 2.668.

**4. USE-3 (question): "begin and end time" are not both first-report facts for long events.** Strength: weak. Remedy: keep the column. Reword the prediction point to "once the event has ended and is logged from the first reports", and add the flood and wildfire numbers to a note. The alternative, blanking the duration of these types, costs little and is not needed on this evidence. A related, unsettled reading: the AI assessment for `nfip_redacted_flood_claims` treats the adjuster's flood duration as a post-inspection field (a different source: the adjuster at a building).
- A Flood's end is "when flood waters receded"; 20.2% of the 48,513 floods last more than 72 h (90th percentile 218 h). 48.2% of wildfires last more than 72 h (90th percentile 529 h). Damage assessments can start before such an end.
- Measured: blanking duration for Flood and Wildfire rows moves Flood RMSE from 3.853 to 3.884 (2,472 rows) and Wildfire from 5.646 to 5.769 (292 rows, noisy).

**5. CLEAN-21 (Should): `magnitude` holds knots for wind and inches for hail in one column.** Remedy: split into `wind_speed_kt` (wind event types) and `hail_size_in` (Hail, Marine Hail), each missing elsewhere. The split is lossless, cheap and safe: LightGBM RMSE 2.6125 against 2.6007, inside the noise. A model without interactions otherwise reads 1.75-inch hail and a 50-knot gust on one axis. `magnitude_type` stays for the wind column.

**6. CLEAN-11 (Should): impossible wind values.** 22 Thunderstorm Wind entries of 1-10 kt and 2 Strong Wind entries of 0 kt (a wind entered because it did damage cannot be 0-10 kt) should become missing; the rows stay. Tiny. The 99 High Wind values above 100 kt, up to 174 kt, are unusual (mountain-top stations) and stay.

**Claims checked**
- **Corrected:** the `Built:` bullet's reading of `hurricane_category` (problem 2). The prediction point's "begin and end time" from first reports does not hold for tornadoes (problem 1) or long floods and wildfires (problem 4). The EG bullet's "ranks the damage below chance" is true for any damage but not for the amount that is scored (problem 3).
- **Hold:** duration none negative, longest 744 h; zone events lack points (37% of rows); `CATEGORY` filled for Hurricane rows only (483 in the frame, 560 in the raw files); flood causes fully filled; `DATA_SOURCE` dropped; the identifier and copy drops in the "Dropped as identifiers or copies" bullet.
- **Holds with a footnote:** `county_zone` as "one code per county, forecast zone or marine zone" (a few renumbered zones; 0.34% of rows).

</details>

<details><summary>Split audit</summary>

**Split audit (split-auditor, 2026-11-01): noaa_storm_events_damage**

**Verdict: right with notes.** The regime, the windows, the expanding train side and the 2007 start are right and backed by measurements. One Should departure: the 2-month gap is set from the NWS certification deadline, but the actors in the use case read NCEI's public releases, which come about 2.5 months after the end of a month. At a refit on 1 January, October's events are not public yet. Two claims need rewording. None of this changes the regime.

```text
Verdict: right with notes.
Validity: SPLIT-1, SPLIT-3, USE-10 hold (temporal; known places: county_zone 99.2% of test rows seen, office and state 100%);
  SPLIT-6 holds; SPLIT-9 holds (no measurable shortcut: 0 episodes cross the cut, later releases change 0-0.17% of labels);
  SPLIT-10 departure: gap 2 months against a public label delay of about 2.5 months (fix: gap 3, or restate the refit date);
  SPLIT-11, SPLIT-14 (train 82.4-94.0%), SPLIT-17 hold; SPLIT-13 holds (known offices and counties are the task);
  SPLIT-20 holds (2007 break measured; drift within 2007-2025 is gradual, no break).
For the curator: gap 2 or 3 months (a fact about the release lag plus a small call on the refit date).
```

**What was checked, with numbers** (frame from the definition, rebuilt from the raw files)

| Check | Finding | Rule |
|---|---|---|
| Regime from the use case | The actor estimates the damage of new events in counties and offices it has seen before, and the events arrive over time, so the split is temporal with known entities. county_zone: 99.2% of test rows seen in train (98.5-99.7%); wfo and state: 100%. The new-entity key `(all but county_zone)` matches 0% of test rows. A grouped split (new county) would test a question nobody asks. | SPLIT-1, SPLIT-3, USE-10, SPLIT-13: hold |
| Time column | `begin_time` is the event's start in local standard time. The data month is the begin month: only 1 of 1,225,290 raw rows has an end month that differs (NWSI Sec. 2.3.2: an event that spans months is entered once per month). So a cut on `begin_time` is a cut on the month whose certification brings the label. | holds |
| Windows and sizes | Calendar years 2025, 2024 and 2023, newest first. Test: 55,961 / 54,755 / 57,763 rows (zero share 0.742 / 0.740 / 0.763). Train: 940,520 / 886,742 / 824,900 rows (94.0 / 88.6 / 82.4%). Train ends on 31 Oct of the year before. My own date masks reproduce the shipped index sets exactly. | SPLIT-11, SPLIT-14, SPLIT-17: hold |
| Episodes across the cut | 0 of 167,629 episodes span two months, so none crosses a window boundary, even without a gap (0 test rows in a shared episode in each window). | holds; a claim to reword (note 1) |
| Gap against the label delay | NWSI Sec. 3: certified "no later than 60 days after the end of the month". NCEI's own metadata (C00510): "updated monthly with up to a 120 day delay possible". Measured on archived releases: the 2025 file of 18 Aug 2025 holds Jan-May 2025, with May 83% present (79 days after its end) and June absent. The file of 16 Jan 2026 holds Jan-Oct 2025, all of October present (77 days), November absent. The file of 26 Oct 2026 holds Jan-Jul 2026, August absent (56 days). The public listing of 25 Dec 2025 and 5 Jan 2026 shows the 2025 file of 16 Dec 2025 (not archived). By the measured lag of 75-80 days, that file holds events through September. | SPLIT-10: departure (problem 1) |
| Training labels not known at the prediction point | No shortcut: no episode crosses the cut. Labels barely move in later releases: 0 of 64,921 damage values of Jan-Oct 2025 differ between the files of 16 Jan 2026 and 19 Aug 2026, and the builder found 0.17% of 2024 values changed between Mar 2025 and Jul 2026. 417 events of Jan and Jul 2025 were added after 16 Jan 2026, all from three offices (PAH 297, FFC 119, MFL 1), 88.5% at $0. NWSI Sec. 3 allows recertification for 18 months; these numbers bound the effect. | SPLIT-9: holds |
| Training history | Blank share 71.8 / 71.2 / 70.3 / 69.5 / 71.8 / 72.2% in 2000-2005, 61.4% in 2006, 7.3% in 2007 (measured). The 2007 start sits on that break. Inside 2007-2025 the drift is gradual. The blank share rises from 7.3% (2007) to 15-21% (2009-2021) and 22-24% (2022-2025). The median positive damage falls from $10,000 (2007-2011) to $5,000 (2018-2024) and $3,000 (2025). The EG share of Thunderstorm Wind falls from 0.925 to 0.789. 46-53 event types and 122-123 offices every year. | SPLIT-20: holds (note 3) |
| Season-shaped test window | Full calendar years, so every window covers the spring tornadoes, summer convection, the autumn hurricanes and the winter storms. 2025 is light on tropical damage: 5 tropical rows against 222 in 2023 and 587 in 2024, and a total of $4.5B against $16.6B and $15.7B. That is one of three windows, and it is already a full year, so there is nothing to widen. | SPLIT-20: holds |
| Copies and near copies | Exact copies across the split: 0% with the datetime, 8.3% without it. Near copies: 4.6% of test rows. `(all but begin_time)`: 17.0% of test rows share all 12 other columns with a training row (the same county, type and magnitude at another time). These are separate events, natural repeats (LEAK-18). The 0.6% duplicate rows share a begin time, so they always land on one side. | holds |

**Alternatives fitted** (untuned LightGBM, 400 trees, the shipped 13 features with `begin_time` as year fraction, month and hour; RMSE on the log1p target)

| Split | 2025 | 2024 | 2023 |
|---|---|---|---|
| shipped: gap 2 months | 2.4030 | 2.5803 | 2.5404 |
| gap 0 | 2.3981 | 2.5810 | 2.5409 |
| gap 3 months (train through September) | 2.4350 | 2.5994 | 2.5607 |
| gap 2 minus as many random Jan-Sep rows as October holds (2 seeds) | 2.3969, 2.3902 | 2.5809, 2.5840 | |
| gap 2 / gap 3, without the time feature | 2.8082 / 2.8008 | 2.9515 / 2.9533 | |
| reference only: random thirds of 2023-2025 held out, trained on all other rows | 2.24, 2.24, 2.22 (R^2 0.670-0.674, against 0.570-0.606 by window) | | |

How to read these numbers:

* The random split overrates the models by 0.16-0.36 RMSE. That fits the use case: offices change their practice over time. An office's $0 share among Thunderstorm Wind entries in 2024 predicts its 2025 share closely (r 0.958, 76 offices), but its 2007-2016 share predicts it much less well (r 0.575). 17 of 84 offices moved by more than 30 points between 2015-17 and 2022-24. This is why the time feature alone is worth 0.37-0.41 RMSE, and why the temporal split is the right test.
* Gap 3 costs 0.019-0.032 RMSE. Removing as many random rows changes the score by -0.013 to +0.004, and without the time feature gap 3 costs nothing (-0.007, +0.002). So the cost is an edge effect: the time feature leans on the newest training month. October itself carries no extra information. It is no argument either way: the gap follows the label delay, not the score (P4 over P6; SPLIT-21 on comparisons over a few windows).

**Problems, ranked**

1. **SPLIT-10 (Should; applies SPLIT-9): the gap is shorter than the actor's label delay by one month.**
   * The problem: `splits_comment` sets the gap from the 60-day certification deadline: "so at a refit on 1 January the events of November and December are not yet in". But the actors named in the use case (a state emergency manager, an insurer's catastrophe desk) get Storm Data from NCEI's monthly releases. On 1 January 2026 the public 2025 file was the one of 16 December 2025. By the lag measured on three releases (75-80 days after the end of a month; a month 47-56 days old is absent), that file held events through September. October 2025 first appears complete in the file of 16 January 2026.
   * The effect: each training side holds one month the actor would not have: 1,401 / 1,743 / 1,705 October rows (0.15-0.21% of train). There is no shortcut, so SPLIT-9 holds and this is the diffuse rest under SPLIT-10 (principles.md, Tensions: unmatured training labels).
   * The same claim recurs in `task_summary.split`: "with every event certified by the start of that year". Certification is not always on time. May 2025 was 83% present 79 days after its end, and 417 Jan and Jul 2025 events came after 16 Jan 2026.
   * The precedent it follows: mortgage and sberbank lag official series to their release (register, 2026-10-21), which is the same logic applied to labels.
   * The mildest remedy, two equivalent ways out for the curator:
     * (a) `gap=3, gap_unit="months"`: train through September. The splits_comment cites C00510 ("up to a 120 day delay possible") and the measured release lag.
     * (b) Keep `gap=2` and restate the refit as made at the mid-January release, which holds all of October (16 Jan 2026 file: 1,703 of 1,703 October 2025 events). The first two weeks of each test year are then predicted by a model refit after them.

   Either way, reword `task_summary.split` to "every event published by the refit". The score difference (+0.02-0.03 for gap 3) is an artifact and should not decide.

**Notes (no change to the split; wording or documentation)**

1. Curation note "they share a date, so the yearly windows keep an episode on one side except at New Year": the exception does not occur. 0 of 167,629 episodes span two months, so none crosses New Year. Suggested wording: "no episode spans two months (0 of 167,629), so none crosses a window boundary".
2. The Anomaly note says a model can learn office practice from `wfo`. It should add that the practice drifts: r 0.958 from 2024 to 2025 against 0.575 from 2007-2016 to 2025, and 17 of 84 offices moved by more than 30 points. This is what the temporal split tests, and it is why the newest training months matter. One line in the History or Anomaly bullet.
3. History bullet: "7-24% from 2007 on" is a trend, not a range (7.3% in 2007, 22-24% in 2022-2025). Since blank rows are dropped, the shipped rows change composition over time. Worth stating with the existing note on the falling positive median.
4. SPLIT-12: the yearly refit is our choice, since the source names no horizon and NCEI releases monthly. It is defensible for the full season in each window. The cost: late-year test events are predicted by a model 14 months stale (15 with gap 3), which an actor refitting monthly would not face. The cost is the same for every method, so no change. The splits_comment could say the cadence is ours.
5. "2025 ... is settled (leak probe 13)": holds and is strengthened (0 of 64,921 Jan-Oct 2025 values changed between Jan and Aug 2026). Nov-Dec 2025 cannot be compared, since they are absent from the January file. The 18-month recertification window (NWSI Sec. 3) stays open until mid-2027 for December 2025.

**Claims checked**

| Claim | Status |
|---|---|
| splits_comment: certification within 60 days (NWSI Sec. 3) | the quote holds (NWSI 10-1605, Sec. 3) |
| splits_comment: "at a refit on 1 January the events of November and December are not yet in" | holds for certification, understates the public delay (problem 1) |
| splits_comment: offices and counties recur (SPLIT-13) | holds (99.2% / 100% / 100%) |
| splits_comment: full calendar years for seasonality | holds |
| task_summary.split: "every event certified by the start of that year" | partly refuted (problem 1) |
| Note: an episode stays on one side "except at New Year" | holds, overcautious (note 1) |
| Note: duplicate rows never on both sides | holds (same begin time) |
| Note: History, 70-72% blank 2000-2005, 61% 2006, 7-24% from 2007 | holds (measured: 69.5-72.2%, 61.4%, 7.3-23.6%) |
| Note: 2025 settled | holds (note 5) |
| Builder: train 825k-941k, test 55k-58k | holds (824,900-940,520; 54,755-57,763) |

**Not checked**

* Whether the features the actor sees at the prediction point (preliminary storm reports) match the certified Storm Data values the test rows carry. For example, 76 event types changed in 2024 between releases. That is the column auditor's and the domain practitioner's question.
* Tuned models under the alternatives.

Evidence files stay in the local run folder: the windows, history and episodes; the archived releases against the final file (the 2025 files of 18 Aug 2025 and 16 Jan 2026, and the 2026 file of 26 Oct 2026); the episode spans and the 2000-2007 blank shares; the fits; the office practice; the scripts.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: noaa_storm_events_damage** (2026-11-01). I take the role of a state emergency-management officer ranking a storm's counties for damage-assessment teams; the catastrophe-desk analyst gets a second voice. The numbers come from my scratch runs: one window (train 2007 to October 2023, test 2024), untuned LightGBM with 400 trees, and the features as shipped.

**Verdict**

- **Fit: approximate, as the definition says.** For the emergency manager's triage, the label is a rough measure of the right quantity (which counties of a storm took the most damage). It is recorded at a finer unit than the decision, and its zeros carry office habits. For the insurer's reserve it is a different quantity (USE-5, last sentence), so that half of the use case should go.
- **Metric: partly.** RMSLE's log scale suits triage by orders of magnitude, and on 2024 it picks the same best model as triage within a storm does. However, 69% of its squared error sits at the zero/positive call, which is mostly whether the office entered a figure. It is also scored per row, while I decide per county and storm (MET-1). I would score within the storm, by `EPISODE_ID`. I would not switch to the insurance siblings' `normalized_gini`, which picks the wrong model here.

**How the decision is made today**

- **Emergency manager.** Local emergency managers run the Initial Damage Assessment. They work from 911 data and self-reports to "determine impact areas to prioritize". The state then verifies those numbers and requests a joint Preliminary Damage Assessment with FEMA (Florida SERT; Missouri SEMA; 44 CFR 206.33). The request is weighed against FEMA's per-capita indicator for public infrastructure cost and against counts of destroyed and major-damage homes.
  - The NWS dollar figure arrives with Storm Data, which is certified up to 60 days after the end of the month (NWSI 10-1605, Sec. 3).
  - Its estimates "can be obtained from emergency managers ... utility companies, and newspaper articles" (Sec. 2.7, p. 12). So part of the label is my own reports, coming back to me.
- **Catastrophe desk.** In the first days the desk reads vendor event estimates (KCC, CoreLogic, Gallagher Re). These are built from hazard footprints and storm-report counts laid over exposure. The desk then reads its own first notices of loss.
  - Until the 2021 revision, the directive referred preparers to Verisk PCS for damage amounts ("Section 2.7 – Removed reference to using Verisk PCS for damage amounts"). For large events before 2021, the label is partly the industry estimate the desk already had.
- **Published uses of these figures.** The ones I found are for planning, not for response:
  - Diaz & Joseph (arXiv 1807.03456) fit a hurdle model on Storm Data tornadoes "for science-informed tornado disaster planning".
  - FEMA's National Risk Index takes its historic losses from SHELDUS and divides them by exposed building value.

**1. My inputs at the moment of the prediction**

- **What I have.** These match the definition's "known" list:
  - the event type for hail, wind, flood and winter weather (the type on the Local Storm Report);
  - the state, county or zone, and office;
  - the begin time, and the end time once the storm has passed;
  - the reported magnitude, and whether it was measured or estimated (LSRs carry that designation);
  - the flood cause, and a hurricane's category.

  I would also have the reporter (the LSR's source field). The definition drops it for the "NWS Storm Survey" marker, which raised RMSE from 2.560 to 2.608. Either the drop or the merge is a small effect.
- **What I would not have.**
  - **A Tornado type that a survey set.** NWSI 10-1605 Sec. 47.6 types an event as a tornado "if the type or intensity of the structural and vegetative damage ... could only have been tornadic". 67.9% of the 23,620 tornado rows from 2007 to 2025 carry SOURCE "NWS Storm Survey". For those rows the begin point and the duration also come from the surveyed path. Tornado rows are 2.4% of the rows but 10.9% of 2024's dollars.
  - **The row itself.** A Storm Data entry is one event in one county segment, assembled weeks later. What I would feed a model in practice is the LSR stream: several unverified reports per county.
    - Storm Data also selects on damage. Sub-severe wind is entered only with "fatalities, injuries, or serious property damage" (Sec. 46, p. A-68).
    - Measured: Thunderstorm Wind with an EG speed below 50 kt is $0 in 2.3% of 10,604 entries, against 39.2% at 50 kt or more.
    - A first report of damage tells me the same thing, so this is a gap in how the input is shaped, not a leak.
  - **The EG wind speeds.** The definition keeps these on purpose. I accept that: my first report is itself a damage report.
- **What is missing although I would always have it:**
  - **Exposure:** population, housing units and building value of the county; for the insurer, its own policies inside the footprint. The NRI's historic loss ratio is loss over exposed building value. Without exposure, the model can learn dollars per place only as a category over 8,135 county or zone codes.
  - **The size of the storm:** how many reports and counties the episode touched.
  - **The LSR remarks**, such as "roof off" or "trees on house", which are the first description of damage. The Storm Data narratives are rightly dropped because they are written later. The builder's two flags read off the narratives moved RMSE from 2.560 to 2.496, so the earlier remarks would carry real signal.
  - **Radar hail swaths and rotation tracks, and power outages per county.**

**2. Is the target what I act on?**

- **As the emergency manager: a rough proxy.** I act on where damage is largest within the storm, in orders of magnitude. Later I act on public-infrastructure cost and damaged-home counts, which the label does not hold. The $0 mixes "no damage" with "no estimate":
  - Wind speeds estimated from observed damage (EG, 50 kt or more) are $0 in 39.2% of 218,587 entries.
  - Hail of 1 to 1.75 in is $0 in 93.3% of entries; hail of 2.75 in or larger still in 58.8%.
  - Offices range from 7% to 91% $0 (the definition's decision table).
- **As the insurer: a different quantity.**
  - **Scale.** Storm Data's 2024 total property damage is $15.7 billion, against $182.7 billion for NCEI's 27 billion-dollar events of 2024. The scopes differ (the NCEI total includes uninsured and infrastructure losses), but the gap is about 12-fold.
  - **Hail.** Hail drives convective-storm claims (Triple-I: up to 80% of severe-storm claims; CoreLogic: 95% of the June 2023 outbreak). Yet hail is 11.1% of the 2024 rows and only 1.4% of their dollars.
  - **Convective total.** Hail, thunderstorm wind and tornado together come to $2.4 billion in 2024. Industry insured convective losses are about $50 to 60 billion a year (Swiss Re 2023; Triple-I 2025).
  - **Undercount in claims data.** In Georgia, insurance claims logged 136 times the lightning incidents and more than twice the dollars of Storm Data (Stallins 2002).

  A model of this label says nothing about the desk's hail book. This is USE-5's "a label ... found to be another quantity than the one the actor acts on" (compare the us_accidents decision of 2026-09-23: a delay code does not serve the first responder).
- **Form.** A number in dollars is fine. What I would consume is the ranking of a storm's counties.

**3. Does one row match one decision, and is the test what I face?**

- **The unit is finer than my decision.** I decide per county and storm; a row is one event of one type in one county segment. In 2024, 25.4% of the 33,350 county-storms (`EPISODE_ID` x county or zone) have more than one row. They hold 54.6% of the rows and 44% of the dollars.
- **A fifth of the rows have no assessment decision.** 19.8% of the 2024 rows are hazards nobody sends an assessor for: marine types, drought, heat, cold, fog, rip current, funnel cloud, waterspout, high surf. They are 99.7% $0 and hold 0.07% of the dollars. They make the task look easier, and the metric rewards predicting zero on them.
- **Dollars are concentrated.** In 2024 the top 0.1% of rows (55) hold 76.7% of the dollars, and the top 1% hold 97.4%. By type: hurricanes 33.7%, flash floods 20.0%, tropical storms 12.1%, tornadoes 10.9%.
- **The test fits.** It is the next calendar year in counties seen before, with a two-month gap for certification. That is what I would face with a model refit each winter (USE-10, known entity; SPLIT-13).

**4. Would I use this model?**

- **As the emergency manager: yes, cautiously, as a first-pass prior** to order a storm's counties before the reports firm up. On 2024 I took the 775 storms with five or more counties or zones and some damage:
  - The log1p LightGBM puts 68.8% of a storm's dollars in its top 3 counties.
  - The event-type mean puts 61.7% there, and a perfect order 86.1%.
  - Weighted by dollars, the model gets 54.2% against 26.4% for the event-type mean.

  I would distrust it in three places:
  - where the office rarely enters dollars, since the model has learned that habit and ranks those counties down;
  - for tornado types that exist only after a survey;
  - everywhere, for the lack of exposure.

  Validation against FEMA PDA outcomes would make me trust it.
- **As the insurer: no.** There is no exposure, the label is blind to hail, and the totals are far off. Predicted dollars sum to 5.9% of the 2024 actual for the log1p model and 11.2% for a Tweedie model.

**5. Does the metric score my decision? Partly.**

- **What RMSLE scores here.** On 2024, with the log1p LightGBM:
  - 69.3% of the squared error falls on the 11.4% of rows where the zero/positive call at $500 is wrong.
  - $0 rows (74% of rows) carry 40.7% of the squared error.
  - Rows of $1 million or more (1% of rows, 97.5% of dollars) carry only 12.5%.

  Much of the score is whether the office entered a figure (the anomaly the definition documents).
- **Would I pick a model by it?** I compared three models on 2024: a log1p LightGBM, a Tweedie LightGBM on dollars (the actuarial form) and the event-type mean.

| | log1p LightGBM | Tweedie on dollars | event-type mean |
|---|---|---|---|
| RMSLE (declared) | 2.586 | 4.372 | 3.471 |
| within-storm top-3 dollar capture | 0.688 | 0.672 | 0.617 |
| same, dollar-weighted | 0.542 | 0.365 | 0.264 |
| mean per-episode Pearson on dollars (`mean_group_pearsonr`, `EPISODE_ID`) | 0.397 | 0.374 | 0.278 |
| global normalized Gini on dollars | 0.821 | 0.930 | 0.646 |

  - RMSLE picks the same winner as triage within a storm, but it places the Tweedie model below the event-type mean.
  - The global normalized Gini picks the Tweedie model, which ranks a storm's counties worse. On this target the Gini measures which storms are hurricanes and floods, not which county of a storm to visit. So `normalized_gini` (the builder's draft issue 5) would score my decision worse than `rmsle`.
  - The per-episode Pearson on dollars orders all three models as triage does.
- **The metric I would choose.** A within-storm score, with `EPISODE_ID` shipped as a scoring column and never as a feature (MET-2): `mean_group_pearsonr` on the dollars, which it computes after the log1p inverse. It is in the library, and it matches the unit I act on (MET-1).
  - Every episode is entered by one office: all 167,629 episodes from 2007 to 2025 have a single WFO. A within-episode score therefore holds the office's habit fixed, which is exactly the label problem RMSLE cannot get away from.
  - **Caveats.** 59.9% of the 2024 episodes with five or more rows have $0 on every row and drop out. Groups where a model's predictions are constant also drop out (1,812 groups for the log1p model against 1,399 for the event-type mean), so models are scored on slightly different sets. The curator should weigh that before adopting it.
  - If a per-row metric is kept, `rmsle` (origin context, MET-11; MET-3 is satisfied with `target_transform="log1p"`) is the best per-row option. Its reason should say that it is dominated by the zero/positive call.
  - The source fixes no k or cost (MET-7: never invent one), so no top-k metric, even though triage is top-k in spirit. MET-6, MET-8 and MET-9 are about classification thresholds and do not apply.

**Gaps, ranked by how much they change the task**

1. **Target (USE-5, USE-8).** The insurer half of the use case fails; the label is another quantity, about 12 times smaller in total and blind to hail. The emergency-manager half is a rough proxy whose zeros the office codes. This changes the task most.
2. **Unit (USE-1, MET-1).** The row is an event in a county segment; the decision is a county in a storm (25.4% of county-storms have several rows, holding 54.6% of the rows). A fifth of the test rows are hazards without an assessment decision.
3. **Inputs as first reports (USE-3).** The rows are Storm Data's entries made weeks later: tornado types and paths come from surveys (67.9% of tornado rows), and county segmentation and inclusion depend on damage. In practice the model would read LSRs, a differently shaped table.
4. **Missing inputs I always have (USE-6 in spirit).** Exposure, storm size, LSR remarks, radar footprints, outages. Their absence lowers the ceiling but does not void the task.
5. **Drift.** Nominal dollars, with positive damage drifting down (median Thunderstorm Wind $5,000 in 2007-2017, $2,000 in 2025). This is mild for a refit each year.

**What an expert in the domain would change**

1. **`use_case`.** Narrow it to the emergency manager alone. Proposed wording: "For example, a state emergency manager, once a storm has passed and its reports are in, ranks the counties it hit by expected property damage to decide where to send damage-assessment teams first." Drop "an insurer's catastrophe desk" and "what to reserve".
2. **`fit_reason`.** Replace "The features are what the first reports hold" with a sentence naming the gaps. Proposed wording: "The features stand in for the first reports: they are Storm Data's entries, made weeks later, with tornado types and paths from surveys, one row per event and county segment where the decision is per county and storm."
3. **Ship `EPISODE_ID` as a scoring column and score within the storm** (`mean_group_pearsonr`), or aggregate the rows to county-storm. Keep `rmsle` if neither is adopted. Do not switch to `normalized_gini`.
4. **Add exposure:** county population and housing units from the Census, joined on the county FIPS code for county rows. Zone rows would need the NWS zone-county correlation file. Possibly also add the storm's size from the data (rows and counties per episode); all events of an episode are known once the storm has passed.
5. **Consider dropping the hazards no one assesses** (marine, drought, heat, cold, fog, rip current, funnel cloud, waterspout, high surf): 19.8% of rows, 0.07% of dollars. This narrows the task to the decision.

**Sources**

- NWSI 10-1605 (26 July 2021): Sec. 1 (purpose), 2.7 (damage sources, the "no information available" box, the revision note on Verisk PCS), 3 (60-day certification), 4 (SPC preliminary reports and LSRs), 46 and 46.3 (thunderstorm wind entry criteria, EG), 47.5 and 47.6 (surveys, tornado criteria).
- NCEI metadata C00510 (reports "may be unverified by the NWS").
- FEMA and state damage-assessment process: [Florida SERT](https://www.floridadisaster.org/news-media/news/20181013-florida-sert-damage-assessment-teams-to-deploy-immediately-to-expedite-assistance/), [Missouri SEMA](https://sema.dps.mo.gov/recover/damage-assessment-process.php), [44 CFR 206.33](https://www.law.cornell.edu/cfr/text/44/206.33).
- Insurer side: [KCC June 2023 estimate and report counts](https://www.businessinsurance.com/convective-storm-system-causes-close-to-55-billion-in-insured-losses/), [CoreLogic June 2023](https://www.reinsurancene.ws/corelogic-estimates-insured-losses-from-june-u-s-storms-at-10bn/), [Swiss Re 2023 convective losses](https://theinsurer.com/news/swiss-re-severe-convective-storm-losses-reach-record-60bn-in-2023), [Triple-I 2025](https://www.mychesco.com/a/news/business/triple-i-reports-51-billion-in-2025-storm-losses-in-u-s/).
- Label quality: [Stallins 2002, Georgia lightning losses](https://www.uky.edu/~jast239/reprints/Southeastern%20Geographer%202002.pdf), [Laidlaw, Lazo & Bushek 2009, survey of the NWS loss-estimation method](https://ams.confex.com/ams/89annual/webprogram/Paper150932.html), [reliability of the Storm Events Database](https://arxiv.org/abs/1606.06973v2).
- Scale: [NCEI billion-dollar disasters, 2024](https://ncei.noaa.gov/access/billions/time-series/US/cost).
- Planning uses: [Diaz & Joseph, tornado damage](https://arxiv.org/abs/1807.03456); [FEMA NRI FAQ (SHELDUS losses)](https://hazards.fema.gov/nri/frequently-asked-questions) (unreachable today; read from the search summary).
- LSR contents: [NWS SCN 05-37, measured/estimated designation](https://www.weather.gov/media/notification/pdfs/scn05-37modified_lsr_format.pdf).

**Scratch**

The scripts and outputs stay in the local run folder:

- the decision unit, the dollar concentration, seven models under RMSLE, Gini and per-episode Spearman, and the squared-error decomposition.
- the hazards with no assessment decision, hail, and within-storm top-k capture.
- the per-episode Pearson.

All numbers come from one window with untuned models.

</details>

<details><summary>Blind review</summary>

**Verdict: include with changes.** This is a real, large, correctly parsed table with honest temporal evaluation and moderate signal. But a big part of the target, especially whether it is zero or not, reflects how each NWS office fills in the form, and that habit changes over time. The task should expose time features, and its documentation should say plainly that the label is an NWS estimate, not a measured loss.

**What the task is.** Each row is one event from the NOAA Storm Events database (NWS "Storm Data"), 2007-2025. The target is log1p of the property damage the NWS staff member preparing the entry recorded (`DAMAGE_PROPERTY`). The features are event type, state, county/zone, issuing forecast office (WFO), magnitude and its type, flood cause, hurricane category, start lat/lon, start time and duration. The most credible use is imputing the damage figure for Storm Data events where the preparer ticked "no information available". That is a real need for hazard-loss researchers, and the prepared population (events already in Storm Data) matches it. As a rapid loss estimator for insurers or emergency managers the use is weak: those users rely on claims, FEMA damage assessments or catastrophe models, not on the NWS figure.

**How I checked the data.** I downloaded the 2007, 2015, 2024 and 2025 details files from the NCEI csvfiles directory.
- Per year, the sample holds 30.0-30.2% of the raw rows with a non-blank damage field (for example 2025: 72,360 raw rows, 16,399 blank, 16,817 sampled; ratio 0.3005). So rows with blank damage were dropped and nothing else was.
- The target matches log1p of the parsed "K/M/B" strings exactly: 0 mismatches over 15,215 uniquely matched 2025 rows and 13,251 uniquely matched 2015 rows.
- The largest values are real disasters: the 2018 Camp Fire ($17B, Butte zone), Harvey 2017 ($10B, Harris County flash flood), Ian 2022 ($7B, Lee County) and Ike 2008.

**Concerns, most serious first**

1. **The zero label is mostly an office reporting convention, not physical "no damage".**
   - What the source says. NWSI 10-1605 (2021), section 2.7: "If this estimate is not available, then the preparer has two choices: either check the 'no information available' box, or make an estimate." In practice offices differ on whether they enter $0 or leave the field blank.
   - Thunderstorm Wind events with an estimated gust (EG). Section 46.3 says that wind value is "based on observed structural or tree damage", so these events had damage by construction. Yet across the 74 WFOs with at least 200 such events, the share recorded as $0 runs from 0.2% (BUF, IND) to 96% (GYX, OAX), with a median of 39%.
   - Change over time. Between 2007-14 and 2020-25, 27 of 95 WFOs changed their zero share by more than 20 points (DMX +62, LZK +51, CLE +48, BGM -38). In the raw files the blank ("no information") share rose from 7.3% (2007) to 17.4% (2015), 21.6% (2024) and 22.7% (2025).
   - Consequences. Zeros are 73% of rows, and WFO is the second most important feature by LightGBM gain (0.235, after event_type at 0.356). A large part of what a model learns is each office's data-entry habit.
   - Change: state this in the task description. Expose time as a feature (concern 2). Consider also reporting the score on rows with damage above zero, so that a method's ranking does not depend only on how well it guesses each office's zero convention. Keep the blank rows dropped: that is correct.

2. **The label drifts strongly over time, so the time features matter.**
   - LightGBM on my own reconstruction of three expanding-window splits (test = 70-80%, 80-90% and 90-100% time quantiles of the sample). With event type, location, magnitude, duration, month and hour, R2 was 0.469, 0.458 and 0.433. Adding `year` raised it to 0.548, 0.567 and 0.569, and RMSE on the log scale fell from about 2.8-3.0 to 2.5-2.6.
   - Other signs of drift: the mean log damage of nonzero rows fell from 9.42 (2007) to 8.44 (2025) even without inflation adjustment, and the Thunderstorm Wind zero share moved from 0.34 (2011) to 0.48 (2019).
   - Change: make sure `begin_time` or features derived from it (year, month, hour) are available to models, not used only to split. Otherwise the benchmark mainly penalizes methods for drift they were never allowed to see. Optionally convert dollars to constant dollars with CPI: nominal values rise about 0.43 on the log scale from 2007 to 2025, small next to the drift but systematic.

3. **Some event types are recorded only when they cause damage, and the estimated wind speed is inferred from the damage.**
   - What the source says. The directive defines Strong Wind as "...resulting in a fatality, injury, or damage", Lightning the same way, and Thunderstorm Wind below 50 kt only when "producing a fatality, injury, or damage".
   - In the data: Strong Wind is nonzero in 94% of rows and Lightning in 83%. EG versus measured-gust (MG) Thunderstorm Wind events have zero shares of 0.37 versus 0.89. Dropping `magnitude_type` costs about 0.02 R2.
   - Why this is not leakage. The qualitative damage report exists before the dollar figure is set, and the imputation use case conditions on the event being in the database. But it makes part of the zero/nonzero split trivial.
   - Change: none required. Document it. Do not add the tornado EF scale, tornado path length/width, SOURCE, injuries/deaths, crop damage or the narratives. These were rightly left out because they come from damage surveys or are outcomes recorded at the same time as the target.

4. **The target is coarse.** The directive asks preparers to round to three significant figures, and they round further. Only 991 distinct target values appear in 300k rows. Among nonzero damages, 66% are exactly 1, 2 or 5 times a power of ten ($1,000 alone: 11,881 rows; $5,000: 9,786). Combined with 73% zeros, RMSE on log1p is driven largely by getting zero versus $1k-$10k right. This is acceptable for a regression benchmark, but worth noting when reading the scores.

5. **Related rows: within-episode copies and exact duplicates.**
   - Episode and event IDs were dropped. In the raw 2025 file an episode has a median of 3 events, a 90th percentile of 18 and a maximum of 412, and in 191 of 1,577 episodes with two or more damaged events every event has the same damage (a total split evenly across zones). In the sample, 5,318 of 80,905 nonzero rows share state, event type, start time, duration and target with another row; Strong Wind accounts for 2,151 of them.
   - Under the temporal split such rows land in the same window except at window edges, so the leak is small. A random K-fold split would leak.
   - There are also 858 fully duplicated rows (0.3%), mostly Heavy Snow and Winter Storm. Change: remove exact duplicates, and never evaluate this task with a random split.

6. **Smaller preparation points.**
   - `magnitude` mixes hail size in inches (median 1.0) with wind in knots (median about 50). That is fine for trees but meaningless for linear or kNN models; splitting it into `hail_size_in` and `wind_kt` would be cleaner.
   - `hurricane_category` is 99.95% missing (158 rows, all Hurricane events). It is harmless but nearly useless.
   - `begin_time` is in local standard time per zone (CST, EST, MST and others), so hour of day is not on a common clock. This is minor.
   - lat/lon is missing for 92% of zone-type rows. That is structural and correctly left as NaN.
   - `state` includes about 20 marine or water-body areas (LAKE MICHIGAN, GULF OF ALASKA). This is fine.
   - `county_zone` has 7,907 levels. It is a reasonable high-cardinality categorical, though it adds almost nothing beyond WFO (removing both changes R2 by less than 0.01).

**Benchmark value.** There is clear signal beyond the trivial: R2 is 0.23-0.26 from event type alone and about 0.45 with all features, against a constant-mean baseline RMSE of about 3.9. The task is not trivial and has 1M rows. It brings mixed types, structural missingness and high-cardinality categoricals, and its temporal split is realistic. These are good reasons to include it, provided concerns 1-2 are addressed or documented.

**What I could not check**
- The exact three test windows used by the benchmark, and whether `begin_time` is passed to models as a feature. I used my own quantile windows.
- Full-row reconciliation for all 19 years. I verified row counts for 4 years and target parsing for 2 years.
- Whether the 858 exact duplicates are double entries in the raw data or distinct events. EVENT_ID was not retained.
- How many episodes straddle the window boundaries, since EPISODE_ID is not in the table.
- How accurate NWS damage estimates are against insured or FEMA losses. The literature calls them rough, and the directive itself allows rough estimates.
- Whether the 2024-2025 figures will be revised in later NCEI file versions. The 2025 file is dated c20260819.

**Sources:** https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/ ; https://www.ncei.noaa.gov/access/storm-events-database/ ; NWSI 10-1605 (July 26, 2021), https://www.weather.gov/media/directives/010_pdfs/pd01016005curr.pdf

</details>

<details><summary>Precedent check</summary>

**Precedent check: noaa_storm_events_damage (precedent-checker, 2026-11-01)**

**Verdict.** Five of the nine choices I checked follow their precedents: blanks dropped, `SOURCE` dropped, history
from 2007, the 2-month gap, and the markers kept. The metric departs from the screening and gives a reason. Three
choices need the curator:

1. Keeping the $0 entries departs from LEAK-25 (Must, P4). A Must takes no exception, and the curator's call of
   2026-10-30 is filed in the triage summary as "no rule", so it is not an amendment either.
2. Keeping the EG wind speeds departs from LEAK-10 as amended on 2026-10-26. The part of them that can be traced
   carries a gain.
3. The `Yes` sits against us_accidents (`No`, Lennart, 2026-09-23), which has a similar mechanism, and the CC states
   no fact that sets this case apart.

I found no drift and no third exception.

What I read: the register (1,620 decisions; it holds no MET rows, so for metrics I used the Cases table of
`metrics.md`), the Cases tables of `leak_checks.md`, `splits.md`, `metrics.md` and `selection.md`, the records behind
each precedent, the policy calls of 2026-10-30 (the zero-inflated triage summary), Andrej's CC lines
of 2026-10-30, and the sibling definitions of this batch. The siblings are AI drafts the curator has not decided. They
show what the batch does, not precedent. My own checks on the raw files stay in the local run folder.
I also cite one run of the column auditor.

| # | Decision | Rules | Result | Closest precedents |
|---|---|---|---|---|
| 1 | $0 entries kept as zeros | LEAK-25 (Must) | **not reasonable as an exception under the ranking** (a Must): amend the rule or apply it | ghanas_indigenous_intel (retired 2026-10-01); caracas_cervical_cancer, account_debt_south_africa, fraud_detection_in_electricity_and_gas_consumption (amendment 2026-10-21, CCs 2026-10-26) |
| 2 | Blank entries dropped | CLEAN-15 (Must) | consistent; the stated cause is an inference (see 1) | CLEAN-15; qsar_tid_11 (2026-10-21) |
| 3 | EG wind speeds kept with a `Potential leak, kept on purpose:` note | LEAK-10 (Must, clause 2), LEAK-37 | **departs; the stated reason is contradicted for the part that can be traced** | distribution_transformers_at_cauca_department (dropped, 2026-10-21); onlinenewspopularity (kept, 2026-10-26); zillow_prize, melbourne_housing_market (blanked, 2026-10-21); digicow `topics_list` (LEAK-37, 2026-10-21); in this definition: `TOR_F_SCALE`, `SOURCE` dropped |
| 4 | `SOURCE` dropped | LEAK-10, LEAK-7 | consistent | kick, expresso_churn_prediction (2026-10-22); distribution_transformers (2026-10-21) |
| 5 | `rmsle` by context, `target_transform="log1p"`, instead of the screening's fallback `rmse` | MET-3, MET-11 | departs from the screening, with a stated reason; follows the diamonds line | diamonds (MET-11, Lennart, 2026-10-21); onlinenewspopularity (CC 2026-10-26); batch pairs: nfip_redacted_flood_claims (AI, `rmse` "for a reserve"), nantucket (fallback `rmse`) |
| 6 | History from 2007, on a measured break | SPLIT-20, SPLIT-21 | consistent | aeolus (Lennart, 2026-10-12); fraud_detection, history cut at 2013 on a measured step (Lennart, 2026-10-26) |
| 7 | 2-month gap (60-day certification) | SPLIT-10 | consistent | brazilian_ecommerce (1 month, 2026-10-15), zillow_prize (1 month, 2026-10-20), sf_permit_time (6 months), house_sales (1 week) |
| 8 | Markers `No Good Target / Scientific Discovery` and `Data Quality Issue` kept on a `Yes` | selection.md, "Reading decision markers" | consistent | 5g_energy_consumption, ieee_fraud_detection, obesity_estimation, student_portuguese_performance (shipped with markers); batch: boreal, crms, pennsylvania, rand, blogfeedback, cape, loan_default |
| 9 | `Yes` on scope (CC 2026-10-30) | SEL-3, SEL-2, USE-5 | **a similar case was decided the other way** (another curator); the CC gives only an implicit reason | us_accidents (`No`, Lennart, 2026-09-23); thailand_road_accident_register_2019_2022 (`Yes`, Andrej, 2026-10-30) |

**A measurement that bears on 1, 2 and 6.** In the raw files the split between blank and $0 changes with the 2007
format. The positive share does not.

| Thunderstorm Wind events | blank | $0 | positive |
|---|---|---|---|
| 2000-2005 | 44-56% | 5-6% | 39-51% |
| 2007 | 10% | 45% | 45% |
| 2007-2025 | 10-24% | 29-45% | 39-56% |

Over all event types the blank share falls from 70-72% to 7%, and the $0 share rises from 5-8% to 70%. From 2007 on,
the $0 share of the entries stays at 67-79%.

What this shows:

* The break is a recoding of the entries that are not positive. That supports the cut at 2007 (SPLIT-20), and the cut
  was not chosen from test windows (SPLIT-21).
* Which code an entry gets is a format convention, so the data does not confirm the comments' reading that a blank means
  "the preparer had no estimate" (the box) and a $0 is an entered zero. The builder could not check how the box is
  exported.

**1. $0 kept (LEAK-25, Must).** The mechanism is the one the rule names: "no event" (no damage) mixed with "not recorded"
(no estimate made). The definition says so itself in its Anomaly bullet.

Since the amendment of 2026-10-21, a mix counts as recovered only when the unrecorded rows are located by a rule that
does not read the label, and are dropped:

* caracas_cervical_cancer: a skipped question;
* account_debt_south_africa: file runs without debt data;
* fraud_detection: the last invoice date, "never by the label".

When the rows cannot be located, the precedent is ghanas_indigenous_intel: retired.

Here only the blanks are located and dropped, and the measurement above shows that blank against $0 does not separate
the two meanings. No label-free rule that locates the "not estimated" $0 entries was found. A rule on the office's $0
share reads the label in aggregate.

What the definition rests on, and why neither is enough:

* "the office is a feature, so a model can learn the practice". This is the mechanism itself, not a recovery.
* "(curator, 2026-10-30: coded zeros are a cleaning choice, no obstacle)". The curator's words were "We don't care. We
  want to add any relevant predictive task, independent if it is zero inflated or not". The summary files that answer
  under "Coded zeros (no rule)". It settled verdicts and priorities. "A cleaning choice at /add-dataset" is the AI's
  application of it, in the triage summary and in the record's Assessment.

The definition therefore attributes an AI reading to the curator. Quote the call and label the gloss as the AI's.

Under the ranking, no higher Must carries the keep. The use case is a "for example" actor with fit approximate. The
Tensions row "a real task against a leak" stops at "a leak that cannot be undone".

The builder's issue 1 offers "exception or amendment". Only the amendment is open. The rule as written leaves two
outcomes: re-target or retire. The remedy ladder puts "fix the definition (re-target)" before exclusion. Re-targeting
to the entered positive amounts would remove the $0 mix, but the entries that were never estimated would still select
the rows.

**2. Blanks dropped (CLEAN-15, Must).** This is consistent: a row without a target leaves. The drop stands on CLEAN-15,
whatever the blank means. It is not LEAK-25 recovery, and the comments' causal reading ("the preparer had no estimate")
should be marked as an inference.

**3. EG speeds kept (LEAK-10).** NWSI 10-1605 Sec. 46.3 says the preparer sets the value "based on observed structural
or tree damage", so for some rows it is set after the prediction point. LEAK-10's second clause (Lennart, 2026-10-26)
settles values of that kind:

* late cells that can be located are blanked (zillow_prize, melbourne_housing_market);
* where they cannot be located, the values go when a gain may sit on them (distribution_transformers_at_cauca_department);
* they stay with a note only when the part that can be traced shows no gain (onlinenewspopularity: masking changed R^2
  by -0.0004).

The definition keeps the speeds "because ... which values the preparer set later cannot be located". Part of them can
be located: 6,177 EG entries come from events whose `SOURCE` is "NWS Storm Survey" (6,114 of them Thunderstorm Wind).
Against the other Thunderstorm Wind EG entries they have:

* a median of 65 kt, against 52;
* damage in 72%, against 62%.

The traced part carries a gain. In the column auditor's run C, blanking those speeds raises the RMSE on the 533 such
test rows of 2024 from 3.246 to 3.448, and on all rows from 2.601 to 2.610.

Blanking them alone would leave a marker, because every Thunderstorm Wind entry has a magnitude (261,702 of 261,702).
That is the same reason the definition gives for dropping `SOURCE`. The same definition also drops `TOR_F_SCALE`, a
wind rating made from the damage, so the EF rating, `SOURCE` and the EG speed are like cases decided two ways.

The reason given, "the first report carries the same description of the damage", is LEAK-37's argument (an input the
actor knows at the prediction point; digicow `topics_list`). It holds only if the EG values appear in the real-time
reports. That can be traced against the NWS Local Storm Report archive (EV-1), and has not been. The figure quoted for
the value, ROC AUC 0.433 for any damage, also understates its link to the amount: the claim auditor measures a Spearman
correlation of 0.462 between the EG speed and log dollars among the positive entries. Andrej's own lines of the same day
on leaks point the same way: "If an unresolvable leak remains, explain it and move to No" (loan_default_prediction);
"Move to yes if you can resolve the leak, otherwise no" (blogfeedback).

**4. `SOURCE` dropped: consistent.** LEAK-7 asks for the smallest fix first. The builder measured it: merging "NWS Storm
Survey" into "Unknown" keeps the survey's signal (RMSE 2.565, against 2.560 as published and 2.608 without the column),
and blanking leaves a marker in a column with no missing values. Dropping a field whose measured marker survives the
smallest fix follows kick and expresso_churn_prediction (2026-10-22). The cost in signal is no reason to keep it
(distribution_transformers: ROC AUC 0.701 to 0.639, dropped). The builder's issue 3 alternative, the merge, would keep
the marker and depart from those cases.

**5. Metric: departs from the screening, with a stated reason.** The screening's fallback `rmse` came "with the target's
scale to settle when adding (MET-3)", and a later stage's finding supersedes it. `rmsle` by context follows diamonds
(Lennart, 2026-10-21: the error matters relative to the size) and onlinenewspopularity (CC 2026-10-26, "RMSLE as
declared", a heavy-tailed count). The declaration is in the MET-3 form (`target_transform="log1p"`, mercari).

Two things for the curator to see:

* The decided context cases have no mass at zero. Here 73% of the entries are $0, so RMSLE weighs heavily whether an
  entry is $0 or a few thousand dollars, and that is the part the office's practice decides (1). No decided case covers
  this.
* The use case says the actor decides "what to reserve". For nfip_redacted_flood_claims the AI suggested `rmse` because
  "the use is a case reserve, set in dollars" (Assessment, 2026-10-30). That is not a curator decision, but it is the
  same wording with the other metric.

Either the use case says what the relative metric serves (where to send assessors first), or the metric follows the
reserve. The insurance siblings' `normalized_gini` was the AI's suggestion for pricing under call 3, and NFIP was set
apart from it as no pricing task. Storm damage is no pricing task either.

**6, 7, 8: consistent.**

* History: SPLIT-20 asks to check for "a change of rules or of the data collection" and to say why; the measurement
  above confirms the break. The positive amounts still drift within the kept years (median of Thunderstorm Wind $5,000
  to $2,000). That is a weighing note under "keep a recent stretch", not a departure. Nominal dollars follow the
  housing cases (house_sales, melbourne_housing_market); CLEAN-21 is about features.
* Gap: SPLIT-10, a gap of the documented delay, as in the four cases listed in the table.
* Markers: "a `Yes` with a concern marker is not a contradiction". The table defines `Data Quality Issue` as damage that
  cannot be undone (LEAK-27, PROV-3). If LEAK-25 is settled by amendment, that marker has nothing left to mark.

**9. Scope against us_accidents.** Lennart's `No` (CC 2026-09-23): "Too hard to tell whether there is a real predictive
distribution here beyond finding the right subsets (feed, period, location) that reproduce a provider's codes". Here:

* event type and office alone give ROC AUC 0.934 of 0.950 for any damage (screening probe);
* the $0 share runs from 7% to 91% across offices;
* the definition relies on the office to "learn the practice".

The screening named this precedent and kept the record "on the event-register precedent". Andrej's `Yes` on
thailand_road_accident_register_2019_2022 and his call 1 of 2026-10-30 ("if a dataset is useful for a predictive
application although the data was collected for something else, then this is fine") are the implicit reasons. Neither
answers us_accidents' point, which was about the label, not the purpose of the collection.

**Also seen (a like pair inside the definition).** The end point (`END_LAT`, `END_LON`, ...) is dropped because for a
tornado it is the end of the surveyed path. The end time of that same path stays, inside `duration_hours`. The column
auditor's run B: blanking the tornado duration raises the tornado RMSE from 4.629 to 4.894. I leave the call to the
column auditor's report.

**Reflection prompts**

**Consistency check (AI, 2026-11-01):** the definition keeps the $0 entries (a departure from LEAK-25, Must: "no event"
mixed with "not recorded", the unrecorded rows not located). That differs from ghanas_indigenous_intel (retired
2026-10-01, rows not located) and from caracas_cervical_cancer, account_debt_south_africa and fraud_detection (located
by a rule that does not read the label and dropped; 2026-10-21 and 2026-10-26). Your call of 2026-10-30 is filed as "no rule"
and covered verdicts. What sets this case apart? (a) The mix follows the reporting office, a feature known at the
prediction point, so a model meets the practice as a learnable effect rather than hidden noise; and with 1,000,829
rows the task is not `Too Small` as ghanas was. A Must takes no exception, so (a) can only be recorded as (d).
(b) Treat it like the precedents: re-target to the entered positive amounts, or retire. (c) Reopen ghanas (retired
also as `Too Small`, so this changes nothing there). (d) Amend LEAK-25: "a mix that follows a reporting unit shipped as
a feature is kept with a note, fit approximate".

**Consistency check (AI, 2026-11-01):** the call on the EG wind speeds (keep with a note) differs from
distribution_transformers_at_cauca_department (dropped 2026-10-21: values set after the outcome for an unknown subset,
with a gain that may sit on them) and from this definition's drops of `TOR_F_SCALE` and `SOURCE`. It would follow
onlinenewspopularity (kept 2026-10-26) only if the traced part showed no gain, and the 6,177 storm-survey EG speeds
show one (RMSE 3.246 kept, 3.448 blanked, on 533 test rows). What sets it apart? (a) A non-survey EG speed is in the
real-time Local Storm Report the actor reads (LEAK-37), to be shown on a sample traced against the LSR archive. The
survey speeds would then stay as a stated residual, since blanking them leaves a marker. (b) Treat it like
distribution_transformers: blank every EG speed (RMSE 2.560 to 2.589) and keep the EG/MG type. (c) Reopen
distribution_transformers. (d) Amend LEAK-10's second clause.

**Consistency check (AI, 2026-11-01):** your `Yes` (2026-10-30) differs from us_accidents (`No`, Lennart, 2026-09-23,
`No Good Target / Scientific Discovery`: a label a model reproduces from "the right subsets (feed, period, location)"),
with a similar mechanism here: event type and office give ROC AUC 0.934 of 0.950 for any damage. What sets it apart?
(a) The target is a dollar amount estimated by the preparer (an expert annotation under SEL-3), whose positive part
carries signal beyond place and reporter (R^2 0.48 on log1p among the positives, screening probe), and whose zero share
is stable over 2007-2025 (67-79% of entries). us_accidents' Severity was a feed's traffic-delay code whose classes
changed meaning (class 3 from 31% to 0%). Recorded under SEL-2 with your call 1. (b) Treat it like us_accidents
(`No`). (c) Reopen us_accidents. (d) Change SEL-3.

**For the curator, in rank order:**

1. LEAK-25 (P4, Must): amend or apply.
2. LEAK-10 (P4, Must): EG speeds, after the LSR trace or blanked.
3. SEL-3 (P2) against us_accidents.
4. MET-11 (P6): make the use case and the metric say the same thing.
5. A text fix: the curator attribution in the target bullet.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief: noaa_storm_events_damage (2026-11-01)**

**Position: ship after changes.** The split, the signal, the scope and the metric hold on measured evidence. The
evidence agents found three real LEAK-10 columns, a use-case half that fails and a SPLIT-10 shortfall; I concede all
of them, and each one has a fix in the definition. The one call I cannot settle by argument is LEAK-25 (point 6): the
dataset ships only if the curator turns the 2026-10-30 call on coded zeros into an amendment. I say so plainly below
rather than dress it up as an exception. No new probes of my own; every number is from the panel's reports.

**1. The split is honest and measured (P4).**
- Claim: calendar-year test windows (2025, 2024, 2023) with an expanding train side and known places mirror a model
  refit each winter. The split auditor rates it "right with notes".
- Evidence: county_zone is seen in train for 99.2% of test rows, and wfo and state for 100%. None of the 167,629
  episodes spans two months, so none crosses a cut. Later releases change 0 of 64,921 Jan-Oct 2025 damage values and
  0.17% of the 2024 ones. The 2007 start sits on a measured break: 69.5-72.2% blank in 2000-2005, 7.3% in 2007. A
  random split would overrate the models by 0.16-0.36 RMSE (R^2 0.67 against 0.57-0.61 per window). So the temporal
  split is exactly what tests whether a model can carry each office's practice forward a year.
- Rules: SPLIT-1, SPLIT-3, USE-10, SPLIT-6, SPLIT-9 (Must) hold; SPLIT-13, SPLIT-14, SPLIT-20 (Should) hold.
- Real problem, conceded: SPLIT-10 (Should). The public files lag about 75-80 days, so October is not public at a
  1 January refit. Mildest fix: `gap=3` months, citing C00510's "up to a 120 day delay possible", and reword
  `task_summary.split` to "every event published by the refit". The 0.02-0.03 cost is an edge effect: it vanishes
  without the time feature and with random row removal. The split follows the application, not the score (P4 over
  P6; forest_fires). Precedent: mortgage and sberbank lag their series to the release.

**2. Real signal remains after every leak fix (P4 fixes, P6 value).**
- Claim: the three LEAK-10 findings are real. Each has a definition fix that keeps the task, and the task stays far
  from both trivial and dummy.
- Evidence and fixes:
  - EG wind speeds: the LSR match shows 94.4% of the 2024 EG speeds were not in the first report (a "TSTM WND DMG"
    with no speed), while measured gusts carry over 92.7% and hail sizes 97.9%. Fix: blank `magnitude` where
    `magnitude_type == "EG"` and keep `magnitude_type`, since the first report says whether it was a damage report or
    a measured gust.
  - Tornado `duration_hours`: Spearman 0.83 with the dropped `TOR_LENGTH`. Fix: blank it on every Tornado row. Blank
    by event type, not by `SOURCE`, so the blank is no survey marker.
  - `hurricane_category`: set per zone, and Michael's Cat 5 is the April 2019 reanalysis. Fix: drop it (483 rows, 0
    in the 2025 window).
  - After all three: LightGBM RMSLE 2.556 (mean of the 3 windows) against a dummy at 3.82/4.01/3.87. Event type alone
    gives R^2 0.269 against 0.567 for all features (builder, before the fixes). The leak probes raise no red flag (best
    single feature 0.248).
- Rules: LEAK-10 (Must), second clause: late cells that can be located are blanked. LEAK-2 (Must): the sibling sweep.
  LEAK-7 (Should): the smallest fix. USE-12 (Must): a leak is no reason to reject a real task. The TP rules hold
  (beats the dummy 3/3).
- Why it outranks the objection: step 2 of the remedy ladder (fix the definition) resolves each one. None is a leak
  that cannot be undone (LEAK-27), so the Tensions row "a real task against a leak" keeps the task.
- Related: Strong Wind, Lightning and sub-50 kt wind rows exist only with damage (3.5-4.0% of test rows). They stay
  under LEAK-37 (Must): the first report already says damage was seen. The domain practitioner and the blind reviewer
  both read it as no leak. Fix: say it in `known` and in the prediction-point bullet.

**3. Scope and target hold, and us_accidents is set apart by facts (P2).**
- Claim: SEL-3 holds. The target is an expert annotation, the NWS preparer's estimate under a written directive
  (NWSI 10-1605 Sec. 2.7). The curator's `Yes` (CC 2026-10-30) stands.
- Evidence against us_accidents (Lennart, 2026-09-23):
  - That label was a traffic-delay code that did not serve the first responder (a USE-5 failure). Its classes changed
    meaning (class 3 from 31% of 2016 to 0% of 2023), and the temporal split left log loss 0.48 against a 0.53 prior.
  - Here the label is dollars of damage, the quantity the actor ranks. The $0 share of the entries stays at 67-79%
    from 2007. Under the temporal split RMSLE is 2.556 against 3.90, and the positives alone give R^2 0.48 (screening
    probe).
  - Within one storm, where the office is fixed (every one of 167,629 episodes has a single WFO), the model still
    ranks counties above the event-type mean: per-episode Pearson 0.397 against 0.278.
  - The blind reviewer says "include with changes". The practitioner would use it "cautiously, as a first-pass prior".
- Rules: SEL-3 (Must): "an observed outcome or an expert annotation". SEL-2 (Must): the use case decides, read with
  call 1 of 2026-10-30. Like cases alike unless a fact sets them apart, and here three facts do.
- Why it outranks the objection: the curator's decision outranks an AI assessment, and the precedent checker's
  option (a) supplies the distinguishing fact to record.

**4. The use case is real once narrowed (P3).**
- Claim: narrowed to the emergency manager's triage, the actor, moment and decision hold. That narrowing fixes the
  definition. It is no reason to drop the dataset.
- Evidence:
  - Local emergency managers run the Initial Damage Assessment to "determine impact areas to prioritize" (Florida
    SERT, Missouri SEMA, 44 CFR 206.33).
  - On 2024, the model's top 3 counties hold 68.8% of a storm's dollars, against 61.7% for the event-type mean (86.1%
    for a perfect order). Weighted by dollars it is 54.2% against 26.4%.
  - Conceded, the insurer half: Storm Data's 2024 total is $15.7B against $182.7B for NCEI's billion-dollar events,
    and hail is 11.1% of the rows but 1.4% of the dollars.
- Rules: USE-1 (Must) holds after narrowing. USE-5 (Must), last sentence: the insurer reading fails, so drop "an
  insurer's catastrophe desk" and "what to reserve" (the practitioner's wording). USE-8 (Must): fit approximate is
  already declared. Rewrite `fit_reason` to name the gaps: Storm Data entries made weeks later, and one row per event
  and county segment where the decision is per county and storm (25.4% of county-storms have more than one row).
- Why it outranks the objection: the remedy ladder (re-target the framing before exclusion) and USE-12. Optional,
  a curator's weighing: drop the hazards nobody assesses (19.8% of rows, 0.07% of dollars).

**5. The metric is right for the narrowed task (P6).**
- Claim: `rmsle` by context, with `target_transform="log1p"`, is the right metric.
- Evidence:
  - On raw dollars the top 0.1% of entries hold 99.96% of the squared deviation, and the model's dollar RMSE beats
    predicting $0 everywhere by only 0.2-3.8%.
  - `normalized_gini` picks the Tweedie model, which ranks a storm's counties worse (dollar-weighted top 3: 0.365
    against 0.542). RMSLE picks the same winner as triage within a storm.
  - Diaz & Joseph 2019 score tornado damage on the log scale. That supports the call, but it is a tornado-only,
    multi-metric, randomly split task, so it is no source metric (MET-5).
- Rules: MET-11 (Must), context (diamonds; onlinenewspopularity). MET-3 (Must). MET-1 (Must).
- Real problems, conceded:
  - The reason says no paper exists, but one does: name Diaz & Joseph 2019.
  - The reason should say that 41-49% of the error falls on the true-$0 rows.
  - Once the insurer half goes (point 4), the clash between "what to reserve" and NFIP's `rmse` is gone.
- Option for the curator: `mean_group_pearsonr` within `EPISODE_ID` as a scoring column. It holds the office fixed,
  but it has a caveat: 59.9% of the episodes with 5 or more rows are all $0 and drop out.

**6. LEAK-25: the open call, and the fix that keeps the dataset (P4).**
- Claim: the zero mix is real. Under the rule as written it cannot be kept as an exception. The fix that keeps the
  dataset is an amendment of LEAK-25, which the curator's 2026-10-30 call already points to.
- Evidence:
  - The source's own "no estimate" mark is located and dropped. The directive forbids the box only for floods, and
    Flood and Flash Flood have no blanks from 2008 on (26 in 2007), against 14.6-28.3% blank for the other main types.
    So the blank is the box: 18.3% of the events, dropped.
  - Conceded: a residual remains, $0 entered where no estimate was made. 13 of 121 EF4/EF5 segments are at $0, and
    17.3% of EF2+.
  - That residual follows a feature, the office. An office's $0 share in 2024 predicts its 2025 share at r 0.958, and
    within one office's storm the model still ranks counties (point 3). So the score is not only the recording
    practice.
  - The precedent that retired a dataset under LEAK-25, ghanas_indigenous_intel, was also `Too Small`. LEAK-25 has
    not decided a large task on its own.
  - The curator saw this exact mechanism (the screening's risks name "$0 against blank, offices that rarely
    estimate") and answered "We don't care. We want to add any relevant predictive task, independent if it is zero
    inflated or not", then `Yes`.
- Rule: LEAK-25 (Must). I concede that nothing ranked above it carries the keep, and that a Must takes no exception.
  Principles, "Consistent judgement" 1: a call that breaks a Must is offered as an amendment. Draft amendment: "a mix
  whose unrecorded part the source flags and the definition drops, and whose remainder follows a reporting unit
  shipped as a feature, is kept with a note and fit approximate".
- Why it outranks the objection: the curator decides and may amend (amendment > exception > precedent). Exclusion is
  for a Must that cannot be fixed, and here the fix is a rule change that only the curator can make. If the curator
  declines, the honest outcome under the rule as written is `No`, since re-targeting to the positives still leaves
  the selection. The rest of the dataset gives no reason to go there.
- Text fix, conceded: the target bullet attributes an AI gloss to the curator ("a cleaning choice"). Quote the call
  instead and label the gloss as the AI's.

**7. The quality items are cheap and decide nothing (P7).**
- Fixes:
  - LEAK-19 (Should): drop the 1,072 exact raw copies (narrative included).
  - CLEAN-21 (Should): split `magnitude` into `wind_speed_kt` and `hail_size_in`. The split is lossless (2.6125
    against 2.6007, inside the noise).
  - CLEAN-11 (Should): set the 24 impossible wind values to missing.
- Wording:
  - Flood blanks: 26, all in 2007.
  - Episodes: none spans two months, so drop "except at New Year".
  - The 2024 file comparison: 1.3% of events were added or removed.
  - Office drift: 30% of offices moved by more than 0.2.
  - Scratch base: 2.582 on the shipped features.
- Untested and bounded: rewrites of older years (2012 file of October 2026). The 2024 and 2025 comparisons bound them
  at 0-0.17%.
- Rule: principles, step 3: a quality problem is fixed when the fix is cheap and safe. None of these touches validity.

**Changes I accept, in rank order:** amend LEAK-25 or retire (curator); narrow `use_case` and rewrite `fit_reason`;
blank EG speeds; blank tornado durations; drop `hurricane_category`; add the damage-report fact to `known`; `gap=3`;
name Diaz & Joseph and the zero share in the metric reason; drop the 1,072 copies; split `magnitude`; fix the
impossible values and the wording.

</details>

<details><summary>Critic</summary>

**Critic: opening brief, noaa_storm_events_damage (2026-11-01)**

**Verdict: do not ship as defined; ship only after the changes below.** Point 1 decides whether it ships at all: as
written, the definition sets aside a Must (LEAK-25) and backs that with a gloss on the curator's words. Points 2 to 4
are validity fixes in the definition, and they are cheap. With all three LEAK-10 fixes the task keeps its signal:
mean RMSLE goes from 2.504 to 2.556 over the 3 windows, against a dummy at about 3.90 (claim auditor, s06).

```text
Verdict: ship after changes (no ship without a decision on point 1).
Validity: SEL-3 consistency check against us_accidents (point 1); USE-5 triggered, fix the text (point 2);
  LEAK-25 triggered, not recovered (point 1); LEAK-10 triggered three times, fixable (points 3, 4);
  SPLIT-10 departure (point 5).
Value: MET-1/MET-11, the reason misstates the search; rmsle kept (point 6).
Quality: CLEAN-21, LEAK-19, CLEAN-11 and text fixes (point 7), no reason to exclude.
```

**1. The $0 label is largely office entry practice (P4, LEAK-25 Must; P2, SEL-3 consistency check).**
- *Problem.* A $0 mixes "no damage" with "not estimated". The definition says that blanks are the "no information
  available" box and that a $0 is an entered zero. The data does not support that reading. In 2007, when the files
  switched to the CSV format, Thunderstorm Wind entries moved from 49.8% blank and 7.1% $0 (2006) to 10.5% blank and
  44.7% $0, while the positive share stayed flat (43.1% to 44.8%; precedent checker). So
  the "no information" entries became $0.
- *More evidence.* 13 of the 121 EF4/EF5 tornado segments are at $0, among them a 33.7-mile EF5 in Alabama in 2011,
  and 17.3% of the EF2+ segments (claim auditor, claim 13). Across offices, the $0 share of Thunderstorm Wind runs
  from 7% to 91% (10th to 90th percentile), and it moves over time: 30.5% of 82 offices shifted by more than 0.2
  (claim 15).
- *Effect.* RMSLE spends 41-49% of its squared error on the true-$0 rows (claim 35). On 2024, 69% of it falls on the
  rows where the zero/positive call is wrong (practitioner). Event type and office alone give ROC AUC 0.933 of 0.952
  for any damage (claim 39). Much of the score therefore ranks how well a model reproduces each office's habit. That
  is the mechanism Lennart retired us_accidents for (`No`, 2026-09-23: codes reproduced from "the right subsets").
- *Rule.* LEAK-25 (Must): retire unless recovered. Since 2026-10-21, recovered means the unrecorded rows are located
  by a rule that does not read the label, and nothing here locates them. The curator's call of 2026-10-30 ("We don't
  care. We want to add any relevant predictive task, independent if it is zero inflated or not") is filed as
  "Coded zeros (no rule)". A Must takes no exception (principles.md, Strengths). The `Yes` gives no fact that sets
  this case apart from us_accidents (Consistent judgement, case 2).
- *Remedy, the mildest that works.* The curator decides it as an amendment of LEAK-25, for example "a mix that
  follows a reporting unit shipped as a feature is kept with a note, fit approximate", and records what sets the case
  apart from us_accidents. Without an amendment, the rule leaves two outcomes:
  - (b) re-target to the entered positive amounts. This removes the mix, but it narrows the task and selects rows on
    the label.
  - retirement.

  Whichever way the curator goes, three text fixes:
  - Quote the curator's words in the Target bullet instead of "coded zeros are a cleaning choice". That phrase is the
    AI's gloss.
  - Mark "blank = no estimate" as an inference that the 2007 recoding contradicts.
  - Change the acceptance reason of `task_target_value_dominant` from "zero-inflated by nature" to "part of the
    zeros are unestimated damage".

**2. Half of the use case fails, and `fit_reason` misstates the inputs (P3, USE-5 Must; USE-3, USE-8 Must).**
- *Problem.* The use case names an insurer's catastrophe desk deciding "what to reserve". The label is a different
  quantity:
  - Storm Data's 2024 total is $15.7B, against $182.7B for NCEI's billion-dollar events of 2024 (the scopes differ).
  - Hail is 11.1% of the 2024 rows but 1.4% of the dollars, while it drives up to 80% of severe-storm claims.
  - The model's predicted dollars sum to 5.9% of the 2024 actual (domain practitioner, Sec. 2).
- *`fit_reason`.* It says "The features are what the first reports hold". Claims 3, 4, 5 and 23 refute that for
  three columns. In addition:
  - 67.9% of tornado rows come from storm surveys (NWSI Sec. 47.6 types a tornado from its damage).
  - Strong Wind, Lightning and sub-severe Thunderstorm Wind enter Storm Data only with damage. They are 94.2%, 83.9%
    and 97.5% positive (claim 42). That is known at the first report only if the report says damage was seen, and
    `known` does not say so.
- *Effect.* A benchmark user reads an insurer task the label cannot serve, and reads the inputs as cleaner than they
  are.
- *Rule.* USE-5, last sentence: "A label checked and found to be another quantity than the one the actor acts on
  still fails" (Lennart, 2026-10-21).
- *Remedy (fix the definition, text only).*
  - Narrow `use_case` to the emergency manager ranking a storm's counties for damage-assessment teams (the
    practitioner's wording), and drop the insurer and "what to reserve".
  - Rewrite `fit_reason` to name the gaps: Storm Data entries made weeks later, tornado types from surveys, and one
    row per event type and county segment where the decision is per county and storm.
  - Add to `known` that the first report says whether damage was seen.
  - Weighing call for the curator: filter the hazard types that no assessor is sent for. They are 19.8% of the 2024
    rows, 99.7% of them $0, and 0.07% of the dollars, and they make the task look easier.

**3. The EG wind speeds are written after the first report, and they can be located (P4, LEAK-10 Must, clause 2).**
- *Problem.* The note keeps the speeds because the late values "cannot be located". The claim auditor located them.
  2024 county Thunderstorm Wind events were matched to the real-time Local Storm Reports (IEM archive), and 12,498 of
  the 13,211 EG events matched. For 94.4% of them the first report was "TSTM WND DMG" with no speed, and only 4.4%
  carried the speed Storm Data shows. The check works: measured gusts carry over 92.7% of the time and hail sizes
  97.9% (claims 3 and 20).
- *Effect.* The model reads a number the preparer set from the damage (NWSI Sec. 46.3; Table A7, "Estimating Wind
  Speed from Damage"). Among the entries with damage it tracks the dollars: Spearman 0.51 on the matched 2024 events,
  0.462 overall. The note's AUC of 0.433 measures any damage, not the amount that is scored.
- *Like cases.* This definition drops `TOR_F_SCALE` for the same mechanism (LEAK-2). On precedent,
  distribution_transformers_at_cauca_department was dropped, and zillow_prize and melbourne_housing_market were
  blanked.
- *Steelman.* MG speeds rank the damage just as well, and the practitioner accepts EG because the first report is a
  damage report. That argues for keeping `magnitude_type`, which the first report carries. It does not argue for the
  number, which 94.4% of first reports lack.
- *Remedy.* Blank `magnitude` where `magnitude_type` is EG, and check ES, the same estimate for sustained wind
  (LEAK-2). Keep `magnitude_type`. The blank follows a shipped feature, so it leaves no marker. Cost: 2.504 to 2.538.

**4. Two more survey products remain: tornado `duration_hours` and `hurricane_category` (P4, LEAK-10 Must; LEAK-2,
LEAK-6).**
- *Tornado duration.* For a tornado, begin and end mean ground contact, which the survey sets (Sec. 47). 68% of
  tornado rows have `SOURCE` "NWS Storm Survey".
  - Duration correlates with the dropped `TOR_LENGTH` at Spearman 0.83. With duration in the model, adding
    `TOR_LENGTH` moves tornado RMSE only from 4.629 to 4.618: the path is already there.
  - Blanking duration raises the tornado-row RMSLE by 0.16 to 0.23 in the 3 windows (claim 23; column auditor +0.26,
    five times the noise).
  - The definition drops the end point of the same path.
- *Hurricane category.* It is set per zone:
  - 23 of the 95 episodes with a category carry more than one value.
  - Michael 2018 runs from 1 to 5 across 14 zones. Its Cat 5 zone ($6B) matches the post-storm upgrade of April 2019,
    while the operational landfall category was 4.
  - NWSI pairs each category with "Types of Damage". The $0 share is 29% at Cat 1 and 0% at Cat 4-5 (claims 4 and
    25).
  - The Built bullet's reading ("the category ... the National Hurricane Center issues before landfall") is wrong.
- *Remedy.*
  - Blank `duration_hours` on every Tornado row: by type, not by `SOURCE`, which would leave a survey marker.
  - Drop `hurricane_category`. It covers 483 rows and none in the 2025 window, and under LEAK-6 a confirmed late value
    goes even when small.
  - Correct the Built bullet.

**5. The gap is shorter than the actor's label delay (P4, SPLIT-10 Should).**
- *Problem.* The gap of 2 months comes from the 60-day certification. The actor reads NCEI's public releases, which
  lag 75 to 80 days (measured on three archived releases; C00510 says "up to a 120 day delay possible"). On 1 January,
  the public file holds events through September. `task_summary.split` ("every event certified by the start of that
  year") is partly refuted: May 2025 was 83% present 79 days after its end, and 417 events were added after
  16 Jan 2026 (split auditor).
- *Effect.* Each training side holds one month the actor would not have: 1,401 to 1,743 October rows, 0.15-0.21%.
  There is no shortcut (SPLIT-9 holds).
- *Remedy.* Either set `gap=3`, or keep 2 months and restate the refit as made at the mid-January release. Reword
  `task_summary.split` to "every event published by the refit". The score difference (+0.02 to 0.03 for gap 3) is an
  edge effect and should not decide.

**6. The metric reason misstates the search, and it leaves out what the score is made of (P6, MET-1 and MET-11
Must).**
- *Problem.* The reason says that no competition or paper on this target was found. Diaz & Joseph 2019 (Weather and
  Climate Extremes 25:100216) models tornado property damage from this database (claim 32). The reason also says
  that a relative error fits the use, yet the use case's "what to reserve" is a dollar sum (see point 2), and much of
  the error sits at the zero/positive call (see point 1).
- *Effect.* Rmsle reads as an unanchored choice, and a reader does not learn that the score ranks models largely by
  how they reproduce $0 entries.
- *Remedy (repair the text).*
  - Name the paper. It reports several metrics on a tornado-only subset with a random split, so it gives no unique
    original (MET-5). It scores on the log scale, which supports rmsle.
  - State that the zero/positive call dominates the score.
  - Keep `rmsle`. A within-storm score (`mean_group_pearsonr`, with `EPISODE_ID` as a scoring column) is a weighing
    call for the curator, with its caveat: 59.9% of the 2024 episodes with five or more rows are all $0 and drop out.
  - Not `normalized_gini`: on 2024 it prefers the model that ranks a storm's counties worse (practitioner).

**7. Quality, fixes that are cheap and safe (P7, Should; no reason to exclude).**
- **CLEAN-21:** `magnitude` holds knots and inches in one column. Split it into `wind_speed_kt` and `hail_size_in`.
  The split is lossless (2.6125 against 2.6007, inside the noise).
- **LEAK-19:** 1,072 rows are exact copies of another raw row in every published column, narrative included. They
  are double entries, not separate events, as the duplicates note says (claim 26). Drop them, or correct the note.
- **CLEAN-11:** 22 Thunderstorm Wind entries of 1-10 kt and 2 Strong Wind entries of 0 kt should become missing.
- **Text:**
  - "Flood and Flash Flood have no blanks" is wrong: there are 26, all in 2007.
  - The scratch base includes `SOURCE` and `year`. The base on the shipped features is 2.582.
  - "except at New Year" never occurs: 0 of 167,629 episodes span two months.
  - The 2024 file comparison leaves out 907 events (1.3%) that were added or removed.

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal: noaa_storm_events_damage (2026-11-01)**

**Where this leaves the case.** The critic and I agree on the verdict: ship only after the changes, and only once the
curator has decided LEAK-25. We also agree on points 2 to 7. Point 1 is the only live dispute. I ran three checks on
it, and the main one goes against me. The office is the largest single part of the score, larger than either brief
said. I concede that effect. I dispute only the critic's reading of the 2007 recoding, and I narrow the us_accidents
distinction to what the numbers still support.

New checks:
- entries that require damage, blanks against $0 by office, and the 2006 format split.
- blanks by year, and the EF4/EF5 segments at $0.
- LightGBM with the critic's LEAK-10 fixes (EG and ES speeds blanked, tornado
  durations blanked, `hurricane_category` out). The frame is rebuilt from the raw files. The date masks reproduce the
  shipped windows, for example 940,520 train and 55,961 test rows for 2025.

**Critic 1, LEAK-25 and us_accidents: the rule and the effect conceded; one sub-claim disputed; the precedent
distinction narrowed.**
- **Conceded: the rule.** LEAK-25 is a Must and takes no exception. The way out is an amendment by the curator. Without
  one, the outcome is retirement. Re-targeting to the positive amounts does not work: whether the office enters an
  amount above $0 is not known at the prediction point (USE-3).
- **Conceded: the three text fixes.**
  - Quote the curator's words in place of the AI gloss.
  - Mark the reading of the blank as an inference.
  - Change the acceptance reason to "part of the zeros are unestimated damage".
- **Conceded, and stronger than the critic put it: the effect.** Mean over the 3 windows:

  | features | RMSLE | ROC AUC for any damage |
  |---|---|---|
  | dummy | 3.90 | |
  | event type + month + time | 3.55 | 0.80-0.84 |
  | + the office | 2.71 | 0.935-0.945 |
  | all features (fixed) | 2.54 | 0.945-0.954 |

  - The office, added after type and time, gives 0.84 of the 1.36 total gain (62%). All the other features together
    add 0.16.
  - Among the positive entries, R^2 on log1p is -0.01 to 0.21 from type and time, 0.18 to 0.38 with the office, and
    0.37 to 0.46 with all features.
  - This run cannot separate the office's habit from regional cost levels. But the spread for the same event type
    (7% to 91% at $0 for Thunderstorm Wind; 0.2% to 96% for EG wind, blind reviewer) makes habit the likelier reading.
  - It follows that I withdraw "RMSLE 2.556 against 3.90" as evidence against us_accidents (my opening, point 3):
    most of that gap is the office.
- **Disputed: "the no-information entries became $0" (the 2006 to 2007 recoding).** The year 2006 holds both entry
  formats, so it allows a direct comparison:

  | 2006 rows | blank | $0 | floods blank |
  |---|---|---|---|
  | PDS (48,562) | 71.3% | 5.5% | 63.3% of 3,158 |
  | CSV (7,838) | 0.1% | 72.7% | 0 of 710 |

  - The directive says floods always get an amount. The PDS blank ignores that rule, so it is no "no information"
    box: it is how the old format wrote an empty field.
  - In the CSV format, floods have no blanks from 2008 on, against 15-28% blank for the other main types.
  - So the 2007 shift is a change of entry system, not the box recoded as $0. Rule: EV-2, a measurement on the data.
  - The fix is a narrower text change than the critic's: write "blank = the box: supported by the flood rule in the
    CSV format, not documented", rather than "contradicted by the 2007 recoding".
- **Narrowed: where the mix sits.**
  - In entries that require damage (Strong Wind, Lightning, Thunderstorm Wind below 50 kt), a $0 with no casualty and
    no crop damage is 3.1%, 0.6% and 0.3% of the entries.
  - In the quarter of offices that enter $0 on 91% of their Thunderstorm Wind, that rate is still 1.2% (0.0% in the
    bottom quarter).
  - So offices do cost damage when the entry rests on it. The mix sits in events entered by a criterion (severe wind,
    hail), where costing was not required. That locates where it is, but not which rows: dropping those events would
    drop most of the task. So it is no recovery under LEAK-25.
  - Two further facts:
    - Blanks rose from 7.3% to 22.7% of events over 2007-2025. The $0 share (r -0.63) and the positive share (r -0.67)
      both fell with them, so early $0 entries held some unestimated damage.
    - 7 of the 13 EF4/EF5 segments at $0 come from the Alabama outbreak of April 2011, where sibling segments of the
      same episode carry $20-50M. That is damage booked elsewhere: real, but clustered.
- **us_accidents, narrowed.** The facts that still set this case apart:
  1. The label is the quantity the narrowed use acts on (dollars of damage, a rough proxy). us_accidents failed USE-5
     on a delay code.
  2. There is signal beyond the subsets that reproduce the code (type, office, period):
     - RMSLE 0.16 lower in every window (2.41 / 2.63 / 2.59 against 2.56 / 2.79 / 2.77);
     - R^2 among the positives +0.08 to +0.19;
     - within one episode, where the office is fixed, Pearson on dollars of 0.31-0.34 against 0.27-0.32.

     In us_accidents the temporal split left almost nothing (log loss 0.48 against a 0.53 prior).
  3. The office practice is stable from one year to the next (r 0.958 from 2024 to 2025). us_accidents had a class
     that vanished inside one feed.

  This is a fact that sets the case apart (Consistent judgement, case 2), but it is smaller than my opening said. The
  curator weighs it.
- **What follows.**
  - The amendment I drafted would ship a benchmark of which about 60% of the gain is the office's reporting. The
    curator should see that number before amending. If adopted, it goes into the note and `fit_reason`.
  - Of the evaluation options, `mean_group_pearsonr` within `EPISODE_ID` cancels the office's level (one office per
    episode). It still has two caveats:
    - the all-$0 episodes drop out;
    - episodes where a model predicts a constant drop out too: 945-1,046 for the type/office model against
      1,193-1,276, so a model can skip hard episodes.

    It is a weighing call, not a fix of LEAK-25.
  - If the curator reads the 62% as us_accidents' mechanism, the result is `No`. I cannot rule that out with
    evidence.

**Critic 2, the use case and `fit_reason` (USE-5, USE-3, USE-8): conceded.**
- Same fix as my opening point 4: narrow the use case to the emergency manager, rewrite `fit_reason` to name the gaps
  (including tornado types from surveys), and add the damage-report fact to `known`.
- Filtering the hazards nobody assesses is a weighing call for the curator.

**Critic 3, EG speeds (LEAK-10 clause 2): conceded, and the ES check run.**
- ES is the same estimate for sustained wind: 1,164 entries with a damage figure, 1,154 of them High Wind. Blank them
  too (LEAK-2).
- My r3 and r4 runs already blank both EG and ES.

**Critic 4, tornado duration and `hurricane_category` (LEAK-10, LEAK-2, LEAK-6): conceded.**
- Blank the duration by event type and drop the category.
- Correct the Built bullet.

**Critic 5, the gap (SPLIT-10, Should): conceded.**
- Either option works. `gap=3` is the conservative one. A refit at the mid-January release also fits a use case that
  estimates after the storm.
- Reword `task_summary.split` either way.

**Critic 6, the metric reason (MET-1, MET-11): conceded.**
- Name Diaz & Joseph 2019, and say that the zero/positive call dominates the score.
- Keep `rmsle`, not `normalized_gini`.

**Critic 7, the quality items (P7): conceded.**
- Do the CLEAN-21, LEAK-19 and CLEAN-11 fixes and the four text fixes.

</details>

<details><summary>Critic rebuttal</summary>

**Critic: rebuttal to the advocate, noaa_storm_events_damage (2026-11-01)**

**Where we stand.** The advocate concedes every fix in my brief. We also agree on the condition that decides the
dataset: it ships only if the curator amends LEAK-25, and otherwise the verdict is `No`. I ran two checks on the
points still open.
- The first settles the LEAK-25 dispute in part.
- The second corrects one of the advocate's numbers without changing the conclusion that depends on it.

What remains open is one disagreement: how the LEAK-25 amendment is worded.

**Advocate 1, the split: conceded.** This is my point 5. We agree on `gap=3` and on the reworded `task_summary.split`.

**Advocate 2, signal after the leak fixes: conceded.** These are my points 3 and 4: blank the EG speeds and the
tornado durations, and drop `hurricane_category`. On the rows that exist only with damage (LEAK-37), I asked only for
the `known` text, and the advocate accepts that. My check c01 supports keeping these rows. In those types, offices
almost always enter a figure:
- Lightning without casualties: 98.3% positive, 1.6% at $0.
- Strong Wind without casualties: 85.0% positive, 4.5% at $0.
- Thunderstorm Wind with an EG speed under 50 kt: 98.1% positive, 1.5% at $0.

**Advocate 3, SEL-3 against us_accidents: conceded, with one number corrected.**
- *The correction.* The R^2 of 0.48 on the positives comes from the screening probe, which still had `SOURCE` and
  the EG speeds. My check c02 used the fixed features: EG blanked, tornado duration blanked, `hurricane_category`
  dropped. Trained and tested on the positive entries, R^2 is 0.276 (2025), 0.454 (2024) and 0.430 (2023). The
  event-type mean scores 0.160, 0.196 and 0.186.
- *Why I concede.* The signal beyond the type is real. The within-storm Pearson (0.397 against 0.278) holds the office
  fixed. The $0 share stays at 67-79% from 2007 on. These facts set this case apart from us_accidents, so I withdraw
  SEL-3 as an objection.
- *What I still ask.* The curator records these facts, with the corrected numbers, as the answer to the consistency
  check (principles, Consistent judgement, case 2).

**Advocate 4, the narrowed use case: conceded.** This is my point 2, and the remedy is the same.

**Advocate 5, the metric: conceded.** This is my point 6. Keep `rmsle`, and repair the reason: name Diaz & Joseph and
state the share of the error on the $0 rows. A within-storm score is the curator's weighing call, and we both reject
`normalized_gini`.

**Advocate 7, the quality items: conceded.** This is my point 7, with the same list.

**Advocate 6, LEAK-25: partly conceded, partly contested.**
- *Conceded, three things:*
  - My brief overstated the 2007 table. It shows that the code is a format convention. It does not show that the
    "no information" entries became $0: before 2007 a blank may have meant no damage.
  - My option (b), re-targeting to the positive entries, does not fix the problem cleanly, because the rows would
    still be selected on the label. I withdraw it, so the outcome is an amendment or `No`.
  - Where an office uses the blank, the blank is the box. Floods have no blanks from 2008 on.
- *Contested: "the source flags the unrecorded part and the definition drops it".* That holds only for the offices
  that use the flag. Check c01 compares offices with 50 or more entries, 2007-2025:

| entries | Spearman(blank share, $0 share) across offices | offices with blank < 2% and $0 > 30% |
|---|---|---|
| Hail | -0.83 (112 offices) | 28 |
| Thunderstorm Wind | -0.21 (114 offices) | 21 |

  For hail, offices that leave the field blank do not enter $0, and offices that enter $0 do not leave it blank. So
  each office picks one code for the same kind of event. In 28 offices the flag is all but unused for hail, and the
  $0 entries hold whatever part was never estimated. Hail and Thunderstorm Wind are about 41% of the shipped rows.
  In the types that need damage to be entered, the codes do not trade off this way (see Advocate 2).
- *Contested: "LEAK-25 has not decided a large task on its own".* LEAK-25 has no size clause. Under principles
  step 4, independent failures are not conflicts. This changes nothing, since the advocate accepts amendment or `No`.
- *Rule.* LEAK-25 (Must). Dropping the blanks is CLEAN-15, not a LEAK-25 recovery. The precedent checker reads it the
  same way: the rows are located by the missing label itself, and only in the offices that use the flag. The
  advocate's draft amendment rests on "a mix whose unrecorded part the source flags and the definition drops". On
  this data that describes a recovery that does not happen in a quarter of the offices.
- *Remedy.* The curator decides. If the rule is amended, the wording should not claim a recovery. For example: "a
  mix of 'no event' and 'not recorded' that follows a reporting unit shipped as a feature is kept with a note and fit
  approximate; the source's own flag is dropped where it is used." The dataset's note then gives the office numbers
  above, so a user knows the $0 code is the office's convention.

**Verdict after rebuttal.** Ship after changes, on one condition: the curator amends LEAK-25 with wording that does
not claim a recovery. Without the amendment, the verdict is `No`. The changes are the ones both briefs list: points 2
to 7 of my brief, the corrected positives number, and option (b) withdrawn.

</details>
