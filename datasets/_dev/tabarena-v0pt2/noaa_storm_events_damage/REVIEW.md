# noaa_storm_events_damage

**Outcome:** added. The AI recommends shipping it after changes: the re-review panel of 2026-11-06 under the exposure
rules (LEAK-41, MET-14 to MET-16) found no exposure, weight or offset to add and the split right; its changes that need
no decision are made (below), issues 7, 8, 10 and 11 are decided and applied (2026-11-08), so no question of that round is open; issues 12 to 14 of 2026-11-09 are decided and
applied (12: each county or zone, hazard and year counts once; 13: `SOURCE` stays dropped; 14: floor $10), and issue 15,
the $10M cap, waits for a decision. NOAA
NCEI's Storm Events Database, 2007-2025: 843,144 entries of the property damage an NWS office entered for one event in
one county or zone, 68% of them $0, for a state hazard-mitigation planner who estimates the damage of storm events
before it is assessed (Diaz and Joseph 2019); tested on the calendar years 2023-2025 with a 3-month gap, scored by the
mean Tweedie deviance at power 1.5 on the dollars, each county or zone, hazard and year counting once (by context; the
source has none; RMSLE until 2026-11-08). Under the rule on choosing test windows, rewritten on 2026-11-10, the AI
recommends keeping one-year windows with the 3-month gap (Horizon) and testing 2025, 2021 and 2017 instead of the three
newest years (issue 16, open; `dataset.py` is unchanged until you decide).

Validity:
* SEL-3 holds on the `Yes` of 2026-10-30. USE-1 and USE-5 hold with the planner as the actor (issue 5); USE-8: fit
  approximate, as a row is one event while the planner sums dollars per county and hazard, and a $0 mixes no damage
  with no estimate. USE-3: the rows are the events with a damage entry (an office leaves 0% to 98% of its events
  blank), which the task summary now says.
* LEAK-25 triggered, kept under the rule as amended on 2026-11-02: the office's $0 practice, with `wfo` a feature.
* LEAK-10 triggered and fixed: the wind speeds estimated from the damage (EG, ES) are blank; the tornado rating, path
  and end point, the reporter, the hurricane category, casualties and crop damage are dropped. D13 (issue 6) is applied
  as decided: `duration_hours` is blank for Tornado, Strong Wind and Heavy Rain, and since the re-review for Seiche too
  (below). The re-review read App. A again for every type: a seiche begins at flooding "resulting in a fatality, injury
  or damage" (Sec. 41), so its 51 durations are now blank too, an extension of D13's reading that both debaters accepted
  (say so if you want them kept); Dust Storm and Volcanic Ashfall join the types kept with a note; Flood (a threat to
  life or property) and Hurricane and Tropical Storm (the storm's direct effects) are recorded as judged outcome-free,
  and Flash Flood, one of whose onsets is damage to a building, is kept with a note since issue 11 (2026-11-08).
* LEAK-10 and the Cases row on spans: the note's premise that the damage-timed part of the kept spans "cannot be
  located row by row" does not hold. `magnitude_type` locates most of it (241,523 of 318,813 rows), and on those rows a
  stronger LightGBM gains +0.023 to +0.031 RMSLE from the span (12 of 12 seeds): issue 7, B, decided on 2026-11-08 and
  applied: these spans are blank, and the 78,843 rows still kept with a note are worth -0.02 to +0.12 RMSLE on their
  test rows (15 fits, median about +0.04), the measured Thunderstorm Wind spans gaining in every fit; under the
  declared deviance (issue 8) their worth has no consistent sign (median -5% of the deviance on their rows).
* SPLIT-9, SPLIT-10 and SPLIT-13 hold: a 3-month gap against a public lag of 75-80 days, no storm crosses a window, no
  training event ends after its cutoff, 98.6-99.6% of the test rows in a county or zone seen in training.
* MET-14, MET-15, MET-16 and LEAK-41 are not triggered: the target is one event's damage, not an amount accrued over a
  time at risk, so there is no exposure weight and no offset (county population does not scale with the damage); the
  cell weight of issue 12 gives each cell one vote and is no exposure.

Value: under the declared deviance (issue 8, 2026-11-08) the signal is weak and unstable. The task probe flags
`no_signal`, `drift_baseline` and `unstable` (TP-1, TP-2, TP-5): its families, fitted by squared error on the dollars,
all lose to the training mean (3,866 against 5,796 for the random forest). LightGBM fitted with the Tweedie loss at 100
trees scores 4,108-5,327, 2,048-2,453 and 788-838 (2023, 2024, 2025) against 4,453, 4,216 and 2,929 for the training
mean and 2,660, 2,301 and 1,740 for the mean per event type, so it beats the per-type mean clearly in 2025 only, and 400
or 1,500 trees score worse. Tuned per window with early stopping (issue 10, kept as shipped), it scores 3,463, 2,044 and
962 (3 seeds): it beats the training mean in every window and the per-type mean in 2024 and 2025, and loses to it in
2023 within noise (bootstrap SE 1,580 for a difference of +802); a GLM on event type and month beats the per-type mean
in all three windows (2,553, 2,130, 1,598). Under RMSLE (until 2026-11-08) untuned LightGBM scored 2.67, 2.93 and 2.94
(2025, 2024, 2023) against 4.05, 4.28 and 4.20 for a constant, and methods spread (TP-3). MET-11: the deviance by
context. MET-1: the reason names the planner, who sums expected dollars, which RMSLE does not score. MET-13: floor $10,
the smallest damage the source records (issue 14; $1 until 2026-11-09).

Quality: LEAK-19 (918 double entries dropped), CLEAN-21 (`magnitude` split into wind speed and hail size), CLEAN-11 (24
impossible wind speeds, all estimates, blank). EV: the counts left from before issue 2's drop are restated on the
shipped rows, and the kept spans' worth is the measured range, since issue 7 measured on the spans that stay (-0.02 to
+0.12 RMSLE over 15 fits, median about +0.04) and since issue 8 on the declared deviance (no consistent sign), no
longer "+0.012 to +0.021, an upper bound".

Weighed: size +; the NWS directive and a public-domain source +; an honest temporal split +; approximate fit -; the
office's $0 convention in the label -; a duration the damage partly times, kept with its worth noted -; under the
declared deviance a tuned model beats the mean per event type in two windows of three, the third within noise -.

Not issues here: the amendment of LEAK-10 for spans that the panel asked for (a third clause tied to the test for
located cells, with heart_failure's `time` as the counter-case on size) is cross-dataset item X4 of the working copy's
REVIEW.md. The mediator asks to record Andrej's release of D13 (the study's decision table assigned D13 to him) before
merging; not needed on the AI's reading: you took over this round as main reviewer on 2026-11-06 and decided D13
yourself (CC of 2026-11-06).

For the curator: issue 15 (the $10M cap, measured on the new unit); issues 12, 13 and 14 are resolved (2026-11-09).

Changes made after the re-review panel (AI, 2026-11-06), no decision needed (`dataset check`: 0 errors, 0 warnings):
the 51 Seiche durations are blank by type, as for Strong Wind; the kept-span note drops "cannot be located row by row"
and "an upper bound", gives the measured worth (-0.01 to +0.08 RMSLE on the five kept types' test rows over 15 fits,
median about +0.03) and the share `magnitude_type` locates, names Dust Storm and Volcanic Ashfall, and records Flood,
Flash Flood, Hurricane and Tropical Storm as judged outcome-free; the metric reason and the reason for dropping the
unassessed hazards name the planner; the task summary says the rows are the events with a damage entry and gives
4.5-5.0% of the test rows for the types entered only with damage, now with hail under 3/4 inch and dust devils; the
counts are restated (918 double entries, 30.1% zone rows, 7,697 codes, 140,270 episodes, 252,451 EG and 1,151 ES
entries); issue 6 says "seven" for "six" and points to issue 7; the record's `No Good Target / Scientific Discovery`
marker, a screening concern that issue 5 settled, is removed. One change departs from the
mediator's list: the panel read Hurricane and Tropical Storm as timed by "damage or" a wind criterion, but that is
App. A's wording for their marine types (Sec. 34, 39), which the data drops; the land types begin with "the direct
effects" of the storm (Sec. 25, 49), so they are recorded with the floods as outcome-free, not kept with a note. Your
CC line of 2026-11-06 keeps its words ("read App. A for every type", "+0.012 to +0.021"); the notes and the record say
what the re-review corrected.

Earlier changes: after the panel of 2026-11-01 the estimated wind speeds and the tornado durations were blanked, the
hurricane category dropped and the gap set to 3 months; on 2026-11-03 the unassessed hazards were dropped (issue 2) and
the use case became the planner's (issue 5); on 2026-11-06 D13 (issue 6); on 2026-11-08 the duration blank on the
241,523 wind entries the first report gives as damage (issue 7, B), and the target in dollars scored by the mean Tweedie
deviance with a $1 floor (issue 8, B); then issue 10 kept that metric with the tuned results in the notes, and issue 11
moved the Flash Flood duration to the spans kept with a note (no data change; `dataset check`: 0 errors, 0 warnings).

**Main points:** Open since 2026-11-10: sign off the one-year windows with the 3-month gap (Horizon), and test 2025,
2021 and 2017 instead of 2023-2025 (issue 16)? Resolved on 2026-11-10 (Andrej): issue 15, the damage stays uncapped, the
planner's sum with the catastrophes in; uncapped the score orders the methods at Kendall's W 0.62 across the test
years and separates tuned LightGBM from a mean per event type only in 2025, stated in the notes as the noise of the
task (the task's representation comes before how well methods separate). Issues 2 to 14 are resolved; on
2026-11-09 issue 12 made each county or zone, hazard and year count once (each entry weighs 1 over its cell's
entries), issue 13 kept `SOURCE` dropped and issue 14 set the floor to $10. On 2026-11-08 issue 7 blanked the duration on the wind entries the
first report gives as damage, issue 8 made the target the dollars, scored by the mean Tweedie deviance with a $1 floor,
issue 10 kept that metric with its signal stated (tuned LightGBM beats the mean per event type in 2024 and 2025, not in
2023, within noise), and issue 11 moved the Flash Flood duration to the spans kept with a note. Made without a decision,
say if you disagree: the 51 Seiche durations are blank, an extension of D13.

**Verdict (2026-11-10, Andrej):** ship (review page of 2026-11-10).

**Horizon:**

* **Verdict:** keep the one-year windows with a 3-month gap (high confidence): the score counts each county or zone,
  hazard and calendar year once, and the gap is the measured publication lag.
* **Length:** one calendar year, a model refit on 1 January that estimates the damage of that year's reported events.
  The source defines no task, and NCEI releases monthly, so the yearly refit is ours; it follows the planner, who
  decides per jurisdiction and hazard on the loss expected in a year
  ([44 CFR 201.6](https://www.ecfr.gov/current/title-44/chapter-I/subchapter-D/part-201/section-201.6); FEMA's
  [National Risk Index](https://hazards.fema.gov/nri/) gives an expected annual loss per county and hazard). The score
  counts each county or zone, hazard and year once, and a cell's entry count is known only once its year is over, so
  a window shorter than a calendar year would cut the cells. A year also holds every storm season.
* **Gap:** 3 months against the publication lag: a Storm Data month is certified "no later than 60 days after the end
  of the month" (NWSI 10-1605, Sec. 3), NCEI's files are "updated monthly with up to a 120 day delay possible"
  (C00510), and in archived releases a month first appears complete 75-80 days after its end, so a refit on 1 January
  holds the events through September. Damage estimates revised after that are not dated in the source.
* **Time frame:** entries from 2007, the first full year of the current entry format, to December 2025. One-year
  windows that keep half the entries for training run from 2017 to 2025 (nine); today's are 2023 to 2025. Across the
  years the share of events without a damage figure rises (7.3% in 2007, 22-24% in 2022-2025), the offices' $0
  practice drifts, and the mean damage per entry ranges from $97,000 (2025) to $1.94M (2017).
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | A | One year, 3-month gap (implemented) | calendar years, each trained on the events through September of the year before: 9 candidates above the floor, 2017 to 2025 | the score's year cells stay whole; every storm season in a window; the planner decides on the loss expected in a year; the gap is the measured publication lag | the yearly refit is ours (NCEI releases monthly) |
  | B | Two years | four candidates keep half the entries for training: 2024-2025, 2022-2023, 2020-2021 and 2018-2019 (train shares 88.9%, 78.5%, 69.0% and 58.5%) | two hurricane seasons per window | a refit every two years where the source is released monthly and the planner works by the year |
  | C | Half a year | half-year windows, a refit twice a year | a refit closer to the events | each window tests one or two storm seasons; splits the year cells the score counts once, so the score's unit would have to change |
  | D | A quarter | quarterly windows, a refit every quarter | a refit closer to the events | each window tests one or two storm seasons; splits the year cells the score counts once, so the score's unit would have to change |

* **Recommendation:** A: a year keeps whole the year cells the score counts once and matches the planner's expected
  annual loss, and the gap is the measured publication lag. **Decision:** A, B, C or D?

**Issues for Andrej and Lennart:**

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

6. **Blank the duration where the damage draws an event's span?**

   * **Problem:**
     - NWSI 10-1605 App. A sets the begin and end of an event by type, and for some types the damage draws them.
     - Strong Wind runs while the wind causes "a fatality, injury, or significant damage" (Sec. 45), and Heavy Rain is
       timed from "When the heavy rain that led to damage began" (Sec. 21).
     - The definition blanked only the tornado durations, so the duration of the other damage-timed types was a
       feature[^6a].
   * **Background:** Thunderstorm Wind runs from "When damage first occurred or winds 50 knots (58 mph) or greater
     were first reported" (Sec. 46), High Wind likewise with its wind criteria (Sec. 24), and Coastal Flood, Lakeshore
     Flood and Storm Surge/Tide from "When the water level began to cause damage or flooding" (Sec. 4, 27, 44). The
     panel's column audit of 2026-11-01 quoted the Thunderstorm Wind entry alone and judged the spans first-report
     facts; the exposure study of 2026-11-05 read the entry of every type.
   * **Effect on the task:** for Strong Wind and Heavy Rain (39,079 rows, 4.6%) the span is a record of the outcome.
     For the five other types (318,813 rows, 37.8%) it is partly the damage's and partly a wind or flooding criterion,
     and Storm Data does not record which set a given span (on 2026-11-06 the re-review found that `magnitude_type`,
     a feature, locates most of the spans the damage set: issue 7).
   * **Experiments:** untuned LightGBM on the shipped splits (trained from 2007 with the 3-month gap), change in
     RMSLE, mean of 4 bagging seeds (SD in brackets):

     | Duration blank on | against | Rows scored | 2023 | 2024 | 2025 |
     |---|---|---|---|---|---|
     | all seven damage-timed types | the definition before | the seven types | +0.013 (0.013) | +0.016 (0.017) | +0.021 (0.018) |
     | the five kept types too | the shipped definition | the five types | +0.021 (0.016) | +0.018 (0.019) | +0.012 (0.030) |
     | Strong Wind and Heavy Rain | the definition before | those two types | -0.009 (0.035) | -0.018 (0.034) | -0.046 (0.057) |

     The study's run, trained from 2016, put the first row at +0.020 to +0.038. A model gains about 1.3 over a
     constant, so the column is a small part of the skill, and on Strong Wind and Heavy Rain it is worth nothing.
   * **Consistency:** the tornado duration was blanked by event type on 2026-11-03 for the same reason, a span the
     damage survey sets; the rule on spans the outcome sets, adopted the same day as this decision, names this column
     as its case[^6b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Tornado only | the duration stays a feature for the seven other damage-timed types | no change; keeps the wind and flood signal | on Strong Wind and Heavy Rain the span records the damage |
     | B | Blank Strong Wind and Heavy Rain too (implemented) | blank for the three types the outcome alone times; the five others keep it, with a note giving its worth | removes the spans the damage alone draws, at no measured cost; keeps +0.012 to +0.021 on the five types | the five types' spans are partly the damage's, a leak kept with a note |
     | C | Blank all seven damage-timed types | blank wherever the damage can set the span | no span the damage may set stays | loses +0.013 to +0.021 on the seven types, part of it a wind or flooding criterion the first report holds |
     | D | Drop the column | no duration for any type | simplest | also loses the duration of floods, winter storms and the types no damage times |

   * **Recommendation:** B: blank where the outcome alone draws the span, keep it with its worth noted where a
     criterion without the damage can draw it too, as the rule on spans says[^6b]. **Decision:** A, B, C or D?

   [^6a]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target
     away; a part, a consequence or another encoding of the target is out.
   [^6b]: **LEAK-10, LEAK-37** Cases row "A span or extent whose start or end the source defines by the outcome"
     (Lennart, 2026-11-06): read the source's definition of the start and end; where the outcome alone draws it, blank
     or drop it for those types; where it is drawn by the outcome or an outcome-free criterion, keep it with a
     `Potential leak, kept on purpose:` note giving its worth.

   **Resolved (2026-11-06, Lennart):** B (decision D13 of the exposure study,
   [#51](https://github.com/TabArena/data-foundry/issues/51)). `duration_hours` is blank for Tornado, Strong Wind and
   Heavy Rain (62,694 rows, 7.4%) and kept for Thunderstorm Wind, High Wind, Coastal Flood, Lakeshore Flood and Storm
   Surge/Tide with a `Potential leak, kept on purpose:` note: worth +0.012 to +0.021 RMSLE on their test rows and
   +0.001 to +0.015 on all rows; the blank on Strong Wind and Heavy Rain costs nothing (-0.009 to -0.046 on their rows).
   The notes gain the exposure paragraph: the source gives no exposure, county population does not scale with the
   damage (Spearman -0.14 to +0.05 among positive entries), so no offset, and storms whose entries share one figure
   hold round office values, not split totals. Supersedes the definition shipped on 2026-11-03 (Andrej), which blanked
   the tornado durations only. `dataset check`: 0 errors, 0 warnings.

7. **Blank the duration also on the wind entries the first report gives as damage?**

   * **Problem:**
     - D13 kept the duration of Thunderstorm Wind and High Wind with a note because Storm Data does not record
       whether the damage or a wind criterion timed a span, but `magnitude_type`, known at the first report, marks the
       entries whose speed the office estimated from the damage (EG, ES), and on nearly all of them nothing but the
       damage can have timed the span[^7a].
     - Strong Wind was blanked the same day for that fact, and these entries, with 435 Thunderstorm Wind entries
       measured under 50 kt, are 241,523 of the 318,813 rows whose duration was kept (75.8%).
     - On those rows the span carries a small but consistent gain under a stronger model, and where other datasets
       could locate such cells they blanked them rather than keep them with a note[^7b].
   * **Background:**
     - Appendix A of the NWS directive times a Thunderstorm Wind entry from "When damage first occurred or winds 50
       knots (58 mph) or greater were first reported" to "When damage ended or winds of 50 knots (58 mph) were last
       reported" (Sec. 46), and High Wind likewise with its wind criteria (Sec. 24).
     - An EG or ES entry carries a speed the office estimated from the damage, which the definition already blanks.
       Matched to the real-time Local Storm Reports of 2024, 94.4% of the EG Thunderstorm Wind entries had a first
       report "TSTM WND DMG" without a speed, so no wind of the criterion was reported; the other 5.6% had a speed in
       the first report, so the blank locates these spans closely, not exactly.
     - A Thunderstorm Wind entry measured under 50 kt met no wind criterion and enters Storm Data only with damage
       (92% of the 435 have property damage).
     - The blank would follow `magnitude_type` and the event type, both features, so a missing duration would tell a
       model nothing it cannot already read.
   * **Experiments:** the mediator's rerun on the shipped splits: the change in RMSLE when the duration is blanked on
     these 241,523 rows (positive: the span carried a gain), mean of 4 paired seeds (SD in brackets):

     | Model | Rows scored | 2023 | 2024 | 2025 |
     |---|---|---|---|---|
     | untuned LightGBM, 400 trees (the note's) | these rows | +0.001 (0.022) | +0.013 (0.028) | +0.020 (0.024) |
     | untuned LightGBM, 400 trees | all rows | +0.001 | -0.002 | +0.008 |
     | LightGBM, 1,500 trees, 127 leaves | these rows | +0.031 (0.009) | +0.023 (0.005) | +0.030 (0.015) |
     | LightGBM, 1,500 trees, 127 leaves | all rows | +0.004 | +0.015 | +0.019 |

     - The stronger model gains on these rows with 12 of 12 seeds, 3 to 4 seed SDs; the note's model with 9 of 12,
       within one SD.
     - A model gains about 1.3 over a constant, so even the largest figure is a small part of the skill.
   * **Consistency:**
     - Your keep differs from Strong Wind, blanked by D13 the same day because its span runs from the first to the
       last damage (the domain practitioner: "All I would have is the time of a damage report, not an end"), and from
       zillow_prize and melbourne_housing_market, which blanked the late cells they could locate (2026-10-21), as
       frempl_french_motor_personal_line did for its located early ends[^7c].
     - medical_facility_operational_data kept a part it could not locate, within about two seed SDs; here the part is
       located, and the stronger model's gain is 3 to 4 seed SDs.
     - Item X4 of the working copy's REVIEW.md would write B's reading into the leak rule[^7f] (blank the part of a
       span that can be located, keep the rest with its worth only when small); D is the reverse, so B goes with taking
       X4 and D with declining it.
     - So what sets an EG wind span apart from a Strong Wind span? The ways out are the options below: nothing, treat
       them alike (B); a fact written down that sets them apart (A; the advocate's candidate, the first report's clock
       times, would reopen the Strong Wind blank); all five types alike (C); or the rule read type by type (D)[^7d].
   * **Panel:**
     - The advocate keeps them: the first reports hold the damage report's time, the rule on inputs the actor knows
       admits that the first report says whether damage was seen, and a blank removes a first-report fact[^7e].
     - The critic blanks them: the first report says when damage was seen, not how long it went on, and the end is
       the preparer's merge of the damage reports, the fact for which Strong Wind was blanked.
     - Before the rerun both set the same tie-breaker, blank if four seeds show a consistent gain on these rows; the
       rerun met it under the stronger model, and the mediator recommends the blank.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep, the note corrected (implemented) | the duration stays on these rows; the note gives their share and the column's measured worth | keeps a time the first report holds; D13 unchanged | keeps spans only the damage can have timed while Strong Wind's is blank; departs from the located-cells cases |
     | B | Blank these rows | `duration_hours` blank on the EG and ES entries of Thunderstorm Wind and High Wind and on Thunderstorm Wind measured under 50 kt (241,523 rows); the note keeps the measured-wind, dust, ash and flood spans, with their worth measured again | treats these spans like Strong Wind's; follows the located-cells cases; the blank follows features, so no new marker | loses +0.001 to +0.031 RMSLE on these rows; rests on the directive's wording, and 5.6% of the EG entries had a speed in the first report |
     | C | Blank every kept type | the duration blank for the five wind and flood types (318,813 rows) and for Dust Storm and Volcanic Ashfall | no span the damage may have timed stays | loses the measured-wind and flood spans, which the first report or a tide gauge gives |
     | D | Amend the rule on spans | the rule reads a span type by type, never within a type; nothing changes here | one reading for every dataset | against the smallest fix and the located-cells cases; the Strong Wind contrast stays |

   * **Recommendation:** B: a feature locates these rows, on them nothing but the damage can have timed the span, as
     for Strong Wind, and the stronger model gains from the span with 12 of 12 seeds, which meets the tie-breaker both
     debaters set. A only with the fact that sets an EG span apart from a Strong Wind span written down. **Decision:**
     A, B, C or D?

   **Notes for the AI:** On B: in `_clean`, blank `duration_hours` where `EVENT_TYPE` is Thunderstorm Wind or High
   Wind and `MAGNITUDE_TYPE` is EG or ES, and where `EVENT_TYPE` is Thunderstorm Wind, `MAGNITUDE_TYPE` MG or MS and
   `MAGNITUDE` under 50 (241,523 rows; the mediator's variant `blankA` in `eg_rerun.py`, run folder of 2026-11-06);
   measure the worth of what is left of the column on the kept types' test rows again (the claim auditor's 5 set-ups
   by 3 windows) and write it into the kept-with-note bullet in place of -0.01 to +0.08, with the EG and ES sentence
   turned into the blank's reason in the "Blanked" bullet; add the rows to `changes` and the `known` wording; re-run
   `dataset check` and the leak probes; a CC line with the call; the main session updates the LEAK-10 / LEAK-37 Cases
   row on spans in leak_checks.md. On A: the curator's fact goes into the kept bullet and a CC line; if it is the
   first report's times, reopen the Strong Wind blank with an issue of its own. On D: the main session amends the
   Cases row (date, curator, this case) and closes X4 as declined; on B, X4 is applied with this case named. The
   rule: LEAK-10 (Must) with its second clause and LEAK-6 (Must) over LEAK-7 (Should); the advocate's ground is
   LEAK-37 (Must).

   [^7a]: **LEAK-10** (Must): a feature holds only what existed at the prediction point and never gives the target
     away; a part, a consequence or another encoding of the target is out. The **LEAK-10, LEAK-37** Cases row on
     spans (Lennart, 2026-11-06): where the outcome alone draws a span, blank or drop it for those types; where it is
     drawn by the outcome or an outcome-free criterion, keep it with a `Potential leak, kept on purpose:` note giving
     its worth.
   [^7b]: **LEAK-10**, second clause (amended 2026-10-26, Lennart): late cells that can be located row by row are
     blanked (zillow_prize, melbourne_housing_market, aeolus_1m); values that cannot be located stay with a note only
     when the part that can be traced shows no gain. **LEAK-6** (Must): measure before acting; a confirmed leak goes
     even when small. **LEAK-7** (Should): the smallest fix that keeps a valid signal. The time-on-risk Cases row
     (amended 2026-11-06, Lennart): "where the data locates the cut row by row, fix it".
   [^7c]: Located and blanked: zillow_prize and melbourne_housing_market (2026-10-21);
     frempl_french_motor_personal_line, whose dates locate the early ends (2026-11-02, 2026-11-06). Not located and
     kept with a note: medical_facility_operational_data (Lennart, 2026-11-05). Not located and dropped:
     distribution_transformers_at_cauca_department (2026-10-21).
   [^7d]: principles.md, "Conflicts between rules": "Treat like cases alike: a precedent with the same facts is
     followed unless a fact sets the new case apart." "Consistent judgement, the curator's included", case 2: a
     precedent with similar facts decided the other way; the ways out are the fact that sets the case apart, the case
     treated like the precedent, the precedent reopened, or the rule amended. A Must has no exceptions; anything else
     is an amendment ("Exceptions and amendments").
   [^7e]: **LEAK-37** (Must; applies **USE-6**): an input the actor knows at the prediction point is not a leak.
   [^7f]: **LEAK-10** (Must): item X4 proposes a third clause for spans drawn by the outcome or an outcome-free
     criterion, tied to the second clause's test: blank the part that can be located; keep the rest with a note giving
     its worth only when that worth is small (heart_failure's `time`, dropped on its size, the counter-case).

   **Resolved (2026-11-08, Lennart):** B. `duration_hours` is blank on the EG and ES entries of Thunderstorm Wind and
   High Wind and on Thunderstorm Wind measured under 50 kt (241,523 rows, as the issue counted; the blank costs +0.023
   to +0.036 RMSLE on them under the larger LightGBM, 12 of 12 seeds), superseding D13's keep on these rows (issue 6).
   The note keeps the measured-wind, dust, ash and flood spans (78,843 rows), worth -0.02 to +0.12 RMSLE on their test
   rows over the re-review's 15 fits, the measured Thunderstorm Wind spans +0.03 to +0.18 in 30 of 30 fits;
   `dataset check`: 0 errors, 0 warnings.

8. **Keep RMSLE, or score the Tweedie deviance on the dollars?**

   * **Problem:**
     - Since issue 5 the actor is a planner who sums expected dollars per county and hazard, while RMSLE scores each
       event's order of magnitude and is minimised by a geometric mean (the best constant for 2024 is $16 against a
       mean of $355,555), and issue 3 kept RMSLE for the earlier triage actor[^8a].
     - The domain practitioner would score the mean Tweedie deviance at power 1.5 on the dollars, the usual score for
       zero-heavy, heavy-tailed amounts, which the mean minimises, and both debaters agreed to switch only if the two
       pick different models.
     - The mediator's probe found that they pick different models in all three windows, which meets that condition,
       but the deviance's picks (a mean per event type in 2023, the least capacity in every window) may come from a
       few large events rather than from a better model, so this is a weighing call between the label's precision and
       the planner's sum[^8b].
   * **Background:**
     - The label is coarse: 44% of the positive figures have one significant digit, and offices enter round values
       ($1,000, $5,000, $10,000), so it supports an order of magnitude and little more.
     - On raw dollars 0.1% of the rows hold 99.94% of the squared deviation; the Tweedie deviance damps that tail far
       more than a squared error does, but much less than a log.
     - No source metric exists: Diaz and Joseph (2019) report several metrics, on tornadoes only and a random split.
     - Under the deviance the target would ship in dollars, not on the log scale, since a deviance scores the mean on
       the original scale[^8c].
   * **Experiments:** the mediator's probe on the shipped splits: candidates a mean per event type and untuned
     LightGBM (100 or 400 trees of 31 leaves, or 1,500 trees of 127 leaves), each trained for each metric (squared
     error on the log for RMSLE, a Tweedie loss on the dollars for the deviance), one seed, no tuning or early stopping;
     in brackets the winner's score, RMSLE or the mean Tweedie deviance, lower is better:

     | Window | RMSLE picks | The deviance picks |
     |---|---|---|
     | 2023 | LightGBM, 400 trees (2.959) | the mean per event type (2,660), ahead of LightGBM, 100 trees (3,828) |
     | 2024 | LightGBM, 400 trees (2.944) | LightGBM, 100 trees (2,040) |
     | 2025 | LightGBM, 1,500 trees (2.675) | LightGBM, 100 trees (762) |

     - Under the deviance more capacity scores worse in every window (100 trees, then 400, then 1,500), which can be
       a score the tail decides or an untuned Tweedie fit that overfits; the probe cannot tell which.
     - The models trained for RMSLE sum to 0.05% to 10% of the actual dollars.
   * **Consistency:** diamonds and onlinenewspopularity score RMSLE by context, neither with a mass at zero;
     pricing_game_2017_french_mtpl scores the mean Tweedie deviance at power 1.5 for an insurer's expected claim
     cost[^8d].
   * **Panel:**
     - For RMSLE (the advocate; the domain practitioner, though they proposed the deviance): the label supports an
       order of magnitude, a score on dollars is decided by a few hurricanes and floods, and the practitioner "could
       pick a model by it".
     - For the deviance (the critic; the domain practitioner, who proposed it): the planner plans with summed expected
       dollars, which RMSLE does not score, and issue 3 chose the metric for the earlier actor.
     - The mediator leans to RMSLE, reading the deviance's preference for a mean per event type and for less capacity
       as tail-driven noise, and leaves the weighing to you.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | RMSLE (implemented) | as now; the reason adds that the deviance was probed, picks other models, and why RMSLE stays | fits the label's precision; a few large events do not decide it | scores the order of magnitude, not the planner's sum; the best constant is $16 |
     | B | The Tweedie deviance on the dollars | the mean Tweedie deviance at power 1.5 with a floor of $1; the target ships in dollars | scores the expected dollars the planner sums | in the probe it ranks a mean per event type first in 2023 and penalises capacity; large events weigh heavily |
     | C | Probe again first | tuned Tweedie fits with early stopping on the three windows, then A or B | settles whether the deviance's picks are noise | a probe to run; the decision waits |

   * **Recommendation:** A, the mediator's lean: the label holds an order of magnitude and little more, and in the
     probe the deviance prefers a mean per event type and the least capacity, which reads as noise from the tail rather
     than a better model for the planner; so the debaters' condition is met, but not, on this reading, by a better
     model; C if you want that reading tested before you decide. **Decision:** A, B or C?

   **Notes for the AI:** On A: add to the metric reason one sentence, e.g. "Probed against the mean Tweedie deviance
   at power 1.5 on the dollars (each candidate trained for each metric, 3 windows, 2026-11-06): the two pick
   different models in 3 of 3 windows, the deviance preferring a mean per event type (2023) or the least capacity;
   RMSLE stays for the label's precision (<curator>, <date>)." On B: the target ships as dollars
   (`property_damage_usd`, no `target_transform`: CLEAN-16), the metric is `Metric.from_context(
   "mean_tweedie_deviance", params={"power": 1.5, "min_prediction": 1.0}, reason=...)`; rewrite `predicted`, the
   target bullet, the accepted warning and the metric reason; re-run `dataset check` and the task probe. On C: rerun
   the mediator's `met_probe.py` (run folder of 2026-11-06) with tuned Tweedie LightGBM and early stopping on a slice
   of each training side, then put A or B again. The rules: MET-1 (Must), MET-11 (context) and the Tensions row on
   the source's metric against a better metric (no source metric here).

   [^8a]: **MET-1** (Must): the declared metric scores the real task, the decision of the use case at the unit the
     actor acts on, the way a practitioner would have chosen a model for it. **MET-11** (Must), origin "context":
     the source defines no metric, the task makes one obvious and the reason says why. Issue 3 (Andrej, 2026-11-03)
     kept RMSLE for ranking a storm's counties; issue 5 (Andrej, 2026-11-03) made the actor the planner, "data, split
     and metric unchanged".
   [^8b]: principles.md, Tensions, "The source's metric against a better metric for the same goal": without a source
     metric, the metric the task makes obvious; which framing of this task's decision that is, the rules leave to the
     curator.
   [^8c]: **CLEAN-16** (Should; amended 2026-11-06, Lennart): "A target scored by a deviance, a rate included, ships
     untransformed: the deviance scores the mean on the original scale, which a fit on the log scale misses".
   [^8d]: diamonds (Lennart, 2026-10-21): "a price's error matters relative to the price, so `rmsle`";
     pricing_game_2017_french_mtpl: the mean Tweedie deviance at power 1.5, "Chosen over the Gini by the curator
     (Andrej, 2026-11-03)".

   **Lennart (2026-11-08, change):** Option B: The Tweedie deviance on the dollars.; i think this is a similiar discussion that we should start from the right metric and maybe ignore prior claims if they dont match the task

   **Resolved (2026-11-08, Lennart):** B. The target ships in dollars (`property_damage_usd`) and is scored by the mean
   Tweedie deviance at power 1.5 with a $1 floor, two orders below the cheapest event type's training mean ($909, Dense
   Smoke) rounded down, superseding Andrej's RMSLE (issue 3, A, and its check under issue 5). Under it the task probe
   flags `no_signal`, LightGBM fitted with the Tweedie loss beats the mean per event type clearly in 2025 only, and the
   Flood and Flash Flood durations carry much of a model's skill; `dataset check`: 0 errors, 0 warnings.

10. **Under the deviance on the dollars, does the task still beat a mean per event type?**

   * **Problem:**
     - Under the mean Tweedie deviance on the dollars, shipped since issue 8, the task probe flags no signal, as all its
       families, fitted by squared error, lose to the training mean[^10a].
     - Tuned per window with early stopping, LightGBM with the Tweedie loss beats the mean damage per event type in 2024
       and 2025 but not in 2023, where a few large events decide every score and no difference can be told from noise.
     - Capping each entry's damage at $10M gives a model that beats the per-type mean in every window and seed, but it
       scores another target than the dollars Lennart chose, and caps were declined elsewhere[^10b].
   * **Background:**
     - The tail decides the score: 0.1% of the 2024 test rows hold 74% of its dollars, the largest single entries are $1
       billion, and a cap at $10M, which binds on 1,761 entries, removes 87% of all dollars.
     - In 2023 the bootstrap standard error of the tuned model's difference to the per-type mean is 1,580, twice the
       difference itself; in 2024 and 2025 the difference is 2 and 26 standard errors over test rows (0.8 and 18 over
       test days).
     - The probe's families are untuned and fitted by squared error on the dollars, so 44% of the linear model's and
       LightGBM's predictions fall at the $1 floor; its flag is a question until tuned models are checked, which this
       issue does[^10c].
   * **Effect on the task:** a benchmark on this metric ranks methods mostly by how they treat the few largest events of
     each test year; in 2023 a mean per event type beats every tuned model, while in 2025 the tuned model halves its
     deviance.
   * **Experiments:** LightGBM with the Tweedie loss at power 1.5, tuned per window over 24 configurations (learning
     rate, leaves, rows per leaf, feature fraction) with early stopping on the last 12 months of the training side,
     refit on the whole side, 3 seeds; scored by the declared metric, lower is better; in brackets the bootstrap
     standard errors of the difference over test rows / test days (2,000 resamples):

     | Window | Training mean | Mean per event type | GLM: event type and month | Tuned LightGBM, 3 seeds | Tuned minus per-type mean |
     |---|---|---|---|---|---|
     | 2023 | 4,453 | 2,660 | 2,553 | 3,463 (2,997 to 4,270) | +802 (1,580 / 1,617) |
     | 2024 | 4,216 | 2,301 | 2,130 | 2,044 (1,968 to 2,101) | -257 (129 / 314) |
     | 2025 | 2,929 | 1,740 | 1,598 | 962 (926 to 1,005) | -777 (30 / 44) |

     The same tuning on alternative targets and metrics, the tuned model against the per-type mean on each one's own
     score (relative difference; z over test rows / test days):

     | Alternative | 2023 | 2024 | 2025 |
     |---|---|---|---|
     | Deviance at power 1.5 on the damage capped at $10M | -20% (-7.2 / -4.2) | -18% (-10.7 / -4.6) | -32% (-18.4 / -11.7) |
     | Deviance at power 1.7 on the dollars | +79% (0.9 / 0.8) | -16% (-5.3 / -1.8) | -38% (-20.0 / -15.2) |
     | Deviance at power 1.9 on the dollars | -8% (-2.0 / -1.7) | -3% (-0.7 / -0.5) | -15% (-9.3 / -8.4) |
     | RMSLE, the metric before issue 8 (untuned LightGBM, 400 trees, against the per-type mean of the log) | 2.96 against 3.83 | 2.93 against 3.85 | 2.72 against 3.62 |

     - The GLM with event type and month, a baseline a planner could build, beats the per-type mean in all three windows
       (-4%, -7%, -8%; within noise in 2023), and in 2023 it beats the tuned LightGBM too; with event type and state it
       is worse than the per-type mean in 2023 and 2024.
     - Under the cap every seed of every window beats the per-type mean; under a power of 1.7 or 1.9 the signal stays
       uneven across windows.
   * **Consistency:**
     - forest_fires (R^2 0.013) was kept because a strong model beats the mean on most folds, a small but real
       signal[^10a].
     - fremtpl2 keeps its claim count uncapped ("A cap is a modelling choice of the literature, not a shown error"), and
       frempl_french_motor_personal_line keeps the claim that decides a fold, measuring a capped score only as
       evidence[^10b].
     - houses drops the rows whose price its source capped at 500,001, calling the capped target censored; no dataset of
       the working copy was found that caps its own target.
   * **Panel:** none; raised when issue 8 was applied.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | The deviance on the dollars (implemented) | as shipped; the notes give the signal by window, with the tuned results | the planner's sum of expected dollars, as issue 8 decided; tuned models beat the training mean in every window and the per-type mean in two | in 2023 no tuned model beats a mean per event type; a few events per year rank the methods |
     | B | Back to RMSLE | the target as log1p and RMSLE, as before issue 8 | a clear signal in every window (2.7 to 3.0 against 3.6 to 3.9 for the per-type mean) | scores the order of magnitude, not the planner's sum; reverses issue 8 |
     | C | The deviance on the damage capped at $10M | the target min(dollars, $10M), the same metric and floor; the notes say what the cap leaves out | a signal in every window and seed (-18% to -32% against the per-type mean); still the expected dollars of all but the largest entries | removes 87% of the dollars, the catastrophes; a cap is our modelling choice, which fremtpl2 declined and houses treats as censoring; tested at one value |
     | D | Retire | the task leaves the collection | no task whose signal depends on the test year | tuned models beat the per-type mean in two windows and the training mean in all three, and B and C have a clear signal |

   * **Recommendation:** A: a small but real signal is no reason to retire, tuned models beat the per-type mean in 2024
     and 2025 and the training mean in every window, and 2023's loss is within noise; the instability is a fact of the
     planner's sum, which issue 8 chose, and a cap would be a modelling choice other datasets declined. C if a stable
     ranking matters more to you than the uncapped sum. **Decision:** A, B, C or D?

   **Notes for the AI:** On A: add the tuned results to the notes' "Signal under the declared metric" bullet (the table
   above, with the GLM baseline) and a CC line; no data change. On B: restore the definition of
   `apply_2026-11-08/after_issue7/` in the run folder (target log1p, RMSLE) while keeping the issue 7 blank, keep the
   issue 8 CC line and add one for the reversal; re-run `dataset check`, the task probe and `span_worth.py --metric
   rmsle`. On C: in `_clean` cap the dollars at $10M before they become the target (rename the target, e.g.
   `property_damage_usd_capped_10m`), say in the target bullet and the metric reason what the cap leaves out (it binds
   on 1,761 entries and removes 87% of the dollars) and why $10M; recompute the floor's cheapest cell under the cap;
   re-run `dataset check`, the task probe, `tune_tweedie.py --cap 10000000` and `span_worth.py`. On D: retire the record
   as `No (Retired)` with the reason, and remove the folder as working_copy.md says. Scripts and outputs:
   `tune_tweedie.py`, `bootstrap_tweedie.py`, `baselines_glm.py`, `tuned/`, `tuned_bootstrap.txt` in the run folder of
   2026-11-08. The rules: TP-1 (Must) and TP-2 (Should) for the signal, MET-1 (Must) for the planner's sum; MET-13's ban
   on a per-row cap is about the loss, not the target.

   [^10a]: **TP-1** (Must): a flag is a question, not a verdict; the probes fit untuned models, so check every flag
     against tuned methods before acting on it. **TP-2** (Should): a small but real signal is no reason to retire;
     retire, fix or keep a task for a concrete reason found in the task itself. Case: forest_fires (R^2 0.013,
     TabPFN-3.5 beats the mean on 26 of 32 folds), kept.
   [^10b]: fremtpl2 (the notes on its 19-row rating profile): "A cap is a modelling choice of the literature, not a
     shown error"; frempl_french_motor_personal_line keeps its largest claim, 802,620, and measures a score with each
     loss capped at 50,000 only to show how it decides a fold. **MET-13** (Must): a deviance gets no per-row cap, as
     that makes the metric improper; a cap on the target changes the task, not the metric.
   [^10c]: **TP-1** (Must), "How to check a flag": against the benchmark's tuned methods. **MET-1** (Must): the metric
     scores the decision of the use case; issue 8 made it the planner's sum of expected dollars.

   **Resolved (2026-11-08, Lennart):** A. The mean Tweedie deviance on the dollars stays as shipped; the notes' signal
   bullet gives the tuned results by window (3,463, 2,044 and 962 against 2,660, 2,301 and 1,740 for the mean per
   event type, with the bootstrap standard errors) and the capped variant as a note, and a CC line records the call.

11. **Is the Flash Flood duration outcome-free?**

   * **Problem:**
     - The re-review read Flood and Flash Flood as timed by a threat to life or property and kept their durations as
       outcome-free, with no note of their worth[^11a].
     - One of the four example onsets of a Flash Flood is the moment water "comes in contact, flowing into, or causes
       damage to an above ground residence or public building", so the damage can set some starts.
     - Under the deviance on the dollars (issue 8) the Flash Flood duration carries much of a model's skill, so this
       reading now moves the score.
   * **Background:**
     - NWSI 10-1605 Sec. 14 ends a Flash Flood when the waters "receded to a point where there was no longer an
       immediate threat to life or property"; a Flood runs from when waters "began to threaten life or property" to when
       there was "no longer any threat" (Sec. 15), and its definition, "inundation by water which causes damage", is the
       entry criterion, not the clock.
     - Storm Data records no onset type; `flood_cause` gives the cause (heavy rain for 95% of the Flash Flood entries),
       not the onset.
     - In the event narratives (read by the definition only to find double entries, then dropped), 6.8% of the 74,987
       Flash Flood entries with a damage figure name water at or in a building or damage to one, 36% a road closed or
       water over a road, 10% a rescue or evacuation; the ones naming a building average $6.5M against $0.8M. For Flood,
       4.5% name a building.
   * **Effect on the task:** blanking the Flash Flood durations would remove much of what a model fitted for the
     deviance learns; keeping them keeps spans whose start the damage may set for an unknown share of entries, at most
     the 6.8% that name a building.
   * **Experiments:** the shipped splits, LightGBM of 100 trees fitted with the Tweedie loss, 5 set-ups per window; the
     rise of the deviance when a type's durations are blanked (positive: the span helped; set-ups with a rise in
     brackets):

     | Blanked | On its own rows, 2023 / 2024 / 2025 | On all rows, 2023 / 2024 / 2025 |
     |---|---|---|
     | Flash Flood (74,914 rows) | +102% / +93% / +31% (15 of 15) | +9% / +27% / +16% |
     | Flood (48,454 rows) | +43% / +0% / +9% (13 of 15) | +5% / +7% / +5% |

     - Under RMSLE, the metric before issue 8, the two together had no consistent sign (-0.09 to +0.09).
     - Among positive Flash Flood entries the duration tracks the dollars at Spearman 0.44 where the narrative names a
       building and 0.31 where it does not.
   * **Consistency:** Thunderstorm Wind, timed by the first damage or the first wind of the criterion, keeps its span
     with a note where the wind can have set it and is blank where only the damage can (issue 7); Strong Wind, timed by
     the damage alone, is blank[^11b].
   * **Panel:** none; raised when issue 8 was applied.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Outcome-free, as read (implemented) | Flood and Flash Flood keep their durations, no note of their worth | no change | the building onset can be the damage; a large worth kept without the note other such spans carry |
     | B | Flash Flood kept with a note | no data change; Flash Flood moves to the kept-with-note bullet with its worth; Flood stays outcome-free (its clock is the threat) | follows the reading for a span drawn by the outcome or a criterion without it; keeps the skill | the damage-timed share is unknown, at most the 6.8% naming a building, and no feature locates it |
     | C | Blank the Flash Flood durations | blank for its 74,914 rows, as for Strong Wind; Flood keeps its own | no Flash Flood span the damage may set stays | loses most of the skill on Flash Flood rows (+31% to +102% of the deviance there), mostly spans a road or a stream sets |

   * **Recommendation:** B: the onset list lets the damage set some starts, so the span is drawn by the outcome or by a
     criterion without it and stays with a note giving its worth, as the measured Thunderstorm Wind spans do; no feature
     locates the damage-timed starts, so there is nothing to blank row by row, and the narratives put them at no more
     than 6.8%. **Decision:** A, B or C?

   **Notes for the AI:** On B: in the notes move Flash Flood from the outcome-free sentence into the kept-with-note
   bullet, with the onset quote (Sec. 14), the narrative shares and the worth above (`worth_floods_tables.txt`); Flood
   stays read as outcome-free with its worth stated; a CC line; the main session updates the spans Cases row. On C: add
   "Flash Flood" to `OUTCOME_SPAN` in `dataset.py`, update `changes` (word limit) and the notes, re-run `dataset check`,
   the leak probes and `span_worth.py --metric tweedie:1.5:1`. On A: state the worth in the outcome-free sentence. If
   you want the damage-timed share pinned down first: join the narratives to the shipped rows on begin time, county or
   zone, type and dollars (`flood_onset.py` has the patterns) and measure the duration's worth on the building-named
   rows alone. The rules: LEAK-10 (Must) and the LEAK-10 / LEAK-37 Cases row on spans; LEAK-10's second clause for
   values that cannot be located.

   [^11a]: **LEAK-10, LEAK-37** Cases row "A span or extent whose start or end the source defines by the outcome"
     (Lennart, 2026-11-06): where the outcome alone draws it, blank or drop it for those types; where it is drawn by the
     outcome or an outcome-free criterion, keep it with a `Potential leak, kept on purpose:` note giving its worth.
   [^11b]: **LEAK-10** (Must), second clause (amended 2026-10-26, Lennart): late cells that can be located row by row
     are blanked; values that cannot be located stay with a note only when the part that can be traced shows no gain.
     Issue 7 (Lennart, 2026-11-08) and D13 (issue 6, 2026-11-06).

   **Lennart (2026-11-08, change):** Option B: Flash Flood kept with a note.

   **Resolved (2026-11-08, Lennart):** B. The Flash Flood duration moves from the outcome-free reading to a `Potential
   leak, kept on purpose:` note with the Sec. 14 onset, the narrative shares (6.8% name a building) and its worth on the
   declared metric (+31% to +102% of the deviance on its rows when blanked); Flood, Hurricane (Typhoon) and Tropical
   Storm stay read as outcome-free, and no data changes (`dataset check`: 0 errors, 0 warnings).

12. **Score the damage summed per county or zone, hazard and year, the planner's unit, instead of each entry?**

   * **Problem:**
     - The planner sums expected dollars per county and hazard (dataset.py:77-82, :193-195), while the score is the
       mean Tweedie deviance of each entry, one reason the fit is approximate (REVIEW.md:12-13)[^12a].
     - In the test years 2023-2025 the entries fall into 37,077 cells of one county or zone, one event type and one
       year, with 3.62 entries per cell on average and 56.9% of the cells holding more than one (counted on the raw
       files with the definition's filters).
     - Issue 8 settled what is scored, the dollars by the Tweedie deviance, so the open question is only the unit:
       each entry, or each cell's sum[^12b]?
   * **Background:**
     - The Tweedie deviance is minimised by the mean, and means add, so a model that predicts each entry's expected
       dollars also predicts each cell's expected sum; the two scores aim at the same predictions and differ in how
       they weigh the errors (an AI reading of the loss).
     - Per entry, a cell counts once for every entry it holds, and 88.1% of the test entries share their cell with
       another entry; per cell, each county or zone, hazard and year counts once, and the errors on two entries of one
       cell offset each other as they do in the planner's total (counted on the raw files).
     - The cells look like the entries: 67.0% sum to $0 against 68.5% of the entries, and the largest 0.1% hold 71%
       of the dollars against 83% for the entries (counted on the raw files), so the deviance at power 1.5 suits the
       sums as it suits the entries.
     - The scorer cannot sum a group's truth and predictions today: its per-group choices keep one label per group
       (last, mean, any, lowest or highest); the cross-dataset item "Add a `sum` aggregation and a per-group mean RMSE
       to the scorer?" adds the sum if this issue chooses it.
     - The source models single events: Diaz and Joseph (2019) predict and score each tornado's damage
       (dataset.py:190-193).
   * **Effect on the task:** per entry, a county hit by many reports of one hazard in a year (hail and thunderstorm
     wind come as many entries) weighs more than a county with one large event, and a model gains by splitting a
     storm's damage right among the entries of one county, which the planner never looks at; per cell, only the total
     of each county, hazard and year counts.
   * **Experiments:** none on models in this round; the counts above are on the raw files of 2023-2025 with the
     definition's filters (134,183 entries).
   * **Consistency:**
     - pricing_game_2017_french_mtpl scores the deviance per policy although the insurer sums its book; there each
       policy gets its own price, a decision per row[^12c].
     - The rule of 2026-11-08 that gives a unit one vote covers rows that repeat one decision, not entries whose
       dollars add, so it does not decide this; the sum is its analogue for an amount (an AI reading)[^12d].
     - FEMA's National Risk Index, which uses SHELDUS, built from these entries (issue 5), gives the expected annual
       loss of 18 natural hazards at the county or census-tract level: the planner's unit in practice is a place and
       a hazard over a year (an AI reading of its documentation)[^12e].
   * **Unknown:** whether models rank differently on the cell sums, and whether 2023, where no tuned model beats the
     mean per event type (issue 10), stays as unstable; issue 10's tuned Tweedie LightGBM scored both ways on the
     three windows would settle it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Tweedie per entry | the mean Tweedie deviance at power 1.5 of each entry's dollars, floor $1, as since issue 8 | scores each event's expected dollars, which add up to the planner's sum; the source's unit; no code change | a cell counts once per entry; errors that offset in the planner's total are still penalised |
     | B | RMSLE per entry | the target back on log1p and scored by RMSLE, as before issue 8 (the panel's and the mediator's recommendation there) | a clear signal in every window (issue 10: 2.7 to 3.0 against 3.6 to 3.9 for the mean per event type) | scores the order of magnitude, whose sum understates the dollars; reverses issue 8; still per entry |
     | C | Tweedie on the cell sums | the scorer sums the dollars and the predictions of each county or zone, event type and year, then takes the mean Tweedie deviance at power 1.5 over the cells (about 12,000 per test year) | the planner's unit; each cell counts once | needs a `sum` aggregation in the scorer; how models rank on it is not measured; the source scores per event |

   * **Recommendation:** C, once the scorer can sum, with the run of the Unknown bullet as part of applying it: the
     planner acts on the total of a county and a hazard, and since the per-entry score already aims at the same
     predictions, the change only makes each county, hazard and year count once and lets errors offset as in the
     planner's total; A stays until the code exists, and B would reopen issue 8. **Decision:** A, B or C?

   **Notes for the AI:** On C: (1) the cross-dataset item adds `sum` (the truth and the predictions summed per group)
   to `_aggregate` in `src/data_foundry/v2/metrics.py`; check how a per-group prediction unit is declared for a
   temporal task without turning the split into a grouped one (`Grouping` drives the grouped splits today); (2) in
   `_clean` add a scoring column `cell`, `county_zone`, `event_type` and the begin year joined as text, role `group`,
   never a feature (`county_zone` and `event_type` stay features); (3) the $1 floor (`min_prediction`) then applies to
   each cell's summed prediction; (4) rewrite the metric reason (the unit and the cell counts), `fit_reason` (its first
   gap) and the notes' signal bullet; (5) re-run `dataset check`, the task probe and `tune_tweedie.py` of the run folder
   of 2026-11-08 scored per entry and per cell, on the cluster; CHANGELOG entry and a CC line. On B: as issue 10's
   notes for its option B. The rules: MET-1 (Must), MET-11 (context), MET-13 (the floor), MET-17 (Should, not binding
   here).

   **Andrej (2026-11-09, discuss):** What are the units planners make decisions for individually? entries or cells? Or
   is it a global aggregation? We want the final aggregation to one score be over the individual decision units.

   **Answer (AI, 2026-11-09):** Planners decide per county and hazard, not per entry and not on a national total; score
   over those cells by summing (needs code) or by giving each cell one vote (no code)?

   * **Problem:**
     - A mitigation planner decides per jurisdiction and hazard on the loss expected in a year (44 CFR 201.6, FEMA's
       planning guide, the National Risk Index), so the decision unit is a county or tract and a hazard, and its
       realisation in one test year is a county or zone, hazard and year cell[^12f].
     - One score over those units is the mean over cells of the deviance of each cell's summed dollars (the issue's
       C), which the scorer cannot compute without the `sum` aggregation you marked to leave today, while weighting each
       entry by 1 over its cell's entries gives a mean over the same cells with no code.
     - The definition's inputs describe an event already reported, which a planner who plans before the year does not
       have, so the use case and the features disagree whichever unit is scored.
   * **Background:** who decides on what, in the primary sources:
     - Local plans, 44 CFR 201.6(c)(2) (https://www.law.cornell.edu/cfr/text/44/201.6): the risk assessment gives "the
       type, location, and extent of all natural hazards that can affect the jurisdiction", "information on previous
       occurrences of hazard events and on the probability of future hazard events", "an overall summary of each hazard
       and its impact on the community" and "An estimate of the potential dollar losses to vulnerable structures"; a
       plan of several jurisdictions must "assess each jurisdiction's risks where they vary", and a plan is resubmitted
       "within 5 years" (201.6(d)(3)). State plans (44 CFR 201.4(c)(2), https://www.law.cornell.edu/cfr/text/44/201.4)
       build on "estimates provided in local risk assessments" and describe vulnerability "in terms of the jurisdictions
       most threatened by the identified hazards".
     - FEMA's Local Mitigation Planning Policy Guide (released April 2022, in force since 19 April 2023, pp. 22-24,
       https://www.fema.gov/sites/default/files/documents/fema_local-mitigation-planning-policy-guide_042022.pdf, read
       in the copy at https://www.caloes.ca.gov/wp-content/uploads/Hazard-Mitigation/Documents/FEMA-Local-Mitigation-Planning-Policy-Guide-04.2022.pdf):
       "B1-d. The plan must include information on previous hazard events for each hazard"; probability "may be defined
       in historical frequencies"; "B2-b. The plan must describe the potential impacts on each participating
       jurisdiction", for example "by referencing historical disaster damages with an estimate of potential future
       losses".
     - National Risk Index, Technical Documentation (December 2025, v1.20,
       https://www.fema.gov/sites/default/files/documents/fema_national-risk-index_technical-documentation.pdf), Sec.
       4.4: "The Expected Annual Loss for each Census tract or county is the average economic loss in dollars resulting
       from natural hazards each year. Expected Annual Loss is computed for each hazard type"; it multiplies the
       exposure, "the probability of that hazard type's occurrence each year (Annualized Frequency)" and the share lost
       per occurrence (Historic Loss Ratio, from SHELDUS, with this database for tornado and inland flood, Sec. 5.4.1).
       Its users are "planners and emergency managers", to "Enhance hazard mitigation plans" and "Prioritize and
       allocate resources" (Sec. 1). Its hazards group this database's types, and "Multiple event records that occur
       on the same day in the same county are counted as a single Inland Flooding event" (Sec. 15.3.1).
     - After a storm the unit is the disaster and the county: FEMA weighs a declaration request's damage per capita
       statewide and "at the county and local government level" (44 CFR 206.48(a),
       https://www.law.cornell.edu/cfr/text/44/206.48). This actor's moment matches the inputs (first reports, before
       the damage is assessed); its unit is one storm in one county or zone (`EPISODE_ID`), all its types summed.
     - Diaz and Joseph (2019, abstract) fit a model per tornado, then "provide static and interactive gridded maps of
       monthly predicted probabilities of damage and property damages for the year 2019": the event is the model's
       unit, a place and a period the planner's.
     - Insurers and reinsurers decide per policy and per portfolio on insured values, which this database does not
       hold, so they are not this task's actor (an AI reading, no source read).
     - A global total is nobody's decision unit (the National Risk Index ranks counties and tracts, a state plan names
       the jurisdictions most threatened), and as a score it is one number per window: the tuned LightGBM below sums to
       24%, 48% and 77% of the test dollars of 2023, 2024 and 2025, the mean per event type to 106%, 185% and 356%.
   * **Use case and features:**
     - The prediction point is after the event, "logged from the first reports ... before any damage survey"
       (dataset.py:151); a planner plans before the year from past occurrences and their frequency, when no begin time,
       duration, measured wind or hail size of that year's events exists, so `use_case` pairs the planner's unit
       with a responder's moment ("to plan where disaster resources and mitigation go").
     - Re-unitising the rows to cells with only what is known before the year gives the planner's task, and a
       different one: a yearly loss forecast per county and hazard from place and history, which the forecasting rules
       put in scope only after the naive-profile test[^12g]; and 72-74% of the county and hazard pairs of the earlier
       years have no entry in a test year, so a cell table built from the entries keeps only the cells where something
       was logged.
     - With the event inputs, the moment the data supports is a planner totalling the estimates of events already
       reported per county and hazard (or a responder after a storm, per storm and county): the task is the loss per
       event that the planner's county total is built from, as the National Risk Index's loss per occurrence is.
   * **Experiments:** the shipped splits; 8 models fitted on each window's training side as in issues 8 and 10 (the
     training mean, the mean per event type, a Tweedie GLM on event type and month, LightGBM with the Tweedie loss at
     100 and 400 trees and tuned per window over 24 configurations with early stopping on the last 12 months, each of
     the three with 3 seeds, and squared-error LightGBMs on the dollars and on log1p); each scored by the declared
     deviance per entry, on the sums per unit (the $1 floor on each unit's sum) and per entry with each cell one vote;
     the top model with the share of 1,000 bootstrap resamples that keep it on top (test days for entries, cells for
     cells), Kendall's tau of the 8-model order against the per-entry order, and the tuned model minus the mean per
     event type with its bootstrap standard error:

     | Window | Per entry: top | Cell sums: top | Each cell one vote: top | Tau against per entry: sums / one vote | Tuned minus per-type mean: per entry | The same: cell sums |
     |---|---|---|---|---|---|---|
     | 2023 | GLM (57%) | GLM (65%) | GLM (60%) | 0.86 / 0.86 | +1,143 (SE 1,871) | +6,308 (SE 7,280) |
     | 2024 | tuned LightGBM (63%) | GLM (81%) | GLM (68%) | 0.79 / 0.79 | -266 (SE 320) | +74 (SE 371) |
     | 2025 | LightGBM, 100 trees (83%) | LightGBM, 100 trees (74%) | LightGBM, 100 trees (70%) | 1.00 / 1.00 | -882 (SE 49) | -1,551 (SE 117) |

     - The unit moves one call: in 2024 the tuned LightGBM leads the per-type mean per entry (ahead in 79% of the
       resamples) and is level with it on the cell sums (49%); in 2023 every score puts the GLM and the per-type mean
       first, in 2025 the 100-tree LightGBM.
     - Without the two squared-error fits, last under every score, tau per entry against the cell sums is 0.73, 0.60
       and 1.00 over 6 models.
     - Each cell one vote orders the models as the cell sums do (tau 1.00, 0.86 and 1.00) and has their top model in
       all three windows; one storm in one county or zone (the responder's unit) and one county or zone over all
       hazards have the same top models (GLM, GLM, 100-tree LightGBM).
     - The test years hold 11,765, 12,676 and 12,636 cells (3.5 to 3.7 entries each), 40% to 44% of them forecast
       zones rather than counties.
     - Per entry the run reproduces issue 10 within its seed range (tuned 3,803, 2,035 and 858; the GLM 2,553, 2,130
       and 1,598, the same as issue 10's); its run folder of 2026-11-08 is not on this machine, so the set-up was
       rebuilt from issue 10's description.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Per entry | the mean deviance over entries, as now | no code; the unit the inputs describe and the source records | a busy cell counts once per entry; in 2024 another top model than every per-cell score |
     | b | Cell sums | the dollars and the predictions summed per county or zone, event type and year, the mean deviance over cells (the issue's C) | the planner's total for one year; errors offset within a cell as in that total; each entry's mean stays the best prediction | needs `sum` in the scorer and a per-group unit on a temporal task, so the cross-dataset item reopens; zone cells are not jurisdictions |
     | c | Each cell one vote (implemented) | a weight scoring column, 1 over the entries of the entry's cell, read by the metric's weight input and declared as the task's unit weight | no code; the final mean runs over cells; the cell sums' top model in 3 of 3 windows | errors within a cell do not offset; the weight can move the best prediction (not measured); the one-vote rule was written for repeated rows, not amounts that add |
     | d | Rows re-unitised to cells | one row per county or zone, hazard and year, the summed dollars as target, inputs known before the year | the planner's unit and moment | another task, a yearly loss forecast from place and history; cells without an entry are missing; the event inputs go |

   * **Recommendation:** c now[^12h]: the final mean runs over the cells the planner decides on, it needs no code, and
     here it picks the same top model as the cell sums in all three windows; b if you want the planner's summed total
     itself, which reopens the `sum` item. Either way `use_case` should say what the inputs allow, a planner totalling
     the estimates of events already reported per county or zone and hazard, since before the year none of them
     exists; `fit` stays approximate[^12a]. **Decision:** a, b, c or d?

   **Andrej (2026-11-09, discuss):** Reply (c): Each cell one vote

   **Resolved (2026-11-09, Andrej):** c: each county or zone, event type and year counts once. Each entry weighs 1
   over its cell's entries (`cell_weight`, a weight scoring column the deviance reads), and the task declares it as its
   `unit_weight` with `cell` as the unit; neither is a feature or a training weight, and `known_at_scoring` says the
   count is known only once the year is over. `use_case` now reads as a planner who totals the damage of the events
   already reported per county or zone and hazard; the metric reason, `fit_reason` (still approximate) and the notes
   give the unit and its counts; a CC line in the notes and the record, and a Cases row for the extension of the
   one-vote rule to entries whose dollars add[^12i]. On the new score with issue 14's $10 floor, the task probe still
   flags no signal (its squared-error families lose to the training mean, 7,555 for the random forest against 5,615),
   the leak probe finds nothing new, and training tuned LightGBM with the weight scored worse in all three windows than
   without it. `dataset check`: 0 errors, 0 warnings.

   [^12a]: **MET-1** (Must, in main): "The declared metric scores the real task: the decision of the use case (USE-1),
     at the unit the actor acts on, the way a practitioner would have chosen a model for it in practice." **USE-8**
     (Must): the fit says how closely the data mirrors the use case; the Validity block names the per-county sum as a
     gap.
   [^12b]: Issue 8 (Lennart, 2026-11-08, B): "i think this is a similiar discussion that we should start from the
     right metric and maybe ignore prior claims if they dont match the task", against the panel's and the mediator's
     lean to RMSLE.
   [^12c]: pricing_game_2017_french_mtpl: the mean Tweedie deviance at power 1.5 per policy, "Chosen over the Gini by
     the curator (Andrej, 2026-11-03)".
   [^12d]: **MET-17** (Should; 2026-11-08, Lennart, in main): a unit counts once "if the actor decides once per unit
     and the unit's further rows are repeats the source's protocol made"; "The score stays per row when each row is a
     decision of its own".
   [^12e]: FEMA, National Risk Index (https://www.fema.gov/flood-maps/products-tools/national-risk-index, read on
     2026-11-09): a baseline measure of expected annual loss for 18 natural hazards at the census-tract or county
     level.
   [^12f]: **MET-1** (Must, in main): the metric scores the decision "at the unit the actor acts on". **USE-1** (Must):
     "A use case is an actor, a moment and a decision". **USE-3** (Must): "Name the prediction point: when the model is
     used and what is known then."
   [^12g]: **SEL-10** (Must): "Time-series forecasting, future values of a series (demand, sales or a price over a
     horizon), is out". **SEL-11** (Must): "A panel that looks like forecasting is in scope when it passes TP-10 ...: a
     model on the features clearly beats each entity's naive profile, and the source's top solutions used no lagged
     target."
   [^12h]: **MET-17** (Should; 2026-11-08, Lennart, in main): the weight is "a weight scoring column the metric reads,
     for scoring only (MET-15)", and "the task declares it as its `unit_weight`"; the rule covers units whose further
     rows "are repeats the source's protocol made", so giving one vote to cells whose entries add their dollars is an
     extension (an AI reading) that needs a Cases row.
   [^12i]: **MET-17** (Should; 2026-11-08, Lennart, in main): one vote per unit "if the actor decides once per unit
     and the unit's further rows are repeats the source's protocol made"; here the entries of a cell add their dollars,
     an extension the Cases row records (Andrej, 2026-11-09).

13. **Keep the reporter (`SOURCE`), with the damage survey's value replaced by the first report's source, instead of dropping the column?**

   * **Problem:**
     - `SOURCE` is dropped for every entry because one of its 44 values, "NWS Storm Survey", marks a damage survey
       the office makes after the event (dataset.py:163, :279)[^13a].
     - The drop also removes the reporter of the other 820,426 entries (a trained spotter, the public, an emergency
       manager, law enforcement, a 911 call centre, a utility), which the office has from the first report and the
       planner could use (counted on the raw files, before the 918 double entries go).
     - Blanking the survey value alone keeps the marker, as the column has no other blank (dataset.py:163), so keeping
       the reporter needs another value for the 23,636 surveyed entries.
   * **Background:**
     - The surveyed entries are 2.8% of the rows: 16,043 tornado entries (68% of all tornado entries), 6,183
       thunderstorm wind entries (2.4% of theirs) and a few hundred of other types (counted on the raw files).
     - The NWS issues a Local Storm Report (LSR) for each report it receives while the storm happens, with its source;
       the Iowa Environmental Mesonet keeps them (its request page offers 2003 to 2026, with a field "Who reported the
       LSR"), and the review matched its 2024 reports to these entries for issue 7.
     - A rough match of the 1,967 surveyed county entries of 2024 with a begin point to the LSRs of the same office
       finds a report from another source for 1,590 (81%) within 30 minutes and 15 km, and for 1,799 (91%) from 1
       hour before to 2 hours after and within 25 km; the others had only the survey's own LSR or none, events nobody
       reported before the survey (counted on the raw files and the review's 2024 LSRs; a nearby report can belong to
       another event of the same storm).
     - The definition's measurement, untuned LightGBM trained to September 2023 and tested on 2024, gives RMSLE 2.626
       without the column and 2.559 with it as published or with the survey value merged into "Unknown"
       (dataset.py:151, :163); that gain includes the survey marker and was measured under RMSLE, not under the
       deviance declared since issue 8.
   * **Effect on the task:** without the reporter a model cannot tell an entry an emergency manager or law enforcement
     sent, often a damage report, from one an automated station measured (an AI reading of who reports what); with the
     survey value kept or blanked it learns which events the office surveyed, a step taken after damage was seen.
   * **Consistency:**
     - The drop follows kick and expresso_churn_prediction (dataset.py:163), where a whole field's fill or
       missingness differed by the outcome; here one value is late and the others are first-report facts, so the rule
       that the smallest fix keeping a valid signal beats a drop points to a fix (an AI reading of which precedent
       applies)[^13b].
     - The duration blanks of issues 6 and 7 go by event type and speed type, never by reporter, so they do not mark
       the survey (dataset.py:165).
   * **Unknown:**
     - The reporter's worth under the declared deviance on the entries that were not surveyed: a fit with and without
       `SOURCE`, scored on those test entries only, on the cluster.
     - How well the LSR match holds for 2007-2023, and whether Storm Data's `SOURCE` is the first report's source or
       the one the preparer picked among several (the NWS directive was not re-read for this).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Drop the column (implemented) | `SOURCE` leaves for every entry | no survey marker; no outside data | the first reporter of 97% of the entries is lost |
     | B | Keep it, survey value blanked | `SOURCE` ships with "NWS Storm Survey" set to missing | one line of code | the blank is the survey marker, as no other entry is blank; merged into "Unknown" the column scored as published (2.559) |
     | C | Keep it, surveyed entries re-sourced from the LSRs | "NWS Storm Survey" becomes the source of the nearest LSR of another source from the same office, near in time and place; an entry with no such report keeps a blank | the first reporter on nearly every entry; the survey value gone | an outside archive and an approximate match for 23,636 entries over 2007-2025; the blank still marks the entries nobody reported before the survey (9% to 19% of the surveyed ones in 2024) |

   * **Recommendation:** C: the reporter is a first-report fact the planner has, the smallest fix that keeps it beats a
     drop, and in 2024 a report from another source exists for 81% to 91% of the surveyed entries; check the match on
     a few early years and the reporter's worth on the entries not surveyed first, and keep A if the match fails for
     the early years[^13c]. **Decision:** A, B or C?

   **Notes for the AI:** On C: download the IEM LSR archive for 2007-2025 (the CSV export of
   https://mesonet.agron.iastate.edu/request/gis/lsrs.phtml; `s05_lsr_match.py` in the claim auditor's scratch of the
   run folder of 2026-10-30 is the match recipe, with the 2024 months); match each "NWS Storm Survey" entry to the LSRs
   of the same `WFO` whose source is not "NWS Storm Survey", within a window around the begin time and a radius around
   the begin point (zone entries, which have no begin point, by the zone's UGC code and the time); take the earliest
   such report's source, mapped to Storm Data's spellings (`Emergency Mngr` to "Emergency Manager", `CO-OP Observer` to
   "COOP Observer"); the rest get a blank, or, if you prefer, leave as events not known at the prediction point (say
   which in the CC). Add the LSR download to `download_description`, take `SOURCE` out of `post_outcome` and ship it
   as `reporter`, rewrite the notes' bullet (dataset.py:163) and `changes`; re-run `dataset check`, the leak probes
   (the blank's damage rate) and the task probe on the cluster; CHANGELOG and a CC line. On B: the blank is a kept
   leak, which LEAK-10 (Must) does not allow without an exception. The rules: LEAK-10, LEAK-7, LEAK-37, LEAK-38.

   **Andrej (2026-11-09, as implemented):** A, as implemented.

   **Resolved (2026-11-09, Andrej):** A: `SOURCE` stays dropped for every entry. The column as published carries the
   post-event "NWS Storm Survey" marker on the surveyed entries (23,621 on the task's rows), so neither the column as
   published nor a blank in place of that value can ship, and the fix that would keep the reporter needs an outside
   archive (the Iowa Environmental Mesonet's Local Storm Reports) and an approximate match in time and place, which in
   2024 finds another source for 81% to 91% of the surveyed county entries and leaves the rest marked by a blank. No
   data change; a CC line in the notes and the record records the call (`dataset check`: 0 errors, 0 warnings).

   [^13a]: **LEAK-10** (Must, in main): out are "a column recorded after the outcome" and "missingness that encodes
     the outcome"; "Fix it in the definition the smallest way (LEAK-7), else drop it". **LEAK-7** (Should, in main):
     "The smallest fix that keeps a valid signal beats dropping the column"; its cases include "re-source settled
     labels (consumer_complaints)". **LEAK-37** (Must): "An input the actor knows at the prediction point is not a
     leak".
   [^13b]: kick and expresso_churn_prediction (Lennart, 2026-10-22; **LEAK-10** with **LEAK-38**): a named field
     "whose missingness or fill, given the covariates known at the prediction point, differs by outcome" is dropped.
     That this covers a whole field and not one late value among first-report values is an AI reading.
   [^13c]: The curator's standard for the information audit of 2026-11-09: every piece of information the actor has at
     a point is available to the benchmark there, and nothing more.

14. **Raise the metric's floor from $1 to $10, the smallest damage the source ever records?**

   * **Problem:**
     - The $1 floor follows the collection's convention, two orders below the cheapest event type's training mean ($909, Dense Smoke), rounded down[^14a].
     - No entry records a damage between $0 and $10: of the 843,144 entries 268,670 have damage, the smallest is $10, 0.17% are below $100 and 6.1% below $1,000 (counted on the definition's frame, 2026-11-09).
     - In the task probe 44% of the linear model's and LightGBM's predictions (squared error on the dollars) sit at the floor, so the floor, not the planner's sum, sets how far they rank behind: keep $1, or clip at the label's resolution?
   * **Background:**
     - A prediction below the floor is scored as the floor; at power 1.5 the cost of a low prediction on an entry with damage y grows like 4y/sqrt(mu), so raising the floor tenfold divides that cost by about 3.2, while an entry without damage costs almost nothing either way.
     - The floor's first reason was practice, a clip "to a reasonable number" (Lennart, 2026-11-04)[^14a].
     - Offices enter round values ($1,000, $5,000, $10,000); 44% of the positive figures have one significant digit (issue 8).
     - For the tuned Tweedie LightGBM at 400 trees, 5.6% to 8.1% of the predictions fall below $1 and its score moves by 1% to 10% between floors of $0.1 and $10 (the notes' "Metric floor" bullet).
   * **Effect on the task:** a planner reads an expected $1 and an expected $10 for one entry as the same nothing; above $10, the floor leaves every score unchanged that a planner could act on.
   * **Consistency:** the rule is the cross-dataset item "Set a deviance's floor where the actor would clip"; pricing_game_2017_french_mtpl asks the same for its 0.1 EUR (its issue 7). Under issue 12's option C the floor applies to each cell's summed prediction, where $10 is still below every cell's plausible sum.
   * **Unknown:** how the benchmark's tuned methods rank at $1, $10 and $100 on the three windows; a cluster run would show it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | $1 | as since issue 8 | follows the collection's rule as it stands | scores predictions ten times finer than anything recorded; 44% of the squared-error fits' predictions decided by it |
     | B | $10 (implemented) | the smallest damage the source records | the label's own resolution; a fact, not a formula | needs the rule changed (the cross-dataset item, B) |
     | C | $100 | one order below the cheapest type's mean; 0.17% of the positive entries lie below it | further from the near-zero outputs | above 457 recorded damages; a round number without a fact of its own |

   * **Recommendation:** B, with the rule changed by the cross-dataset item: $10 is the smallest amount anyone entered, so a finer prediction is not a planning difference. **Decision:** A, B or C?

   **Notes for the AI:** On B: `params={"power": 1.5, "min_prediction": 10.0}` in `dataset.py`; rewrite the notes' "Metric floor" bullet (the fact: the smallest recorded damage, with the counts above), the metric reason and `predicted`; re-run the task probe (share at the floor) and `dataset check`; re-run `tune_tweedie.py` of the run folder of 2026-11-08 on the cluster (`sbatch`, gpua100*) for the signal bullet; a CC line naming the $1 of 2026-11-08 as superseded; a MET-13 Cases row; CHANGELOG entry. The count script is `storm_small.py` (build the frame, quantiles of the positive target).

   **Andrej (2026-11-09, change):** Option B: $10.

   **Resolved (2026-11-09, Andrej):** B: `min_prediction` is $10, the smallest damage the source records (none of the
   268,670 entries with damage lies between $0 and $10). The metric reason, the notes' floor bullet and `predicted`
   say so; a CC line in the notes and the record, and a Cases row under the floor rule[^14b]. At $10 no prediction of
   LightGBM or CatBoost fitted with the Tweedie loss, of the GLM or of the means falls below the floor, and their
   scores are the same at $1 and $10; a squared-error LightGBM has 1.7% to 2.3% of its predictions below it and scores
   better at $10 (12,103 against 22,656 in 2023); in the task probe the linear model and LightGBM still have 43.8% at
   the floor.

   [^14a]: **MET-13** (Must, in main; amended 2026-11-06, Lennart): "The floor is a parameter the definition states, as practice clips a model's output before scoring (Lennart, 2026-11-04, on bemtpl97: "in pratice we would also clip to a reasonable number"): two orders below the smallest plausible mean". The definition's notes call the $1 "a convention of this collection that can change later, not a property of the source".
   [^14b]: **MET-13** (Must, amended 2026-11-06, Lennart): the floor sits "two orders below the smallest plausible
     mean"; the $10 is the label's resolution instead (Andrej, 2026-11-09), about two orders below the $909 of Dense
     Smoke too. The rule's text is the cross-dataset item "Set a deviance's floor where the actor would clip".

15. **Decide issue 10's cap again on this task's own facts, once issue 12 has set the unit?**

   * **Problem:**
     - Issue 10 kept the uncapped dollars partly because "caps were declined elsewhere", but those precedents are a claim count (fremtpl2) and one large claim in a motor book (frempl), not a catastrophe tail in which 0.1% of the 2024 test rows hold 74% of the dollars[^15a].
     - In 2023 no tuned model can be told from a mean per event type (+802, standard error 1,580), so the declared score orders methods mostly by the few largest events of each test year.
     - Once issue 12 sets the unit, decide cap or no cap by how stably the score orders methods on this task, or leave issue 10's call as it is?
   * **Background:**
     - For the cap: at $10M the tuned model beats the mean per event type in every window and seed (-18% to -32%), and the cap binds on 1,761 entries.
     - Against the cap: it removes 87% of the dollars, the catastrophes, and a planner's expected annual loss (FEMA's National Risk Index, issue 12) counts them; so the cap trades the planner's sum for a stable ranking.
     - Lennart's own standard in issue 8 points to this task's facts first: "start from the right metric and maybe ignore prior claims if they dont match the task".
     - Summing per county, hazard and year (issue 12, C) leaves the tail about as heavy (the largest 0.1% of the cells hold 71% of the dollars against 83% for the entries), so the unit alone may not settle the stability.
   * **Effect on the task:** none until decided; the question is whether the score ranks methods or years.
   * **Experiments:** issue 10's tuned runs (3 seeds per window, bootstrap over test rows and test days); no run yet on the cells or on a measure of rank stability.
   * **Unknown:** how stably the benchmark's tuned methods are ordered across the three windows and across bootstrap resamples of the test days, uncapped and capped, under the unit issue 12 picks.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Uncapped, as decided (implemented) | issue 10 stands | the planner's whole sum, catastrophes included | a few events per year order the methods; the call rests partly on precedents of other kinds |
     | B | Cap at $10M now | as issue 10's option C | a signal in every window and seed | drops the catastrophes the planner counts; tested at one value |
     | C | Measure, then decide | after issue 12: rank stability of 4 to 5 tuned methods (Kendall's W across windows, share of bootstrap resamples that keep the top method) uncapped and at $10M, then A or B with the numbers | the call rests on this task's facts | a cluster run; the decision waits |

   * **Recommendation:** C: the uncapped sum is the planner's quantity, so A should stand unless the measured ranking is mostly noise; the precedents of other targets should not decide it either way. **Decision:** A, B or C?

   **Notes for the AI:** On C, after issue 12 is decided: extend `tune_tweedie.py` of the run folder of 2026-11-08 to 4 or 5 methods (Tweedie LightGBM, the GLM with event type and month, CatBoost with the Tweedie loss, a squared-error LightGBM, the per-type mean), score each window per entry or per cell as issue 12 says, uncapped and capped at $10M, with 2,000 bootstrap resamples of test days; report Kendall's W across windows and the share of resamples that keep the top method; run with `sbatch` on gpua100*; then put A or B again with the table.

   **Andrej (2026-11-09, change):** Option C: Measure, then decide.

   **Answer (AI, 2026-11-09):** Cap at $10M, since uncapped the score cannot order the methods in two of three test
   years; cap, or keep the whole sum?

   * Measured on the shipped score (each cell one vote, floor $10): the GLM on event type and month, the mean per event
     type, tuned Tweedie LightGBM, Tweedie CatBoost and squared-error LightGBM, 3 seeds, 2,000 bootstrap resamples of
     test days.
   * Uncapped, the top method differs in every year (GLM 2023, CatBoost 2024, tuned LightGBM 2025) and stays on top in
     57%, 59% and 78% of the resamples; Kendall's W of the ranks across the years is 0.62.
   * Uncapped, tuned LightGBM minus the per-type mean is +6,781 (SE 7,458), +13 (SE 753) and -1,040 (SE 120): only 2025
     separates a model from a lookup table.
   * Capped at $10M (fitted and scored on the capped dollars): W 0.91, the top kept in 81%, 92% and 95%, tuned LightGBM
     below the per-type mean in every year (-247, SE 70; -137, SE 90; -255, SE 30).
   * The cap binds on 1,761 entries (0.2%) and removes 87% of the dollars; $10M is the only value tested.

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Uncapped (implemented) | issue 10 stands | the planner's whole sum, catastrophes included | in 2023 and 2024 the order of methods is mostly noise, so the task adds little to a benchmark ranking |
     | b | Cap at $10M | target min(dollars, $10M); metric, unit and floor unchanged; the notes say what the cap leaves out | the same methods lead across years and resamples; models beat the per-type mean every year | leaves out the catastrophes, 87% of the dollars the planner sums; one cap value tested |

   **Recommendation:** b: the issue's own test for keeping the uncapped sum, a ranking that is not mostly noise, fails
   in two of three years, and the cap keeps every entry and its expected dollars up to $10M[^15b]. **Decision:** a or
   b?

   **Andrej (2026-11-10, discuss):** That methods separate well should never be the main objective, the main objective
   should always be representing the task correctly. It can always happen that methods perform equally well and noisy
   tasks are normal.

   **Answer (AI, 2026-11-10):** Keep the sum uncapped (a): the planner's task includes the catastrophes, so the cap
   would score a different quantity; I withdraw the recommendation of the cap, which rested on ranking stability.

   * The planner's quantity is the expected annual loss of a county and hazard; FEMA's National Risk Index, the
     reference for that planner (issue 12), builds it from the recorded losses with the large events in, not capped.
   * A $10M cap removes 87% of the dollars (1,761 entries, 0.2%), so a capped score would rank methods on the 13% of
     the loss a planner cares least about[^15c].
   * The stability numbers stay as facts in the notes: uncapped, Kendall's W across years 0.62 and the top method kept
     in 57%, 59% and 78% of the resamples; tuned LightGBM separates from the mean per event type only in 2025. That is
     a noisy task, not a wrong one.

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Uncapped (implemented) | issue 10 stands; the notes state the measured noise | the planner's whole sum | methods hard to tell apart in 2023 and 2024 |
     | b | Cap at $10M | target min(dollars, $10M) | stable ranking | scores 13% of the dollars, not the planner's sum |

   **Recommendation:** a. **Decision:** a or b?

   **Andrej (2026-11-10, discuss):** Reply (a): Uncapped

   **Resolved (2026-11-10, Andrej):** (a), the damage stays uncapped in training and scoring. The planner's expected
   annual loss includes the large events, and a $10M cap would score 13% of the dollars; the ranking's instability
   (Kendall's W 0.62 across the windows, tuned LightGBM apart from the mean per event type only in 2025) is a fact of a
   noisy task, stated in the notes' signal bullet. Applied: that bullet states the measured W 0.62 uncapped as a fact
   and no longer calls the cap open; a CC line in the notes and the record.

   [^15a]: Issue 10 (resolved 2026-11-08, Lennart, A), its Problem: "it scores another target than the dollars Lennart chose, and caps were declined elsewhere"; its footnote cites fremtpl2 ("A cap is a modelling choice of the literature, not a shown error") and frempl_french_motor_personal_line (its largest claim, 802,620, kept). **MET-13** (Must, in main): "a cap on the target changes the task, not the metric".
   [^15b]: **MET-13** (Must, in main): "a cap on the target changes the task, not the metric". **MET-1** (Must): the
     metric scores the decision of the use case, here the planner's sum of expected dollars.
   [^15c]: **MET-1** (Must, in main): "The declared metric scores the real task: the decision of the use case
     (USE-1), at the unit the actor acts on". **TP-2** (Should, in main): "A small but real signal is no reason to
     retire".

16. **Which years should the three test windows be?**

   * **Problem:**
     - The three test windows are the calendar years 2023, 2024 and 2025, while one-year windows that keep half the
       entries for training reach back to 2017, nine years in all[^ns-split14].
     - Since 2026-11-10 the newest window always stays and the others are chosen from the use case and statistics of
       the data, and walking back from the newest needs its own reason[^ns-split15].
     - The damage per entry moves widely between years as the costliest storms land in some years and not in others
       (mean $97,000 in 2025, $1.94M in 2017), and the three newest years are three of the four lowest.
   * **Background:**
     - Every candidate is a calendar year with the 3-month gap, so every one holds all storm seasons and whole year
       cells; the median entry is $0 and the 90th percentile $10,000 in every year ($20,000 in 2017), so the years
       differ in their largest entries.
     - B spreads the windows evenly over the nine eligible years (the 1st, 5th and 9th candidate); C takes every third
       year from the newest.
     - The offices' $0 practice drifts: an office's 2024 share of $0 predicts its 2025 share at r 0.958 and its
       2007-2016 share at r 0.575, and the share of events without a damage figure rises from 7.3% (2007) to 22-24%
       (2022-2025). An older test year meets an older practice, which its own training years mostly share.
     - PSI, the population stability index, compares a feature's distribution in the window with its train side;
       above 0.25 is usually read as a large shift. The largest PSI is 0.12 to 0.24 (office, state, event type) in
       every candidate, so the features do not set one year apart. The candidate table's unseen-category share reads
       100% in every year because the tool counts the scoring cell (county or zone, hazard and year), which carries the
       year; it is no feature.
   * **Statistics:** from the candidate table; the test means from every entry of the year, the train side's from a
     100,000-row sample, which a few large entries move (2025's side reads $573,000 and 2024's $357,000, though the
     two sides differ by one year of entries).

     | Year | In | Test entries | Mean damage per entry, test | Train side (sample) | Train share | Largest PSI |
     |---|---|---|---|---|---|---|
     | 2025 | A, B, C | 45,870 | $97,300 | $572,900 | 94.1% | 0.24 |
     | 2024 | A | 44,255 | $355,600 | $356,600 | 88.9% | 0.19 |
     | 2023 | A | 44,056 | $377,300 | $433,900 | 83.3% | 0.15 |
     | 2022 | C | 40,592 | $509,100 | $497,700 | 78.5% | 0.19 |
     | 2021 | B | 39,249 | $479,200 | $388,400 | 73.8% | 0.22 |
     | 2020 | none | 40,745 | $657,400 | $356,800 | 69.0% | 0.15 |
     | 2019 | C | 47,165 | $132,100 | $345,200 | 63.4% | 0.13 |
     | 2018 | none | 43,237 | $869,800 | $369,200 | 58.5% | 0.13 |
     | 2017 | B | 41,367 | $1,941,000 | $188,200 | 53.6% | 0.12 |

   * **Effect on the task:** A ranks models on three adjacent, low-damage years, so how a model handles a year of
     catastrophic storms is not tested. B adds 2021 and 2017, the costliest year in the data, which the planner's
     annual loss includes; its oldest refit trains on 53.6% of the entries (2007 to September 2016). C adds 2022 and
     2019, a middle and a quiet year, with every refit on 63.4% or more.
   * **Consistency:** issue 15 (2026-11-10, Andrej) kept the catastrophes uncapped because the planner's expected
     annual loss includes them; B tests a year they dominate. The signal measured for issues 10, 12 and 15 (tuned
     models, Kendall's W 0.62 across the windows) was taken on 2023-2025.
   * **Sources:** the definition `datasets/_dev/tabarena-v0pt2/noaa_storm_events_damage/dataset.py` (`temporal`,
     `splits_comment`, the History bullet and the anomaly bullet on the $0 practice); the record
     `curation/records/noaa_storm_events_damage.md`; the candidate table `.venv/bin/python -m
     data_foundry.curation.cli dataset windows noaa_storm_events_damage --root datasets/_dev/tabarena-v0pt2` (9
     years).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Three newest years (implemented) | tests 2025, 2024 and 2023 | the office practice closest to deployment; each refit trains on 83.3% or more | three adjacent years, three of the four lowest in damage; no year of catastrophic storms |
     | B | Spread evenly over nine years | tests 2025, 2021 and 2017 | the even spread over the eligible years; adds 2017, the costliest year, which the planner's annual loss includes | the oldest refit trains on 53.6%; a few catastrophic entries may decide the 2017 score; the measured signal in the notes is re-run |
     | C | Every third year | tests 2025, 2022 and 2019 | spread over seven years; every refit on 63.4% or more | no year of catastrophic storms; does not reach the oldest eligible years |

   * **Recommendation:** B: walking back has no reason of its own here, every candidate is a whole year with every
     season, and an even spread over the nine years puts a costly year next to the newest, as the planner's
     uncapped annual loss asks. **Decision:** A, B or C?

   **Notes for the AI:** on B, `temporal = Temporal(on="begin_time", splits=TemporalSplits(window=1, unit="years",
   cutoffs=(2025, 2021, 2017), gap=3, gap_unit="months"))`: test 45,870, 39,249 and 41,367 entries, train 793,017,
   622,584 and 451,520 (94.1%, 73.8%, 53.6%). On C, `cutoffs=(2025, 2022, 2019)`: test 45,870, 40,592 and 47,165,
   train 793,017, 661,889 and 534,532 (94.1%, 78.5%, 63.4%). Counts from the candidate table. Then rewrite
   `task_summary.split` ("a later calendar year (2023, 2024 or 2025)"), `splits_comment` (the years, the reason, the
   numbers above), the test-year cell counts in the score-unit bullet and the per-window results of the signal
   bullet (re-measure or date them as taken on 2023-2025); a CC line in the record, a dated CHANGELOG entry and
   `dataset check`. The windows tool should leave out the `unit_weight` unit (`cell`) as it leaves out the scoring
   columns; a framework note, not part of this decision.

   [^ns-split14]: **SPLIT-14** (Must): a temporal task has at least 3 windows, and no window's train side holds less
     than 50% of the data.
   [^ns-split15]: **SPLIT-15** (Must for the newest window, Should for the others; amended 2026-11-10, Lennart and
     Andrej): "The newest window is always a test window ... Prefer windows in other years, then other seasons, then
     other months, weeks or days, over the windows just before the newest. Walking back from the newest is one choice
     among others and needs its reason too, such as a history too short for others, or a use case that only cares
     about the weeks after a refit."

**Review panel:** ship after changes (mediator). Tier full, a re-review of 2026-11-06 under LEAK-41 and MET-14 to
MET-16, after decision D13 (issue 6): 12 reports. The mediator's issues 1 and 2 are issues 7 and 8 here (its option (a)
of issue 1, the blank, is option B of issue 7); its issue 3 is cross-dataset item X4, its issue 4 needs no decision (see
the outcome), and its issue 5 is applied: the record's leftover marker is removed. Claims: 27 audited; 19 hold, 7
refuted (the kept spans' worth, understated; "App. A read for every type", which missed Seiche; the metric reason's
manager; the share of types entered only with damage; two sets of stale counts; the record's marker) and 1 at risk (the
reason for dropping the unassessed hazards); 4 untested (the 2024 Local Storm Report match, the 2025 file comparison,
the office spread and drift, the RMSE figures of older definitions). All are fixed, in the definition or (the marker) in
the record, and one claim that held, that the kept worth is the criterion's rather than the damage's, was overturned by
the mediator's rerun (issue 7). Blind review: include with changes; its main concern, that a $0 is mostly an office's
reporting habit, is settled under LEAK-25 as amended, and the masking it calls undocumented is documented in the notes,
which its task sheet did not carry. Task gamer: nothing beats the honest model by more than noise plus about 0.01 RMSLE;
`magnitude_type` with the blanked speeds is worth 0.092 and the duration 0.013, both known at the stated prediction
point; no late labels and no training row after a cutoff. Agreed: the task, the split, D13 as applied, the Seiche blank,
the measured worth and every text fix, Flood and Flash Flood recorded as outcome-free, the spread of methods. Disputed:
the spans `magnitude_type` locates (issue 7: the advocate keeps them as first-report times, the critic blanks them as
Strong Wind's; the rerun met the tie-breaker both set, for the blank); the metric (issue 8, a weighing call); the
LEAK-10 amendment and the release of D13, settled as upkeep of the rules and the process, not defects (X4; Andrej's
release of D13: see the outcome). One reading of the panel is corrected: its quotes that time Hurricane and Tropical
Storm by "damage or" a wind criterion are App. A's marine sections (34, 39); the land types run on the storm's direct
effects (Sec. 25, 49) and are recorded as outcome-free.

<details><summary>Mediator</summary>

**Mediator report: noaa_storm_events_damage (exposure re-review, full tier, 2026-11-06)**

I ran the decisive experiment and the MET-1 probe. Both rebuttals had named these as the tie-breakers. Splits are the
shipped ones, in the order they ship.

**1. Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL-3 holds; USE-1, USE-5 hold (approximate fit, issue 5). LEAK-10 / spans Cases row: D13 is applied as
  decided (Tornado, Strong Wind, Heavy Rain 100% blank, 0% elsewhere; no marker, LEAK-38). LEAK-10 is triggered on
  the located damage-timed spans (EG/ES wind entries, Thunderstorm Wind measured under 50 kt). The rerun shows a gain
  on those rows, so blanking them is recommended (issue 1, a change to D13). Seiche: 51 durations blanked (agreed by
  both sides). LEAK-25 kept as amended. LEAK-37 note incomplete (text). SPLIT-9, SPLIT-10, SPLIT-13 hold.
  MET-14/15/16 and LEAK-41 are not triggered (no weight, no exposure).
Value: TP-3, methods spread (keep). MET-1: the reason names the old actor (text fix). The Tweedie probe picks a
  different model from RMSLE in 3 of 3 windows (issue 2, a weighing call).
Quality: stale counts, unnamed types and the record marker (text).
Weighed (metric): label precision +, tail dominance of dollar metrics +, planner sums dollars -, probe disagreement -.
For the curator: issue 1 (EG/ES blank: a, recommended), issue 2 (metric weighing), issue 3 (LEAK-10 amendment),
  issue 4 (Andrej's release of D13), issue 5 (record marker).
```

**2. Agreed facts (no side disputes them)**

- The task is real. USE-1/USE-5 hold with the planner as actor (issue 5, Andrej, 2026-11-03).
- The target equals log1p(DAMAGE_PROPERTY) in 100% of 9,527 matched 2024 rows (blind reviewer). Blanks are dropped, not
  set to $0.
- The split is right (split auditor):
  - gap of 3 months against a public lag of 75-80 days;
  - 0 episodes cross a window;
  - 0 training events end after the cutoff;
  - county_zone seen in train for 98.6-99.6% of test rows.
- D13 is applied exactly. Every App. A quote is verbatim (claim auditor, precedent checker).
- Blanking Strong Wind and Heavy Rain cost nothing (10 of 15 fits were better with the blank).
- `magnitude_type` marks the estimated-wind rows. EG/ES rows are 241,088 of the 318,813 kept-span rows (75.6%):
  Thunderstorm Wind 228,978 EG + 56 ES, High Wind 11,018 EG + 1,036 ES.
- In 2024, 94.4% of EG Thunderstorm Wind first reports were "TSTM WND DMG" with no speed. Separately, 435 Thunderstorm
  Wind rows carry a measured speed under 50 kt.
- The note's sentence "the part the damage set cannot be located row by row" is false. Both sides concede it.
- The note's worth "+0.012 to +0.021, an upper bound" is understated. Over 15 fits the measured worth is -0.009
  to +0.078, median about +0.03 (claim auditor T3). Both sides accept the wording "+0.01 to +0.08 ... median
  about +0.03" with "an upper bound" dropped.
- Even +0.08 is about 6% of the ~1.3 RMSLE gain over a constant. The keep of the column as a whole does not flip on this
  point alone.
- Seiche (Sec. 41): the begin is drawn "resulting in a fatality, injury or damage". Both rebuttals accept blanking the
  51 rows (advocate: "blank it, which is costless"; the critic holds blank and accepts the curator's call).
- Hurricane (482), Tropical Storm (3,837), Volcanic Ashfall (77) and Dust Storm (1,476) are timed "damage or criterion".
  Name them in the kept note.
- Flood and Flash Flood are timed by "threat to life or property". They stay, recorded as threat-timed and judged
  outcome-free. The worth has no consistent sign: -0.125 to +0.098 over 15 fits; Flash Flood alone -0.011 / +0.053
  / +0.071 (column auditor).
- Stale text:
  - `known` says 3.5-4.0%; shipped is 4.4-4.9%.
  - 1,072 double entries; shipped is 918.
  - 40% / 37% zone rows; shipped is 30.1%.
  - 8,135 codes; shipped is 7,697.
  - 167,629 episodes; shipped is 140,270.
  - EG 254,988; shipped is 252,451. ES 1,162; shipped is 1,151.
  - REVIEW issue 6 option A says "six"; it should say "seven".
  - Hail under 3/4 inch (504 rows, 67-89% positive) and Dust Devil are missing from the entered-only-with-damage list.
- Stale actor: "The manager" appears in the metric reason, in the REVIEW.md header and in the UNASSESSED filter's
  reason. The actor is now the planner.
- Population: rows with a blank damage figure are dropped. Blank rates run 0-98% by office (EAX 98%, ALY 96%), and 22.7%
  of 2025 source rows are blank. The handling is settled under LEAK-25. A task_summary sentence is missing.
- TP-3: methods spread (LightGBM 2.83 against linear 3.24), so the probe's no_spread flag does not hold. Keep.
- The record shows no release of D13 by Andrej, although the study's table assigns D13 to him.

**3. The decisive experiment: blank the EG/ES spans (and Thunderstorm Wind under 50 kt) against the shipped column**

Design:
- Variant "blankA": `duration_hours` set to NaN where event_type is Thunderstorm Wind or High Wind and magnitude_type is
  EG or ES, plus Thunderstorm Wind MG/MS under 50 kt. That is 241,523 rows.
- Shipped splits; 4 seeds; two LightGBM set-ups:
  - small: 400 trees, subsample 0.8, colsample 0.9 (the note's own set-up);
  - big: 1500 trees, lr 0.03, 127 leaves, close to the task gamer's model.
- Each seed is paired: the same seed fits both variants.
- Reported: RMSLE(blankA) - RMSLE(shipped). Positive means the span carried a gain on those rows.

| set-up | rows | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| small | EG/ES rows (mean of 4 seeds, SD) | +0.001 (0.022) | +0.013 (0.028) | +0.020 (0.024) |
| small | all rows | +0.001 | -0.002 | +0.008 |
| big | EG/ES rows (mean of 4 seeds, SD) | +0.031 (0.009) | +0.023 (0.005) | +0.030 (0.015) |
| big | all rows | +0.004 | +0.015 | +0.019 |

- Big set-up: 12 of 12 seeds are positive on the EG/ES rows, and the 4-seed ensemble gives +0.031 / +0.023 / +0.030.
- Small set-up: 9 of 12 seeds are positive. The gain is within one seed SD.
- For comparison, blanking all five kept types moves the EG/ES rows by +0.009 / +0.024 / +0.015 (small set-up). Most of
  the five types' worth sits on the located damage-timed rows.
- The U50 rows (12-63 per window) are too few to read on their own.

Reading:
- Under the stronger model the located part carries a consistent gain of about 3-4 seed SDs. Under the note's small
  model it is within noise.
- The precedent checker's 2-seed figure (+0.041) was high. Its sign holds.
- Both sides' stated condition is met: "If the 4-seed rerun shows a consistent gain on the EG/ES rows, take a" (advocate
  rebuttal point 1; critic rebuttal).

**4. Changes to make now (no decision needed)**

Each carries its rule. All are text fixes except the Seiche blank.

1. Kept-span note (LEAK-10 / spans Cases row; EV-2):
   - Drop "cannot be located row by row" and "an upper bound".
   - State the worth as "+0.01 to +0.08 RMSLE on these types' test rows depending on the model (median about +0.03)",
     and mirror it in REVIEW issue 6 and the leak_checks.md Cases row.
   - If the curator takes issue 1 option a, re-measure the worth of what is left of the column first and write that
     number instead.
2. Seiche (spans Cases row; both sides agree): blank its 51 durations by type, the same mechanism as the OUTCOME_SPAN
   blank. This extends D13's own reading, and the curator may veto. Add Seiche to the blank list in `changes`.
3. Name Hurricane, Tropical Storm, Volcanic Ashfall and Dust Storm in the kept-with-note bullet (spans Cases row).
   Reword "read App. A for every type" in the CC, the notes and the Cases row.
4. Add one clause (spans Cases row; LEAK-37), so no later reviewer reopens the point: "Flood and Flash Flood are timed
   by a threat to life or property (App. A), judged outcome-free and kept; their worth has no consistent sign (-0.13
   to +0.10 over 15 fits)."
5. Metric reason (MET-1): replace "The manager ranks counties by orders of magnitude" with the planner, and add the
   sentence the practitioner asked for: RMSLE scores order of magnitude, not summed dollars (the RMSLE-optimal constant
   for 2024 is $16 against a mean of $355,555). Fix the REVIEW.md header the same way.
6. UNASSESSED filter reason (USE-1): ground it on the planner: property damage is almost never entered for these hazards
   (99.1% $0, 0.5% of the dollars).
7. Population sentence (USE-3): add to task_summary.row: "events with a damage entry; offices leave 0-98% blank". No
   data change; LEAK-25 as amended stands.
8. `known` and notes (LEAK-37, USE-3): 4.4-4.9% of test rows, 95-96% of them damaged. Add "Hail under 3/4 inch" and
   "Dust Devil" to the entered-only-with-damage list.
9. Stale counts (EV): 918 double entries (in `changes` too); 30.1% zone rows / 30.1% without lat/lon; 7,697 codes;
   140,270 episodes; EG 252,451 / ES 1,151. Change "six" to "seven" in REVIEW issue 6. Alternatively, date each old
   figure "before the issue 2 drop".
10. Tornado line of the Cases row (precedent checker 1b): say that the tornado is blanked on the survey fact (Spearman
    0.83 with TOR_LENGTH), not on the row's own reading.

**5. Changes that need the curator (ranked: validity first, Must first)**

**Issue 1 (P4, LEAK-10 Must): blank `duration_hours` on the EG/ES wind rows and on Thunderstorm Wind rows measured under
50 kt?**

Problem:
- D13 keeps the five types' spans because "which criterion set a span is not recorded".
- On an EG/ES entry no wind of 50 kt or more was reported (94.4% were damage reports with no speed). Sec. 46's begin and
  end ("When damage first occurred" / "When damage ended") can then only be the damage.
- That is the same fact as Strong Wind's span, which D13 blanked.
- `magnitude_type` is a first-report feature and locates these rows (241,523; 75.8% of the kept-span rows).

Effect: the rerun above. On those rows the gain is +0.023 to +0.031 RMSLE (big model, 12 of 12 seeds) or +0.001
to +0.020 (small model). On all rows it is +0.004 to +0.019.

Advocate's best evidence:
- LEAK-37 admits whether damage was seen at the first report, and the LSR times are first-report facts.
- The association is weaker on EG rows: High Wind AUC 0.459 against 0.686 for MG.
- LEAK-7 favours keeping a valid signal.

Critic's best evidence:
- LEAK-37 admits that damage was seen, not how long it went on. The span's end is the preparer's merge of the damage
  swath.
- Treat like cases alike: Strong Wind was blanked on the same fact.
- The time-on-risk Cases row and LEAK-10's located-cells clause say: where rows can be located, fix them.
- The critic's rebuttal also notes that the AUC within EG rows measures separation, not worth. EG rows are 62.5%
  positive.

Ruling by rank:
- Both rest on P4 Musts.
- LEAK-37 does not cover the span's length, so there is no conflict there. The advocate's distinction between a speed
  estimated from damage and a report's clock time applies equally to Strong Wind, which the curator blanked.
- LEAK-6 lets a keep with a note stand only where the late part cannot be located and the traced part shows no gain.
  Here the part is located, and it shows a gain.
- LEAK-7 (Should) yields to the Must. Blanking only the located rows is itself the smallest fix: measured-gust and flood
  spans keep their signal.
- The blank repeats `magnitude_type` and the wind-speed gap, so it is no new marker (LEAK-38).
- Caveat: about 5.6% of EG entries had a spotter's estimated speed, so the location is close but not exact. That is the
  same standard as melbourne's batch-located blank.

Options (the precedent checker's prompt):
- (a) Blank the EG/ES rows and Thunderstorm Wind under 50 kt. The note keeps the measured-gust and flood spans, with
  their worth re-measured. Recommended: both sides' own tie-breaker is met.
- (b) Keep as is, with the note corrected: the EG/ES share and the worth on them, +0.001 to +0.031.
- (c) Blank all five types.
- (d) Amend the spans row: read spans type by type only, never located within a type.

Decision needed: a, b, c or d. Under a, the worth figure in change 1 must be re-measured on the new column.

**Issue 2 (P6, MET-1 Must, a weighing call): RMSLE against Tweedie deviance (p 1.5, on dollars)**

The probe: each candidate was trained for each metric (L2 on log1p for RMSLE; LightGBM tweedie p 1.5 on dollars for
Tweedie). One seed, untuned, no early stopping.

| window | RMSLE picks | Tweedie picks |
|---|---|---|
| 2023 | LightGBM 400x31 | event-type mean (2,660), ahead of LightGBM 100x31 (3,828) |
| 2024 | LightGBM 400x31 | LightGBM 100x31 |
| 2025 | LightGBM 1500x127 | LightGBM 100x31 |

- Among the RMSLE-trained models, Tweedie's own pick also differs from RMSLE's in all 3 windows.
- Under Tweedie, more capacity scores worse every year: 100 trees < 400 < 1500/127 leaves.
- The log-trained models' Tweedie scores range from 40k to 600k.
- RMSLE-trained predictions sum to 0.05-10% of the actual dollars.

Effect: the two metrics pick different models in 3 of 3 windows. This triggers the switch condition both sides set:
"switch only if they pick different models".

Each side's best evidence:
- For RMSLE (advocate, practitioner):
  - 44% of positive figures have one significant digit;
  - on dollars, 0.1% of rows hold 99.94% of the squared deviation;
  - no source metric exists (MET-5);
  - the practitioner: "I could pick a model by it".
  - My probe adds: Tweedie ranks a per-type mean first in 2023 and penalises capacity, which reads as tail-driven noise.
- For Tweedie (critic, practitioner):
  - the planner plans with summed expected dollars;
  - the RMSLE-optimal constant is $16 against a mean of $355,555;
  - the issue 3 metric call was made for the triage actor.

Rule: MET-1 (Must) and the tension row "the source's metric against a better metric" (there is no source metric). The
rules leave which framing to ship open.

Options:
- (A) Keep RMSLE, with change 5's reason plus a line that Tweedie was probed and disagrees, and why (tail-driven).
- (B) Switch to mean_tweedie_deviance p 1.5 on dollars (needs a CLEAN-16 check on the target transform).
- (C) Rerun the probe with tuned Tweedie fits and early stopping before deciding.

My lean is A, but it is the curator's weighing.

**Issue 3 (rule maintenance; principles.md "Exceptions and amendments"): amend LEAK-10 with a third clause for spans**

- What: spans drawn "by the outcome or an outcome-free criterion". Tie the clause to the second clause's test: blank the
  located part; keep the rest with a note only when its worth is small. Name heart_failure `time` (dropped: AUC 0.84
  alone, LightGBM 0.75 to 0.90) as the size counter-case.
- Both sides agree it is right. The advocate holds that it does not gate shipping. It does not: the dataset meets the
  rule either way once issue 1 is decided.
- Without it, the register will flag this keep under a Must, as it did loan_default's.
- Decision needed: adopt, adopt with different wording, or keep it as a Cases row only.

**Issue 4 (process, house rules): Andrej's release of D13**

- The study's decision table (report.md l.728) assigns D13 to Andrej, "in his folders, or with his release". The record
  shows Lennart's CC only. Andrej is `checked_by`.
- Decision needed: record his release, or confirm that he gave it, before merging.

**Issue 5 (bookkeeping, records.md): the record's `No Good Target / Scientific Discovery` marker**

- The marker sits on a `Yes` record. It belongs to the retire option of issue 5, which was not taken.
- Decision needed: remove it (one click).

**6. Disputed points and how they were settled**

| Point | Advocate | Critic | Outcome |
|---|---|---|---|
| EG/ES spans | keep with corrected note (LEAK-37, LEAK-7, spans row) | blank (LEAK-10 located cells, time-on-risk row, Strong Wind like-case) | Fact settled by the rerun: a consistent gain on the located rows (big model 12/12 seeds). By rank and by both sides' tie-breaker: a. It changes a curator decision, so it is issue 1. |
| Tweedie probe as a gate | not a gate; a weighing call | MET-1 Must, settle on evidence | Probe run: the metrics disagree in 3/3 windows. Not a failed Must on its face (the metric is defensible on the label's precision). A weighing call: issue 2. |
| LEAK-10 amendment and Andrej's release | maintenance, not a defect | needed | Both are right. Neither changes the data. Issues 3 and 4, not a condition on the data. |
| Seiche | blank (rebuttal) | blank, curator's call accepted | Agreed: blank (change 2). |
| "Worth is the criterion, not the damage" (advocate's support point) | AUC 0.459 against 0.686 | AUC measures separation, not worth | The critic is right. The rerun shows the worth sits largely on the damage-timed rows. |

**7. The task gamer's exploits (no rule IDs in its report)**

1. `magnitude_type` with the wind-speed gap, +0.092 mean (Thunderstorm Wind +0.21 to +0.26).
   - Rules: LEAK-37, LEAK-10, LEAK-38.
   - Known: the EG-blank bullet, dataset.py l.156, settled by the 2024 LSR match. It is a reasoned keep, not a
     `Potential leak, kept on purpose:` note, and no gain for the type itself is stated.
   - Not an issue. Optionally add the 0.09 figure to the bullet.
2. `duration_hours`, +0.013 mean (+0.000 / +0.004 / +0.034).
   - Rules: LEAK-10 and the spans Cases row.
   - Known: the kept-on-purpose note.
   - The gain differs from the note (all rows +0.001 to +0.015; 2023 is +0.034), so it is an issue. It is covered by
     change 1 and issue 1.
3. Tie size: rows sharing a begin_time, counted over train and test, +0.006 (noise ±0.004).
   - Rule: LEAK-9 (a method reading other test rows; transductive).
   - New, no note. At noise, so no action.
4. Lat/lon decimal count, +0.001.
   - Rule: a format marker (LEAK-38 class).
   - New, noise, no action.
5. Population: rows enter only when the office later entered a damage figure.
   - Rules: USE-3; LEAK-25 as amended.
   - Known in the notes (18% blanks dropped). Change 7.
6. Lookup in the public source file: true of any public dataset. Not ranked.

The gamer found no flaw that hurts an honest model: no late labels and no training row after the cutoff.

**8. Consistency with precedent**

- D13 is consistent with the precedents type by type, and its reversal of the 2026-11-03 definition states its fact
  (precedent checker 1a-1c).
- bank_marketing `campaign` (kept with a note, worth 0.0013-0.0016 once the period is known) is consistent.
- The one departure is the located part:
  - zillow_prize, melbourne_housing_market and frempl's located branch blank cells they can locate.
  - Strong Wind (the same day, the same curator) was blanked on the same fact as an EG span.
  - medical_facility_operational_data kept a part that could not be located and sat within about two seed SDs. Here the
    part is located, and under the stronger model it sits at 3-4 SDs. That sets it apart from medical_facility, not from
    zillow or melbourne.
- heart_failure `time` is the size counter-case for issue 3's amendment.
- No drift and no third exception is due.

Reflection prompt (the precedent checker's, updated with the rerun):

**Consistency check (AI, 2026-11-06):** your keep of `duration_hours` for Thunderstorm Wind and High Wind (D13, a keep
with a note) differs from Strong Wind (blanked by D13 the same day) and from zillow_prize and melbourne_housing_market
(located cells blanked, 2026-10-21) on the EG/ES rows. On those rows App. A's span can only be the damage's,
`magnitude_type` locates them (241,088 rows), and blanking them costs +0.023 to +0.031 RMSLE on those rows under the
stronger model (4 seeds, 12 of 12 positive), or +0.001 to +0.020 under the note's model. What sets them apart?
(a) Nothing: blank the EG/ES and the under-50-kt spans, and keep the note for the measured-gust and flood spans
(recommended).
(b) The first-report times make the EG span a LEAK-37 fact, recorded as an exception with that fact, which would also
reopen the Strong Wind blank.
(c) Blank all five types.
(d) Amend the spans row to read type by type only.

</details>

<details><summary>Claim audit</summary>

**Claim audit: noaa_storm_events_damage (exposure re-review, full tier, 2026-11-06)**

Definition: the dataset's `dataset.py` (README.md, REVIEW.md, record). NWSI 10-1605: the text extracted from the
PDF downloaded today (md5 7bf8de30dd420eef049401d387eef2ba).

**Verdict**

D13 holds as a decision: the blank hits exactly Tornado, Strong Wind and Heavy Rain. Every App. A quote checks out
against the PDF. The Strong Wind and Heavy Rain blank costs nothing. I found no sign that the kept spans carry a
damage-only signal. Two claims about the change are refuted:
- (a) The worth the note gives for the five kept types (+0.012 to +0.021 RMSLE) is the low end. It comes from one model
    set-up, untuned 400-tree LightGBM averaged over bagging seeds. The deterministic fit of the same run, and a stronger
    LightGBM, give +0.02 to +0.08.
- (b) "The study read App. A for every type" missed Seiche (Sec. 41): its begin time is drawn by "a fatality, injury or
    damage". 51 rows, not named in the notes.

Older claims are also refuted: stale counts left from before issue 2 (`known` 3.5-4.0% -> 4.4-4.9%; 1,072 double
entries -> 918; and others), the metric reason still naming "the manager" after issue 5 moved the use case to a planner,
and a `No Good Target` marker on a `Yes` record. None of these changes the task, the split or the metric. All of them
are fixes to the text.

**Tests run**

- T1 container facts, splits, scorer on a constant
- T2 raw files: counts, and the association of the duration with the label per event type, using durations from before
   any blank
- T3 the duration's worth on the shipped splits: 5 variants x 5 LightGBM set-ups x 3 test years.
   Variants: shipped; old (Strong Wind and Heavy Rain durations restored, aligned
   by the full-row key like the curator's script); blank5 (the five kept types blank too); blankFF (Flood and Flash
   Flood blank); nodur (no column). Set-ups: small_det = 400 trees, deterministic; small_bag1/2 = 400 trees, bagging
   seeds 1 and 2; big_det = 1500 trees, lr 0.03, 127 leaves, deterministic; big_bag1 = the same with bagging seed 1.
- T4 double entries before and after the unassessed-hazard drop, EG/ES counts, zone shares
- T5 missing begin_lat/lon against the label
- Source reads: NWSI 10-1605 App. A, the begin and end times of every type; Diaz and Joseph (2019), the study's text
extract; one more web search for a source metric.

**Claims table** (claim, source, test, result, evidence, rule)

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 1 | Duration blank for exactly Tornado, Strong Wind, Heavy Rain (62,694 rows, 7.4%; SW 18,243 + HR 20,836 = 39,079, 4.6%); kept for TSW, High Wind, Coastal/Lakeshore Flood, Storm Surge (318,813, 37.8%) | notes "Blanked", REVIEW 6, CHANGES.md | T1 per-type missing share | HOLDS | missing 1.000 for the 3 types, 0.000 for every other row; all counts exact; never negative, max 743.98 h | LEAK-10, LEAK-37 Cases row |
| 2 | App. A quotes: SW Sec. 45, HR Sec. 21, TSW Sec. 46, HW Sec. 24, floods Sec. 4/27/44, Tornado Sec. 47 | notes, REVIEW 6 | read the PDF (the extracted text, lines 1137, 2403, 2611, 3268, 4306, 4361, 4473, 4912) | HOLDS | every quote word for word | LEAK-10 |
| 3 | "the study read App. A for every type"; seven damage-timed types | notes CC 2026-11-06 | read the begin/end lines of all ~55 types | REFUTED (completeness, small) | Seiche (Sec. 41, line 4091): "Beginning Time - When water levels rose to initiate shoreline flooding, resulting in a fatality, injury or damage"; end "When water returned to pre-seiche levels". 51 shipped rows, 57% positive, kept as a feature with no note. Flash Flood (line 1845) and Flood (2041) are timed by "threat to life or property", not by damage: not damage-timed by the rule's reading, and their worth is not measurable (row 7) | LEAK-10, LEAK-37 Cases row |
| 4 | Kept five: "worth +0.012 to +0.021 RMSLE on these types' test rows ... +0.001 to +0.015 on all rows, an upper bound on that part" | notes "Potential leak, kept on purpose", REVIEW 6 resolution, leak_checks.md Cases row | T3 RMSLE(blank5) - RMSLE(shipped) on kept5 rows | REFUTED (understated) | kept5 rows, per year 2023/24/25: small_det +0.040/+0.027/+0.034; big_det +0.078/+0.020/+0.063; big_bag1 +0.044/+0.021/+0.032; small_bag1/2 -0.000/+0.036, +0.024/-0.009, +0.042/+0.030. Over 15 fits: -0.009 to +0.078, median about +0.034. On all rows up to +0.047. The curator's own run had the deterministic fit at +0.027 to +0.040 (the study's summary of that run) and reported only the bagged mean of the small model. The study's +0.020 to +0.038 sits in the same range | LEAK-10 / LEAK-37 Cases row ("a note giving its worth"), EV rules |
| 5 | The kept worth is mostly the wind/flood criterion, not the damage part ("the part the damage set cannot be located row by row") | notes | T2: within-type association of the old duration with the label, damage reports (EG) against measured winds (MG) | HOLDS (supports keeping) | High Wind MG: AUC(any damage) 0.686, Spearman 0.191; High Wind EG: 0.459, 0.013. TSW MG: Spearman with the positive amount 0.305; TSW EG: 0.159. The association is no stronger where damage set the span. Coastal Flood AUC 0.495, Lakeshore 0.521, Storm Surge 0.634 | LEAK-10, LEAK-37 |
| 6 | Strong Wind / Heavy Rain blank "costs nothing measurable: -0.009, -0.018, -0.046" | notes, REVIEW 6 | T3 RMSLE(shipped) - RMSLE(old) on SW+HR rows | HOLDS | 15 fits: -0.109 to +0.066, 10 of 15 negative (the blank is better). The noise floor on these rows is large: in the blank5 contrast, which leaves them untouched, they move -0.066 to +0.130. T2 shows no leak signal in the old values either: Heavy Rain AUC 0.402, Spearman -0.071; Strong Wind Spearman with the amount -0.059 | LEAK-10 |
| 7 | (implied) no other type's duration carries a measurable damage-timed worth | D13 scope | T3 blankFF on Flood + Flash Flood rows | HOLDS | ff rows -0.125 to +0.098 over 15 fits, no consistent sign. T2: Flood Spearman with the amount 0.451, Flash Flood 0.342 (a strong signal; the begin/end are threat-defined) | LEAK-10 |
| 8 | Blank by type, so "a blank is no survey marker" | notes | T1 | HOLDS | missing exactly when event_type is one of the 3 types; event_type is a feature already | LEAK-10, LEAK-38 |
| 9 | Tornado: duration tracks TOR_LENGTH (Spearman 0.83); 68% from "NWS Storm Survey" | notes | T2 | HOLDS | 0.831; 67.9% | LEAK-10 |
| 10 | Heavy Rain is "timed by the damage" | notes, REVIEW 6 | T2 | HOLDS on the text, WEAK in the data | 95.2% of Heavy Rain entries are $0, so whatever "damage" timed the span is not the property figure; the old duration has no leak signal (row 6). The blank is still costless | LEAK-10, LEAK-37 |
| 11 | Exposure: none; the duration is not an exposure; no weight, no offset | notes "Exposure", CHANGES.md | T1: sample_weight(c), scoring columns | HOLDS | sample_weight None, scoring_columns [], no denominator among the features. The target is one event's damage, not a count over a time at risk | MET-14, MET-15, LEAK-41 |
| 12 | County population: Spearman -0.14 to +0.05 with log damage | notes "Exposure" | read the study's log | HOLDS (study evidence, not re-run) | -0.139, -0.059, -0.052, +0.003, +0.049. Side note: the same log shows "+ log county population" at -0.014 and -0.020 RMSLE in 2023 and 2024 (+0.016 in 2025): a small feature gain, an outside join, not adopted | MET-14 |
| 13 | Metric: no source metric; Diaz and Joseph (2019) use accuracy/AUROC and MSE on log damage, tornadoes only, random split | metric reason | read the study's text of the paper; web search | HOLDS | "randomly partitioned ... training set (60%), cross-validation set (20%), and test set (20%)"; MSE 0.0918, accuracy 0.821, AUROC 0.872. The search found no competition and no benchmark metric | MET-1, MET-5, MET-11 |
| 14 | Metric reason: "The manager ranks counties by orders of magnitude" | dataset.py l.182, README Metric block | compare with the use case | REFUTED (stale actor) | issue 5 (B, 2026-11-03) made the actor a state hazard-mitigation planner (use_case l.71-76); the reason still cites the manager. The REVIEW.md header also still says "for an emergency manager ranking a storm's counties". RMSLE is still justified by the nine orders of magnitude | MET-1 |
| 15 | Metric computable per fold; constant RMSLE 4.05 / 4.28 / 4.20 | REVIEW issue 2 resolution | T1 scorer on a train-mean constant | HOLDS | scorer 4.0535 / 4.2779 / 4.2027, equal to a direct log RMSE (predictions on the log1p scale); unit per row; 44,056-45,870 test rows per fold | MET-2 |
| 16 | Raw dollars: the top 0.1% of entries hold 99.96% of the squared deviation; range $0 to $17B | metric reason | T1 | HOLDS (99.94% on the shipped rows) | max $17.0B | MET-11 |
| 17 | 68% of the entries are $0 | predicted, accepted warning | T1 | HOLDS | 68.13% | - |
| 18 | Split: test = calendar year 2023/2024/2025, train = every earlier event up to the end of September | split, splits_comment | T1 | HOLDS | train ends 2024-09-30, 2023-09-30, 2022-09-30; test 1 Jan to 31 Dec | SPLIT-10 |
| 19 | `known`: "some types are entered only with damage (3.5-4.0% of test rows)"; notes "3.5-4.0% of the test rows, 95-96% of them with damage" | task_summary.known, notes | T2: Strong Wind + Lightning + TSW with MAGNITUDE < 50 kt per test year | REFUTED (stale) | 4.56% / 4.41% / 4.94% (2023/24/25), 95.4-96.5% with damage. The old figure fits the denominator from before issue 2's drop | USE-3 accuracy, EV |
| 20 | `changes` and notes: "1,072 double entries" | changes, notes LEAK-19 bullet | T4 | REFUTED (stale) | 1,072 before the unassessed drop, 918 in the shipped definition. The type breakdown (248 TSW, 228 Hail) holds | LEAK-19 |
| 21 | Notes: zone events 40% of rows, 37% lack lat/lon, 8,135 county_zone codes; "no episode spans two months (0 of 167,629)"; EG 254,988 / ES 1,162 | notes | T1, T2, T4 | REFUTED (stale counts; the substance holds) | zone rows 30.1%, lat/lon missing 30.1%, 7,697 codes; 0 of 140,270 episodes span two begin months (1 has a different end month; no window effect with a 3-month gap); EG 252,451, ES 1,151 in the shipped rows | EV |
| 22 | Blank share 18% of 1,225,290; dropped hazards 156,767 (15.7%), 99.1% $0, 0.5% of the dollars | notes | T2 | HOLDS | 18.32%; 156,767 (15.66%), 99.08%, 0.52% | USE-1 |
| 23 | EF4/EF5 13 of 121 at $0; 17.3% of EF2+ | notes, accepted warning | T2 | HOLDS | 13/121; 517/2,990 = 17.3% | LEAK-25 |
| 24 | (implied) no row is a copy across the split | probes/leak.txt | read the probe | HOLDS | 0.0% of test rows have an exact copy in train once begin_time is included (14.8% without it) | LEAK-19, SPLIT |
| 25 | (implied) begin_lat/lon missingness is not an outcome marker | - | T5 | HOLDS | missing on 0.03% of the county rows and 100% of the zone rows: it follows cz_type, not the label | LEAK-38 |
| 26 | Record: suggestion 'Yes' with decision_markers [No Good Target / Scientific Discovery] | record front matter | read against records.md ("a clean dataset has none") and REVIEW 5 (B, ship) | REFUTED (inconsistent bookkeeping) | the marker belongs to option C (retire), which was not taken | records.md |
| 27 | Unassessed-hazard filter: "the hazards no one sends a damage assessor for" | task_summary.row, UNASSESSED comment | check against the current use case | AT RISK (wording) | the filter was justified by the manager's triage (issue 2, USE-1). Issue 5 replaced the actor with a planner. The rows (99.1% $0, 0.5% of the dollars) still make sense to drop for a property-damage planner, but the stated reason names a decision the use case no longer has | USE-1 |

**Untested (and why)**

- LSR match "94.4% of 12,498 EG events had no speed in the first report": needs the 2024 Local Storm Reports, not in
  the warehouse folder.
- "0 of 64,921 damage values differ between the 2025 files of January and August 2026": the older file is not in the
  raw folder.
- Office $0-share spread and drift (r 0.958 / 0.575, 30.5% of 82 offices): not re-run; not touched by today's change.
- RMSE figures of older definitions (2.626, 2.596, 4.537/4.796 tornado rows): they were measured on definitions before
  issue 2, so they cannot be reproduced on the shipped one. They are dated in the text.

**Refuted, ranked (validity first, Must first)**

1. Row 4, the worth in the "Potential leak, kept on purpose" note (LEAK-10 / LEAK-37 Cases row, a Must-level leak note
   that has to give its worth). The note reports the most favourable estimate as the worth and as "an upper bound".
   Measured worth is +0.01 to +0.08 RMSLE on the kept types' rows, median about +0.03, depending on the fit.
   What it changes: the number in the notes, REVIEW 6 and the leak_checks.md Cases row. The decision does not change:
   even +0.08 is about 6% of the ~1.3 gain over a constant, and row 5 shows the worth is not concentrated where damage
   set the span.
   Mildest remedy: write "+0.01 to +0.08 RMSLE on these types' test rows depending on the model (median about +0.03;
   untuned bagged LightGBM +0.012 to +0.021)" and drop "an upper bound", or say "an upper bound for this model".
2. Row 14, the metric reason cites "the manager" (MET-1, Must: the metric scores the use case's decision). The metric
   stays.
   Mildest remedy: "A planner compares events by orders of magnitude, so RMSLE ...". Also refresh the REVIEW.md header
   sentence.
3. Row 3, Seiche left out of D13's type reading (LEAK-10 / LEAK-37 Cases row). 51 rows: the begin is drawn by the
   damage,
   the end by an outcome-free level.
   Mildest remedy: add Seiche to the kept-with-note list (or blank its 51 durations; either way it costs nothing
   measurable).
4. Row 19, `known` and the notes state 3.5-4.0% for the damage-only types; the shipped value is 4.4-4.9%, with 95-96%
   of those rows damaged. This is a task_summary claim a reader acts on.
   Mildest remedy: update both numbers.
5. Rows 20 and 21, stale counts from before issue 2: 1,072 -> 918 double entries (in `changes` too); 40% / 37% -> 30.1%;
   8,135 -> 7,697 codes; 167,629 -> 140,270 episodes; EG 254,988 -> 252,451.
   Mildest remedy: recompute the counts on the shipped rows, or date them "before the issue 2 drop".
6. Row 26, the record's `No Good Target / Scientific Discovery` marker on a `Yes`.
   Mildest remedy: remove the marker (the curator's call; issue 5 resolved B).
7. Row 27, the reason for the unassessed-hazard filter names the old actor (USE-1).
   Mildest remedy: re-ground it on the planner ("property damage is almost never entered for these hazards: 99.1% $0,
   0.5% of the dollars").

**Sources**

NWSI 10-1605 (https://www.weather.gov/media/directives/010_pdfs/pd01016005curr.pdf, July 26, 2021 edition); Diaz and
Joseph 2019 (https://doi.org/10.1016/j.wace.2019.100216, the study's text extract); web search: no published metric for
this task.

</details>

<details><summary>Column audit</summary>

**Column audit (2026-11-06, exposure re-review, full tier): noaa_storm_events_damage**

VERDICT: ship after a note change. D13 is applied as decided and the column table is clean, except one gap
under the new LEAK-10 / LEAK-37 Cases row on spans the outcome sets. NWSI 10-1605 App. A also times Flash Flood
(74,914 rows, 8.9%, the third-largest type) partly by damage. Dust Storm, Seiche and Volcanic Ashfall are timed the
same way. None of these four is named in the `Potential leak, kept on purpose:` note. On Flash Flood test rows the
column is worth -0.011 / +0.053 / +0.071 RMSLE (2025/2024/2023), which is more than on the five types the note names.
No other column has a span or value that the damage sets beyond what is already settled. There is no training weight,
so probe 22 / LEAK-41 do not apply.

Prediction point checked against: the first curation_comments bullet ("a storm has passed, the event has ended and is
logged from the first reports (type, place, begin and end time, a measured wind speed or the hail size, whether damage
was seen), before any damage survey, claim or damage estimate").

How the evidence was produced:
- The frame was rebuilt through dataset_io.from_definition(raw=True): 843,144 rows, 13 features. The raw SOURCE,
  EVENT_ID and other raw columns were joined back by lineage.
- App. A's begin and end times for every type were read from the study's text extract
  of NWSI 10-1605 (26 July 2021).
- Model numbers: untuned LightGBM with 400 trees, subsample 0.8 and colsample 0.9, 4 seeds. Trained on the shipped
  windows (begin_time < 1 Oct of the year before) and tested on the calendar year. The test sets reproduce the shipped
  ones exactly (45,870 / 44,255 / 44,056 rows). begin_time enters as year fraction, month and hour. The score is RMSE on
  the log1p target, which is RMSLE. My overall RMSE is 2.74 / 2.98 / 2.96, against the definition's 2.67 / 2.93 / 2.94,
  because of the different hyperparameters. Read the deltas, not the levels.
- dtype probe (--no-fetch): it flags 1 column of 12, `event_type` as ordinal_like. That is a false positive: the event
  types are nominal (NWSI Table 1).

**Column table**

**log1p_property_damage_usd (target)**

- Meaning (codebook): DAMAGE_PROPERTY, "estimated amount of damage to property", parsed from "10.00K", shipped as log1p
- Known at the prediction point: the outcome
- dtype and cleaning: float. Blanks dropped (CLEAN-15), $0 kept. The name states the transform. The metric is rmsle with
  target_transform log1p, not a deviance, so CLEAN-16 as amended holds.
- Verdict: fine. The $0 mix is settled under LEAK-25 as amended.
- Rule: CLEAN-15, CLEAN-16

**event_type**

- Meaning (codebook): one of the permitted Storm Data events (NWSI Table 1); 34 levels left
- Known at the prediction point: yes, as the reported type. Two caveats already noted: a tornado's type can be settled
  by the survey, and some
  types are entered only with damage (LEAK-37 note; see problem 3)
- dtype and cleaning: category, nominal. The probe's ordinal_like flag is wrong: there is no order.
- Verdict: fine
- Rule: LEAK-37, CLEAN-14

**state**

- Meaning (codebook): state or territory name
- Known at the prediction point: yes
- dtype and cleaning: category; 55 levels after the marine drop
- Verdict: fine
- Rule: -

**cz_type**

- Meaning (codebook): C county / Z zone (marine types dropped)
- Known at the prediction point: yes
- dtype and cleaning: category: C 589,601 / Z 253,543
- Verdict: fine
- Rule: -

**county_zone**

- Meaning (codebook): state FIPS + C/Z + county or zone number
- Known at the prediction point: yes
- dtype and cleaning: category, 7,697 codes. A meaningful identifier turned into a place code; renumbered zones are
  minor (settled
  2026-11-01).
- Verdict: fine
- Rule: CLEAN-3, CLEAN-14

**wfo**

- Meaning (codebook): the forecast office whose area holds the event
- Known at the prediction point: yes
- dtype and cleaning: category, 123 offices
- Verdict: fine. It also carries the office's $0 practice, kept under LEAK-25 as amended.
- Rule: LEAK-25 (settled)

**magnitude_type**

- Meaning (codebook): EG/ES estimated gust/sustained, MG/MS measured. Filled only for Thunderstorm Wind, High Wind and
  Strong Wind
  (all of their rows); blank elsewhere.
- Known at the prediction point: yes: whether a wind report was a damage report or a measured gust is in the first
  report (LSR match of 2024,
  settled)
- dtype and cleaning: category
- Verdict: fine
- Rule: LEAK-10 (settled)

**flood_cause**

- Meaning (codebook): "reported or estimated cause of the flood"; filled for Flash Flood, Flood and Debris Flow only
- Known at the prediction point: yes (heavy rain, dam/levee break, ice jam, planned release)
- dtype and cleaning: category, 7 values
- Verdict: fine
- Rule: -

**begin_lat, begin_lon**

- Meaning (codebook): "begin point of the event or damage path"
- Known at the prediction point: yes: the place of the first report (an LSR carries lat/lon)
- dtype and cleaning: float, ranges valid. Missing on all Z rows and on 0.04% of C rows (138 rows: Winter Storm 119,
  Heavy Snow 8 and a
  few others). The C-row missingness does not follow damage (0.04% at $0, 0.00% positive), so it is no outcome marker.
- Verdict: fine
- Rule: CLEAN-10, LEAK-10

**begin_time**

- Meaning (codebook): begin date and time, local standard time (the split column too)
- Known at the prediction point: yes. For the damage-timed types, App. A sets the begin at "when damage first occurred"
  (Thunderstorm Wind, High
  Wind, Strong Wind and others), so the time is when the damage started, not how much it was. A check for rounding
  as a marker shows no effect: Thunderstorm Wind begins on a :x0/:x5 minute in 52.3% of rows, with a positive share
  of 0.568 against 0.554 on exact minutes, and Hail 0.100 against 0.095.
- dtype and cleaning: datetime
- Verdict: fine (a reading under the new Cases row: the start's timing does not carry the amount)
- Rule: LEAK-10/37 Cases row

**duration_hours**

- Meaning (codebook): end minus begin. App. A defines begin and end per type.
- Known at the prediction point: It depends on the type, as follows.
  - Blanked (D13, applied and verified): Tornado, Strong Wind and Heavy Rain, 62,694 rows, NaN on 100%. No NaN
    anywhere else, none negative, so the blank follows the type and is no marker.
  - Kept with a note: Thunderstorm Wind, High Wind, Coastal Flood, Lakeshore Flood and Storm Surge/Tide (318,813
    rows, counts verified). Each runs from "damage or criterion" to "damage ended or criterion".
  - NOT NAMED, same class (problem 1):
    * Flash Flood. Its begin is "When flood waters became an immediate threat to life or property", with four listed
      onset examples. One of them is "The point at which any amount of water comes in contact, flowing into, or
      causes damage to an above ground residence or public building". Its end is "no longer an immediate threat".
    * Dust Storm: begins when visibility reached the criterion "or began to cause a major impact".
    * Seiche: begins "When water levels rose to initiate shoreline flooding, resulting in a fatality, injury or
      damage".
    * Volcanic Ashfall: begins "When volcanic ash began to cause disruption to transportation, commerce, fatality,
      injury, or damage".
  - Outcome-free by App. A (my reading): Hail, Lightning (begin = end), winter types (accumulation; the "inferred
    by damage reports" criteria time is not in the data), Flood (threat to life or property, not damage), the
    tropical types (direct effects, guided by the TCP advisories), Wildfire (out of control to under control),
    Avalanche, Debris Flow, Dust Devil, Frost/Freeze, Tsunami, Astronomical Low Tide, Dense Smoke, Sneakerwave.
- dtype and cleaning: float, 0 to 744 h
- Verdict: Flash Flood, Dust Storm, Seiche and Volcanic Ashfall: a leak kept under the Cases row but missing from the
  note
  (problem 1). Otherwise fine as decided.
- Rule: LEAK-10, LEAK-37 Cases row (2026-11-06), LEAK-38

**hail_size_in**

- Meaning (codebook): maximum hail diameter in inches (MAGNITUDE for Hail; CLEAN-21 split)
- Known at the prediction point: yes. Hail sizes kept their value in 97.9% of the LSR matches.
- dtype and cleaning: float, 0.13 to 7.75. Missing for every non-hail row; no Hail row is missing it. No impossible
  values.
- Verdict: fine. Sizes under 3/4 inch mark outcome-selected rows (problem 3).
- Rule: CLEAN-21, LEAK-37

**wind_speed_kt**

- Meaning (codebook): measured gust or sustained wind in knots. EG/ES estimates are blanked.
- Known at the prediction point: yes for MG/MS
- dtype and cleaning: float, 17 to 149 kt. 79,581 values, all MG/MS. The impossible ones went with the estimates.
- Verdict: fine
- Rule: LEAK-10, CLEAN-11 (settled)

Dropped columns re-checked against the frame: SOURCE, CATEGORY, TOR_*, END_*, casualties, crop damage, narratives and
EPISODE_ID are absent. EG/ES speeds are NaN on all 253,602 EG/ES rows. The drops listed under "identifiers or copies"
are absent too.

**Problems, ranked (principles.md: P4 validity first, then P7 quality)**

1. LEAK-10 / LEAK-37 Cases row "a span or extent whose start or end the source defines by the outcome" (Must, P4).
   Flash Flood, Dust Storm, Seiche and Volcanic Ashfall are spans timed by the outcome or by an outcome-free criterion,
   kept, with no `Potential leak, kept on purpose:` note.
   Evidence:
   - App. A text, quoted in the table row for duration_hours.
   - Flash Flood is 74,914 rows (8.9%), 36.1% positive. Its duration ranks the positive damage at Spearman 0.342
     (Thunderstorm Wind 0.165, High Wind 0.233, Coastal Flood 0.436).
   - Blanking duration on Flash Flood rows only changes RMSLE on the Flash Flood test rows by:
       2025: -0.011 (SD 0.04-0.05), 2024: +0.053 (SD 0.01-0.04), 2023: +0.071 (SD 0.02); 3,619-5,383 rows per window.
     On all rows the change is +0.001 / +0.012 / +0.004. In the same runs, the five kept types moved by -0.004 to
     +0.003 because their duration was left in, a check that the runs are stable.
   - So the Flash Flood duration is worth about as much as, or more than, the five types the note names (+0.012 to
     +0.021).
   - Dust Storm (1,476 rows), Seiche (51) and Volcanic Ashfall (77, all $0) are too small to measure: 69-268 test rows,
     noise 0.03-0.10.
   - The note and CC say the study "read App. A for every type", and the Cases row lists only the five, so both claims
     need correcting.
   Strength: moderate. The span starts at damage to a building in one of four listed onset criteria. The others (road
   closed, 6 inches over a road, 3 ft ponded) are outcome-free, and the end is threat-based.
   Mildest remedy, which is what the Cases row prescribes for a mixed span: keep the column. Add Flash Flood (Sec. 20),
   Dust Storm (Sec. 11), Seiche (Sec. 41) and Volcanic Ashfall (Sec. 51) to the `Potential leak, kept on purpose:`
   note, with the Flash Flood worth measured on the shipped splits by the definition's own setup. Name them in the
   Cases row's example too. Re-word "read App. A for every type".
   Question for the curator: on Flash Flood the worth reaches +0.07, and the damage criterion is one onset example of
   four, not half of an "or". Keep with a note (the rule as written), or blank it (option C of issue 6 extended)?
   I lean keep: the rule as written applies, and the end is outcome-free.

2. Boundary reading for the curator (P4, question, no change proposed): Flood.
   - App. A: "When flood waters began to threaten life or property" until "no longer any threat to life or property".
     That is a threat, not damage, so I read it as outcome-free. A preparer can still date the threat by the first
     damage.
   - The duration ranks the positive damage at Spearman 0.451 on 48,454 rows, the highest of the large types, but a
     long flood is also a large flood.
   - Wildfire (Spearman 0.520) is timed by fire control, which is outcome-free.
   - Both end after damage assessments can start. That was settled under the prediction point "the event has ended"
     (audit of 2026-11-01, problem 4).
   - If the curator reads "threat to property" as the outcome, Flood joins problem 1 as a kept-with-note type.

3. LEAK-37 note completeness (Should, P7): hail under 3/4 inch is entered only with damage or an accumulation.
   - App. A, Hail: "all reports of hail that is 3/4 of an inch or larger ... will be entered. Observed hail
     accumulations of smaller sizes ... that cause property and/or crop damage, should be entered."
   - In the frame: 504 Hail rows under 0.75 in, 67-89% positive, against 1.9-5.0% at 0.75-1.0 in. 0.0-1.5% of Hail
     rows per year.
   - `hail_size_in` < 0.75 therefore marks a row selected by the outcome, the same mechanism as Thunderstorm Wind under
     50 kt (435 MG rows under 50 kt, 92% positive). The first report gives the hail size and whether damage was seen,
     so it stays (LEAK-37).
   - Remedy: add "Hail under 3/4 inch" (and Dust Devil, flagged 2026-11-01) to the first bullet's list of types entered
     only with damage, and update the 3.5-4.0% share if it moves (it is tiny). No data change.

4. dtype probe flag on event_type (ordinal_like): not a problem. It is nominal; no change.

**Settled and not reopened**

- D13 is applied and verified: the blanked types are 100% NaN, there is no NaN elsewhere, and the row counts in the
  notes check out.
- The Thunderstorm Wind kept-span carries a survey part I could locate but not remove without a marker. 49.9% of the
  NWS Storm Survey rows have a duration above 0, against 26.6% of the others. The positive share is 0.613 with a
  duration above 0 and 0.542 at 0. Blanking by SOURCE would make a missing duration the survey marker, which is why the
  definition blanks by type. This is consistent with D13's note and needs no change.
- The EG/ES blank, the hurricane category, SOURCE and the tornado duration were checked again and hold.
- No exposure or weight column ships. MET-14 / MET-15 and LEAK-41 do not apply, and the notes' exposure paragraph is
  consistent with the columns.

</details>

<details><summary>Split audit</summary>

**Split audit (2026-11-06, exposure re-review, full tier): noaa_storm_events_damage**

Verdict: right (with two carried-over notes, no change asked).

Today's change (D13: duration_hours blank for Tornado, Strong Wind, Heavy Rain; kept with a note for Thunderstorm
Wind, High Wind, Coastal Flood, Lakeshore Flood, Storm Surge/Tide) touches no split, and the split still mirrors the
application. The 2026-11-01 audit's one problem (SPLIT-10, gap 2 against a ~2.5-month public release lag) is settled:
gap=3 months ships and task_summary.split reads "every event published by the refit". The numbers below are
re-measured on today's frame (843,144 rows after the 2026-11-03 drop of unassessed hazards), which the earlier audit
(~1.0M rows) predates.

Method: definition loaded with load_definition(...)().to_container(); splits taken from
c.experiment_metadata.splits (never re-split); episode ids rebuilt from the raw files with the definition's own filters
(_dollars, UNASSESSED / Marine, the LEAK-19 de-duplication). Date masks (train: begin_time < 1 Oct of year-1; test:
the calendar year) reproduce the shipped train and test sizes exactly.

**What was checked, with numbers**

1. Regime (SPLIT-1, SPLIT-3, SPLIT-13, USE-10): holds. A planner estimates the damage of new events in known places
   over time, so temporal with known entities. Test rows whose county_zone is seen in train: 99.63% / 99.18% / 98.59%
   (2025 / 2024 / 2023); wfo and state 100% in all three.

2. Windows and sizes (SPLIT-11, SPLIT-14, SPLIT-17, SPLIT-20): hold.
   - 2025: train 793,017 (2007-01-01 .. 2024-09-30), test 45,870; train share 94.5%; test $0 share 0.687.
   - 2024: train 749,875 (2007-01-01 .. 2023-09-30), test 44,255; 94.4%; 0.679.
   - 2023: train 702,587 (2007-01-01 .. 2022-09-30), test 44,056; 94.1%; 0.691.
   - Full calendar years, so each test window covers every storm season. The train side is expanding from 2007, the
   format break the earlier audit measured (blank share 70-72% in 2000-2005, 7.3% in 2007).

3. Gap against the label delay (SPLIT-10): holds. gap=3 months (container: time_gap 3, months). Train ends 30 Sep, which
   matches the measured public lag (a month appears complete 75-80 days after its end; the 1 Jan public file holds
   events through September; C00510 "up to a 120 day delay possible").

4. Training rows whose label or inputs are not known at the prediction point (SPLIT-9, LEAK-24):
   - No training event ends after its window's cutoff (0 in each window) and no event begun before a test year ends
     inside it (0), so every training duration_hours and begin_time is complete at the refit.
   - Revised damage estimates: the training labels are those of the 2026 files, not of the files the actor would hold
     at each refit. Measured bound (earlier audit and the builder): 0 of 64,921 Jan-Oct 2025 values differ between the
     files of 16 Jan and 19 Aug 2026; 0.17% of 2024 values (14 changed, 107 blanks filled, 1.3% events added or removed)
     between Mar 2025 and Jul 2026. A diffuse rest, no shortcut. Still untested for older years (REVIEW item 43: the
     2012 file was rewritten on 26 Oct 2026, no earlier copy compared); since those years are far from every cutoff,
     a revision there is not a label the actor lacks at the refit, only a different archive version. No change.

5. Hidden groups, one storm's many county rows (SPLIT-13, LEAK-18): hold. 140,270 episodes in the shipped rows; 94.6% of
   the rows sit in episodes of 2 or more (median 3 rows, 90th pct 15, 99th 46, max 412). 0 episodes span two begin
   months (largest span 30 days 8 h, inside one month), 0 span two offices, and 0 episodes have rows on both sides of
   any of the three windows. Within a test year an episode's rows are correlated (the effective test size is nearer
   the episode count than the row count); this widens the noise of a score, it biases no method.

6. The type-specific blank of duration_hours on both sides of every window (today's change): reads the same.
   - Tornado, Strong Wind, Heavy Rain: 100% blank on train and on test in all three windows (train 22,053 / 17,491 /
     20,130 rows for the 2025 window; test 1,296 / 560 / 593; 2024 test 1,773 / 813 / 885; 2023 test 1,171 / 722 /
     762).
   - The five kept types and every other type: 0% blank on train and on test in all three windows. So the blank is a
     pure function of event_type, identical in meaning on both sides; overall blank share 7.5-7.6% train, 5.3-7.8% test,
     the difference only the type mix of the year.
   - The kept spans keep their meaning over time: Thunderstorm Wind is 69-78% zero-length with a 90th percentile of
     0.07-0.10 h in every year 2007-2025; the other four kept types have a median of 1.1-3.5 h and a 90th percentile
     of 10-21 h, with no break at any cutoff. The column's worth on the kept types (+0.012 to +0.021 RMSLE, REVIEW
     issue 6) was measured on these shipped splits, so the noted upper bound holds for the windows as shipped.

7. Training weight / time on risk (SPLIT-9, LEAK-41): not applicable. No ScoringColumn(role="weight"), no exposure and
   no offset ship (MET-14, MET-15 bullet), so no training side admits rows by a cut time on risk.

Alternative split: not fitted today. Nothing in today's change gives a reason to doubt the regime; the earlier audit's
random-split reference (overrates by 0.16-0.36 RMSE) and gap comparison stand, and the gap question is settled.

Problems, ranked by principles.md: none new.

**Notes carried over (no change to the split)**

- (a) SPLIT-9 / LEAK-24, low: training labels come from the 2026 archive, not the files of each refit; measured bound
    0-0.17% of values per year for 2024-2025, untested before (REVIEW item 43). Mildest remedy if ever wanted: none in
    the split; a dated note that labels are the archive's as of the download already covers it (download_description).
- (b) Episodes cluster the test rows (94.6% of rows in multi-event storms); worth a line for anyone reading score
    differences between methods on one window (SPLIT-21), not a split change.

</details>

<details><summary>Domain practitioner</summary>

**Domain practitioner: noaa_storm_events_damage, exposure re-review of 2026-11-06 (full tier)**

Actor played: the state hazard-mitigation planner of task_summary.use_case (Diaz and Joseph 2019), who estimates the
property damage of storm events from what is known about each event before its damage is assessed. The prediction point
in the first curation bullet is the logged event before any damage survey (first reports).

**Verdict**

- Fit: approximate (agree; USE-8). One sentence: the inputs are the planner's event description, but the label is a
per-event NWS office estimate whose $0 mixes "no damage" with "no estimate" by office, while the planner acts on
aggregate expected loss per county and hazard.
- D13 (duration): agree with B. What I would know matches the call type by type (below). No change asked.
- Exposure/weight (MET-14, MET-15, MET-16, LEAK-41): agree, none. Damage is not accrued pro rata over the duration, and
  I
do not price per hour of storm, so duration is no denominator and no weight. LEAK-41 does not apply.
- Metric: partly scores my decision (MET-1). RMSLE suits the precision of the label. It does not score the quantity I
plan with, the expected dollars. My choice would be mean_tweedie_deviance (p about 1.5) on the dollars, after a probe
that checks whether the two metrics pick different models. Not a Must.

**1. Do I have each input at the prediction point? (the question on duration, type by type)**

Shipped-data numbers (participant kit, 843,144 rows):

| Type | Rows | Duration 0 | Median hours | Spearman (duration, log damage), positive rows |
|---|---|---|---|---|
| Thunderstorm Wind | 261,454 | 72.9% | 0.0 | 0.165 |
| High Wind | 53,486 | 23.8% | 2.3 | 0.233 |
| Coastal Flood | 2,871 | 6.1% | 4.0 | 0.436 |
| Lakeshore Flood | 335 | 0.3% | 13.5 | 0.042 |
| Storm Surge/Tide | 667 | 10.3% | 15.0 | 0.175 |

Strong Wind / Heavy Rain / Tornado: all blank since D13.

- Thunderstorm Wind: yes, in practice. 73% of the entries have a duration of 0, which is a point event: one Local Storm
  Report time. The rest are swaths built from the times of the first gust and damage reports. Every one of those times
  is in the first reports. A damage report carries its time, and LEAK-37 already admits that the first report says
  whether damage was seen. What the reports do not give is the dollar amount. The remaining leak is the preparer's
  later merging of reports into a swath, which is small (Spearman 0.165) and is in the kept note.
- High Wind: yes. Its criteria are measured: ASOS sustained 40 mph or gusts of 58 mph (NWSI 10-1605 Sec. 24). I would
  read the span off the observations.
- Coastal Flood, Lakeshore Flood, Storm Surge/Tide: yes, better than for any wind type. "Flooding" is a water level
  above the gauge's flood threshold. NOAA tide gauges publish it in real time, so I know the span without any damage
  report. The strong relation on Coastal Flood (0.436 among positive rows) is mostly physics: a longer inundation does
  more damage. It is signal, not a leak. This is the type where I would most want the column kept.
- Strong Wind: no. By definition it is below the high-wind criteria, it is entered only with damage, and Sec. 45 times
  it by "When the wind started to cause ... significant damage" to "no longer caused ... damage". No measured
  criterion bounds it. All I would have is the time of a damage report, not an end. Blanking it is right, and the
  re-measurement shows it cost nothing (-0.009 to -0.046 RMSLE on its test rows).
- Heavy Rain: I would know a rain duration from gauges and radar, but not this one. The span is "the heavy rain that
  led to damage" (Sec. 21). Blank is right. Only 4.8% of its rows are positive, so it matters little.
- Tornado: no. The ground contact comes from the damage survey (settled 2026-11-03).
So: yes, I would know it for Thunderstorm Wind and Coastal Flood and not for Strong Wind. The line D13 draws (outcome
alone, against outcome or an outcome-free criterion) is the line between what I could and could not read off
observations. The Cases row on spans (LEAK-10, LEAK-37) applied here gives the answer a practitioner would.
- Small inconsistency to note, not to fix: Flood and Flash Flood (123k rows, the largest dollar types) are timed by
  "when flood waters began to threaten life or property" (Sec. on Flash Flood and Flood). That is an impact judgment,
  not damage, and I would know it from warnings and first reports. Spearman with the positive damage is 0.34 to 0.45,
  as high as Coastal Flood. Kept implicitly. It would be consistent to name it in the kept note as judged
  outcome-free, so a later reviewer does not reopen it.
- Inputs I would always have and the data lacks: the exposure of the place (buildings, values) and the warning
  issued. The exposure was tested (county population does not scale, Spearman -0.14 to +0.05) and settled as an
  outside join. Not reopened.

**2. Is the target what I act on?**

A proxy (USE-5). Planners do use this field: local hazard mitigation plans tabulate NCEI Storm Events losses by county
and hazard, and SHELDUS and FEMA's National Risk Index are built partly from it. So the label is the real planning input
and not a made-up quantity (issue 5, settled). But three gaps remain:
- (a) I act on the sum, the expected annual loss per county and hazard, not on one event. In 2024 the top 1% of rows
    hold 96.8% of the dollars.
- (b) Nominal dollars. I would plan in constant dollars. The note shows the positive median of Thunderstorm Wind falls
    ($5,000 to $2,000), which is office practice and not inflation, so deflating would not fix it. No change asked.
- (c) The $0 is partly "no estimate made" (settled under LEAK-25 as amended). For me, the office's $0 habit is noise I
    would not want a model to learn, yet 62% of the gain over a constant comes from the office. This is the gap that
    most lowers my trust (below).
I want a number in dollars: an expected loss, not a class.

**3. Does one row match one decision? Is the test data what I face?**

A row is one event in one county segment, and my unit is a county by hazard over a year. That is an aggregation gap,
already named in fit_reason ("A planner plans for kinds of events"). The test data, a later calendar year in known
counties and offices refit yearly, is what I face (SPLIT-13 holds). The 3-month gap matches the NCEI lag.

**4. Would I use this model?**

As a screening tool for the order of magnitude of an event type in a county: yes. As a basis for the dollar figure of a
mitigation plan: no, for two reasons. A model trained under RMSLE predicts about the geometric mean: the RMSLE-optimal
constant for 2024 is $16 per event, against a mean of $355,555, and summed it understates annual loss by four orders of
magnitude. And much of its skill is reporting convention (wfo). I would trust it more if its skill held with the office
fixed: a check per office, or the within-storm score the earlier panel tried, which picked the same model on 2024.

**5. Does the metric score my decision?** Partly (MET-1).
For: the label is coarse. 44% of the positive figures have one significant digit, and offices enter round values
($1K, $5K, $10K ...), so the label supports order-of-magnitude accuracy and no more. RMSLE scores exactly that, and it
does not let a few hurricanes and floods decide (on raw dollars, 0.1% of the rows hold 99.96% of the squared
deviation). As a planner ranking hazards and counties by order of magnitude, I could pick a model by it.
Against: my decision is a sum of expected dollars. RMSLE is minimised by exp(E[log(1+y)]) - 1, not by E[y], and it
gives 37-47% of the error to the $0 entries, where part of the $0 is the office convention.
What I would pick: mean_tweedie_deviance on the dollars with p about 1.5 (in the metric library; the standard loss-cost
score for zero-mass, heavy-tailed amounts). It is minimised by the mean, so predictions add up to the annual loss I
plan with, and its scale term (mu^(2-p)) damps the tail far more than RMSE. MET-6 and MET-7 do not apply: there is no
threshold or k. MET-8 and MET-9 do not apply: this is regression. MET-14 and MET-15 do not apply: no rate and no
denominator, so the Tweedie would be unweighted. Before any switch, run a probe: if Tweedie p = 1.5 and RMSLE pick the
same model over the 3 windows (as RMSLE and the within-storm score did on 2024), RMSLE stays and the reason should say
it was checked. This was resolved on 2026-11-03 for the triage framing (issue 3). The use case has since become the
planner's (issue 5, B), and the metric reason still says "The manager ranks counties by orders of magnitude". That
sentence names the old actor and should read "the planner" (EV text fix, MET-1).

**Gaps, ranked by how much they change the task**

1. Unit: per-event rows against the planner's county-by-hazard expected loss. The metric then scores a geometric mean,
   not the expected dollars (MET-1, USE-5). Named in fit_reason; the metric reason does not weigh it.
2. The label's $0 convention by office (LEAK-25 as amended, settled). It shapes much of the learnable signal.
3. The metric reason names "the manager" from the superseded triage use case. A text inconsistency after issue 5.
4. Flood and Flash Flood spans, timed by "threat to life or property", are not named in the duration note. Consistency
   of D13, no measured leak expected.
5. Nominal dollars. Minor, since the drift is practice, not inflation.

**What an expert would change**

- Keep D13 as shipped. Optionally add one clause to the duration note: Flood and Flash Flood are timed by threat
  (Sec. on Flood and Flash Flood), judged outcome-free, and kept without a potential-leak note.
- Replace "The manager" by "the planner" in the metric reason, and add one sentence that RMSLE scores order of
  magnitude, not expected dollars, so summing the predictions does not give the expected loss.
- Probe mean_tweedie_deviance (p = 1.5, on dollars) against RMSLE on the 3 windows. Switch only if they pick
  different models. A weighing call for the curator (MET-1, MET-10), not a Must.
- No exposure, weight or offset: agree with the exposure paragraph (MET-14, MET-15, MET-16; LEAK-41 not triggered).

**Sources**

- NWSI 10-1605 (July 2021, the exposure study's text extract): App. A begin and end
  times for Thunderstorm Wind (Sec. 46), High Wind (24), Strong Wind (45), Heavy Rain (21), Coastal Flood, Lakeshore
  Flood, Storm Surge/Tide (4, 27, 44), Flash Flood and Flood ("threat to life or property"), Wildfire, Debris Flow,
  Hurricane.
- Definition, README and REVIEW.md of noaa_storm_events_damage; the change note; the participant kit's data (my
  statistics).
- Diaz and Joseph (2019), Weather and Climate Extremes 25:100216 (as cited in the definition).
- Domain practice: local hazard mitigation plans (44 CFR 201.6 risk assessment) cite NCEI Storm Events loss history.
  SHELDUS and FEMA NRI draw on Storm Data. NOAA CO-OPS tide-gauge flood thresholds and ASOS high-wind criteria are
  measured in real time. These are from domain knowledge, not fetched this session.
- Rules: USE-1, USE-3, USE-5, USE-8, SPLIT-13; LEAK-10, LEAK-37 (Cases row on spans), LEAK-25, LEAK-41; MET-1, MET-6
  to MET-10, MET-14 to MET-16.

</details>

<details><summary>Blind review</summary>

**Blind review: noaa_storm_events_damage (target log1p_property_damage_usd, regression, temporal split on begin_time, 3
windows)**

Inputs used: the clean room's 200k-row sample (of 843,144) and its task sheet, the NCEI bulk-format PDF, and two raw
NCEI detail files (2010, 2024) downloaded for cross-checking. No other local files were opened.

Verdict: Include with changes. It is real NOAA data, the target matches the source exactly, the split is honest, and
there is clear signal (LightGBM R2 about 0.49 vs 0.19 for an event-type mean). But a large share of what is learnable is
how each NWS office reports damage, not the damage itself, and this should be documented or reduced.

**What the task is**

Each row is one NWS Storm Events record (county or zone, event type, time, magnitude). The target is the NWS
property-damage estimate in nominal USD, log1p. Plausible users: insurers, emergency managers, or researchers who want a
damage estimate from an initial storm report before an assessment exists, or who want to fill in missing damage values
in the database. The use is real but weak: the NWS fills in the damage field together with the rest of the record, so in
practice the "features" and the label become available at about the same time. Best framed as "estimate reported damage
from the storm-report attributes".

**Data checks (evidence)**

- Real and correctly built. For the 2024 sample rows with a unique (county_zone, begin_time, event_type) key in the raw
  2024 file (9,527 of 10,616), the target equals log1p(DAMAGE_PROPERTY) in 100% of rows. Row counts match "drop blank
  damage, drop marine/heat/drought/fog/etc. types": 2010 raw has 46,014 such rows vs 45,951 scaled from the sample; 2024
  has 44,298 vs 44,754. Zero share matches too (2010 0.640 raw vs 0.636 sample; 2024 0.679 vs 0.681).
- Blank DAMAGE_PROPERTY (17% of 2010 raw rows, 22% of 2024 raw rows) was dropped, not turned into 0. Good.
- 34 event types kept. Drought, Heat, Excessive Heat, Dense Fog, Cold/Wind Chill, Funnel Cloud, Rip Current, High Surf
  and marine types were removed. That is a sensible choice but it is not documented in task.md.
- Values are plausible: max 22.8 (about $8B), 68% zeros, 91.5% of nonzero values are multiples of $1,000, and the top
  five values ($1k, $5k, $10k, $2k, $3k) make up 52% of nonzero rows. This is typical of rounded human estimates.

**Concerns, most to least serious**

1. A zero target often means "damage not estimated", not "no damage", and this depends on the office. (Serious; a
   validity and interpretability issue.)
   Evidence: among Thunderstorm Wind rows, offices with at least 100 events have zero-damage shares from 0.01 (IND),
   0.015 (BUF) and 0.018 (AKQ) up to 0.993 (BYZ), 0.994 (ABR) and 0.995 (TFX); the median office is 0.54. For Hail the
   range is 0.38 (ILM) to 1.00 (BYZ, TAE, TFX). For Winter Storm it is 0.08 (CLE) to 1.00 (IWX, STO, TFX). In LightGBM
   gain importance, wfo ranks first (9.0M), ahead of event_type (8.7M) and county_zone (2.6M). Weather does not explain
   a 1% vs 99% split between neighbouring Plains offices; reporting habit does.
   The source treats 0.00K as a valid estimate ("damage_property Ex: 10.00K, 0.00K, 10.00M: The estimated amount of
   damage"), so zeros cannot be separated from "not assessed".
   Change: at minimum, document that the target includes office reporting habits. Better: drop (wfo, event_type) cells
   whose zero share stays near 1, or use only Hail and Thunderstorm Wind events from offices that report damage. Another
   option is a two-part framing. Keep wfo as a feature either way, because removing it does not remove the bias.

2. Several rows share one estimate within an episode, and the timestamp feature carries drift. (Moderate.)
   Evidence: in 2024, sampled rows average 2.6 per episode (maximum 39), and the episode mean explains about 70% of
   target variance. Example: BTV Winter Weather zones on 2007-01-01 all have $3,000 or $5,000. Because the split is
   temporal, this only leaks at window edges. However, removing the begin_time-derived feature cuts R2 from 0.486 to
   0.372, a sign of strong drift over time in reporting practice. Thunderstorm Wind zero share moves from 0.51 (2007) to
   0.35 (2010-12) to about 0.48 (2018+).
   Change: keep the temporal split, as it is right. Consider an episode-aware gap at the window edges. Expect methods
   that handle drift to be favoured.

3. Some columns were silently masked by the preparation and are not documented. (Moderate, mostly documentation.)
   - wind_speed_kt is set only for measured gusts (MG/MS). For estimated gusts (EG/ES) it is NaN, although the raw
     MAGNITUDE is 100% filled for Thunderstorm Wind (2024 EG mean 53.4 kt). Presumably this is deliberate, because EG
     speeds are often inferred from damage. That is defensible, but it is undocumented, and magnitude_type=EG still
     gives this away: EG rows have mean target 4.93 and 40% zeros, MG rows 0.60 and 93% zeros. Dropping magnitude_type
     does not change R2 (0.489 vs 0.486), because the NaN pattern of wind_speed carries the same information.
   - duration_hours is NaN for every Tornado, Heavy Rain and Strong Wind row (7.4% of rows), although the raw end times
     exist. Again, presumably this hides damage-path information, but it is undocumented. For other events, duration
     needs END_DATE_TIME, which is known only afterwards; that is acceptable under the "estimate from the full report"
     framing.
   - Tornado EF scale, path length and width are excluded. This is correct, because EF scale is damage-based by
     definition ("Enhanced Fujita Scale describes the strength of the tornado based on the amount and type of damage").
   Change: write these choices into task.md. Optionally drop magnitude_type or keep it consistently. A single "wind
   speed is damage-derived" flag would be more honest than half-masked speeds.

4. Dollars are nominal, not adjusted for inflation, from 2007 to 2025. (Minor.) Prices rose about 50% over this period,
   a shift of about 0.4 in log units. That is small next to an RMSE of about 3.0, but it is a systematic drift. Change:
   deflate to constant dollars, or note it.

5. Preparation details. (Minor.)
   - county_zone is a categorical with 7,395 levels; it is redundant with state/cz_type plus FIPS but useful.
     Acceptable.
   - begin_lat/lon are missing for all zone-based events (30%); this is structural and fine.
   - Duplicates: 585 rows with identical features in the 200k sample (0.3%), 560 of them fully identical. These are
     separate events (e.g. hail reports in one county at the same minute). Negligible.
   - begin_time is in local standard time, as the source says ("usually in LST"). Fine for month and hour features.
   - The latest year (2025) may still be revised by NCEI; the files carry creation stamps such as c20260728. Note it.

**Benchmark value**

LightGBM (600 trees) with expanding-window training, testing on 2020-21, 2022-23 and 2024-25: R2 = 0.468 / 0.486 / 0.502
(mean 0.486, RMSE 2.98). An event-type mean baseline gets R2 0.185. Without wfo and county_zone, R2 is 0.475; without
IDs and the timestamp, 0.394. The task is not trivial, has room between methods, is large (843k rows), and is a
realistic heavy-tailed, zero-inflated target. Worth having once concern 1 is documented or reduced.

**Could not check**

- The exact three test windows used by the harness (I used my own two-year windows).
- The full 843k table (only the 200k sample is given), and raw years other than 2010 and 2024.
- Whether office zero-rates reflect true no-damage policy in some places (e.g. rural Montana) rather than "not
  assessed". NWS Directive 10-1605 guidance on entering 0 was not read.
- Revision history of damage values between file versions.

</details>

<details><summary>Task gamer</summary>

**Task gamer: noaa_storm_events_damage (target log1p_property_damage_usd, RMSLE = RMSE on the shipped log1p values, 3
yearly test windows 2023/2024/2025)**

Verdict: the task barely games. I found no feature or rule that beats the honest model by more than noise plus about
0.01 RMSE. The columns that touch the outcome are worth 0.01 to 0.09, and a model logging the event from its first
reports has them.

Honest baseline (LightGBM on features() with date parts, 400 rounds, 127 leaves):
- r0f0 2.6118 | r1f0 2.9313 | r2f0 2.9426 | mean 2.8285
- Untuned LightGBM (31 leaves, 100 rounds, raw begin_time): mean 2.9178.
- Noise: two refits with an added random column gave means of 2.8321 and 2.8292. The spread is about +-0.004 on the mean
  and +-0.01 per split.
- Scale note: metrics.py inverts the log1p before the RMSLE, so predict on the shipped scale. Predicting expm1 values
  scores worse (3.03).

**Exploits and outcome-touched columns, ranked by gain (gain = baseline RMSE minus the variant's; for a column the
baseline already has, it is how much worse the model gets without it)**

| # | Exploit / column | Script | Honest | With it | Gain per split (r0,r1,r2) | Deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | magnitude_type + wind_speed_kt (EG estimated gust, whose speed the prep nulled, vs MG measured) | attacks_wind.py | 2.9206 (both dropped) | 2.8285 | +0.108 +0.082 +0.086 (mean 0.092); Thunderstorm Wind +0.21..+0.26 | Yes, mostly: an EG thunderstorm-wind row is a damage report (93% of 2025 EG narratives mention trees down or damage, vs 5% of MG). Spotter reports carry the E/M qualifier. | None needed. To be strict, drop magnitude_type for Thunderstorm Wind. |
| 2 | duration_hours (end time minus begin time) | attacks1.py, per_type.py | 2.8411 (dropped) | 2.8285 | +0.000 +0.004 +0.034 (mean 0.013) | Yes: the prediction point is after the event has ended | None |
| 3 | tie size: rows sharing the same begin_time, counted over train and test | attacks_tie.py | 2.8285 | 2.8222 | +0.003 +0.006 +0.011 (mean 0.006, at the noise level) | Roughly: simultaneous zone warnings are known when the event is logged | None |
| 4 | lat/lon decimal count (precision format) | attacks1.py | 2.8285 | 2.8277 | -0.010 +0.006 +0.007 (mean 0.001, noise) | Yes | None |

Per-event-type gain of duration_hours (RMSE without it minus with it; per split):
  Thunderstorm Wind +0.041 +0.025 +0.057; High Wind +0.021 +0.057 +0.019; Lightning +0.003 +0.136 +0.062;
  Ice Storm +0.071 +0.089; Winter Storm +0.061 -0.017 +0.010; Winter Weather +0.002 -0.006 +0.069;
  Hail +0.007 -0.038 -0.059; Flood -0.061 -0.067 +0.029; Flash Flood -0.070 +0.011 +0.111; Tropical Storm -0.153 +0.356
  (small n).
- The column most likely to be set by the outcome (a flood's span, recorded until the water recedes) gives no consistent
  gain. The consistent gain is in Thunderstorm Wind and High Wind, where a nonzero span marks a multi-report path.
  Spearman(duration, y) within type is at most 0.19 (Flood).
- Missingness: duration_hours is NaN for all Tornado, Heavy Rain and Strong Wind rows and for no others, so its gap only
  repeats event_type. The prep removed it for those types.
- wind_speed_kt missingness is exact: NaN for every EG/ES row (the prep nulled estimated speeds) and filled for every
  MG/MS row. Positive-damage rate: EG 62.5%, MG 10.8%. The gap therefore tells the outcome only as far as magnitude_type
  does (row 1). Dropping magnitude_type alone costs 0.002 because the wind gap stands in for it.
- Per-type gain of magnitude_type alone (with the wind gap kept) is noise: Thunderstorm Wind +0.007..+0.016, the other
  types -0.11..+0.15 on small n.

- Mechanism, finding 1: in NOAA Storm Data a thunderstorm-wind row with an estimated gust is almost always a damage
  report ("trees down"), and its gust is a default inferred from the damage: 50 kt in 6,173 of the 2025 EG rows, 52 kt
  in 4,672. The prep nulled those speeds but kept magnitude_type, and the null pattern carries the same bit. Whether the
  event was a damage report is known when the first report is logged, so this is signal at the stated prediction point,
  not an exploit. What would decide it: whether the benchmark means "first reports" to include the reporter's own damage
  description. If not, drop magnitude_type for Thunderstorm Wind and Strong Wind (cost about 0.09).
- Mechanism, finding 2: duration is end minus begin. Under the stated prediction point (event ended, before the damage
  survey) it is known. Gain 0.013, concentrated in the wind types.
- Mechanism, finding 3: tie_n counts other rows starting the same minute, across train and test. Zone products (winter
  storms, high wind) start many rows at once. The gain is at the noise level.

**Flaws that hurt an honest model**

I found none that I could measure in the kit.
  - Recent-only training (honest_variants.py): rows from 2012 on 2.8332, from 2016 on 2.8331, from 2019 on 2.8479, all
    against 2.8285. Old rows do not hurt.
  - Label rate of the last training months vs the test windows: no sign of late-filled labels. Last-12-month positive
    rate is 0.29 to 0.32, and the test windows are 0.31 to 0.32.
  - Population flaw (not measurable in the kit): the source leaves DAMAGE_PROPERTY blank on 22.7% of 2025 rows, and the
    kit has no such rows. 2025 has 72,360 source rows and 45,870 kit rows; the kit also drops marine event types. A row
    is in the task only if its office later entered a damage figure, which is not known at the stated prediction point.
    Blank rates run from 0% to 98% by WFO (EAX 98%, ALY 96%). Among non-blank rows, the positive share rises only from
    0.19 (offices with under 5% blanks) to 0.25 (over 70% blanks). So the selection on the label field slightly enriches
    positives at offices that leave blanks. A deployed model would also face events left blank. Mild fix: state in
    task.md that the population is events with a damage entry, or keep the blanks as their own documented class. A test
    window cannot hold rows the deployed model would see, so this cannot be scored here.

**Attacks that found nothing (mean RMSE; baseline 2.8285; noise +-0.004)**

  - Row position as a feature: 2.8374 (worse). Rows are sorted by begin_time. Within ties, the order matches no column
    (state is monotone in 60% of ties, county_zone in 43%, event_type in 66%). Mean y by relative position in a tie is
    flat (2.38 to 2.65, no trend). Rank in tie 2.8272; relative rank 2.8285.
  - Next-row label agreement 0.708 vs 0.566 by chance: these are clusters from the same storm. Test labels are not
    available, so it is not usable.
  - Same-day counts over train and test (wfo, state, county_zone, event_type x wfo, all): 2.8445 (worse).
  - Begin minute / minute 0 / minute divisible by 5: 2.8304 (no gain). Positive rate is 0.22 at minute 0 vs about 0.36
    otherwise, which the model already gets from time and type.
  - Format-only features alone (decimals, minute format, duration format, missing flags): 3.632. event_type alone 3.766.
    event_type + formats 3.595. The format gain is the missing flags repeating event type and EG/MG. Over the full model
    the formats add nothing (row 4).
  - Exact feature twins across the split (all features but time): 14-16% of test rows have one. Twin-mean RMSE on those
    rows is 3.10-3.23, worse than the model.
  - Transforms over all rows: none shipped (lat/lon and magnitudes are raw values). Gap between train and test: train
    ends Sep 30 and the test starts Jan 1, so there are no cross-boundary episodes.
  - Training rows dated after the prediction point: none (train max < test min on every split).
  - Lookup in the published source file (StormEvents_details d2023-d2025): matching on begin_time + county_zone +
    event_type recovers DAMAGE_PROPERTY. This works, as it does for any public dataset, and is not ranked.
  - Web: no competition, forum or "leak" thread for this table. Published work (CU Boulder tornado-damage paper; dos
    Santos 2016 on database reliability) notes that damage is "as reported", that coverage changed over time, and that
    zero damage is common. None of it gives an exploit that applies here.

**What I could not check**

  - Score effect of the blank-damage filter: the kit has no blank rows. Rebuilding them from the source would be
    building a different task.
  - Whether magnitude_type in the final database is ever revised after a damage survey, which would make EG partly later
    information. The 2025 narratives suggest it is set from the first damage report.
  - Damage revisions between NOAA file versions (the source files are versioned c2026xxxx). I compared one version only.

Sources: https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/ (details files d2023, d2024, d2025; only d2025
was compared), https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/Storm-Data-Export-Format.pdf,
https://arxiv.org/pdf/1606.06973,
https://deepai.org/publication/some-comments-on-the-reliability-of-noaa-s-storm-events-database

</details>

<details><summary>Precedent check</summary>

**Precedent check for D13 in noaa_storm_events_damage (REVIEW issue 6, Lennart, 2026-11-06), full tier**

**Verdict.** On the type-by-type reading, D13 is consistent with the precedents. Where it reverses an earlier call, it
gives a fact for the reversal. It has one gap: its "keep with a note" for the five types rests on a premise the data
contests. The definition says the damage-set part "cannot be located row by row". But the column `magnitude_type`, which
is known at the first report, locates most of it. That is a departure without a stated reason, so a reflection prompt is
drafted below. There are also two smaller findings: types the type-by-type reading left out, and a rule-text gap.

**1. D13 against each precedent**

**a) The new LEAK-10 / LEAK-37 Cases row on spans the outcome sets (Lennart, 2026-11-06).**

- D13 is the row's founding case, so it is consistent by construction.
- Strong Wind (Sec. 45: "When the wind started to cause a fatality, injury, or significant damage") and Heavy Rain (Sec.
  21: "the heavy rain that led to damage") are timed by the outcome alone, so they are blanked.
- Thunderstorm Wind (Sec. 46), High Wind (Sec. 24), and Coastal Flood, Lakeshore Flood and Storm Surge/Tide (Sec. 4,
  27, 44) are timed by "damage or" a criterion. They are kept with a note.
- I checked every quote against the study's NWSI text and they are verbatim.
- On how thoroughly each type is argued:
  - Thunderstorm Wind and the three flood types are quoted in full.
  - High Wind is only "likewise". Its actual text is "When damage first occurred, or when sustained winds or gusts first
    equaled or exceeded locally/regionally established criteria" / "When damage ended or sustained winds or gusts
    dropped below high wind criteria". It fits the kept branch.

**b) Tornado duration (Andrej, 2026-11-03; earlier panel issue 4, claim 23).** Consistent: D13 keeps the blank. The
tornado blank rests on a different fact from the new row.
- NWSI times a tornado by ground contact ("When the sub-cloud vortex first contacted the ground"), which is a criterion
  without the outcome. Read literally, the row would keep the tornado duration.
- It stays blank because the damage survey sets the span: Spearman 0.83 with the dropped `TOR_LENGTH`, and +0.16
  to +0.26 RMSLE on tornado rows. That is a survey product, not a first-report fact, which sets it apart from digicow
  `topics_list` (LEAK-37, 2026-10-21).
- The row's case text does say "a tornado's span and path come from the damage survey". It would help to say outright
  that the tornado is blanked on the survey fact and not on the row's reading.

**c) The dataset's own earlier call (column audit 2026-11-01; definition shipped by Andrej 2026-11-03, tornado only).**
D13 reverses it for Strong Wind and Heavy Rain and states the fact that sets the new call apart.
- The audit quoted the Thunderstorm Wind entry alone. The study of 2026-11-05 read App. A for every type.
- The blank costs nothing measurable: -0.009, -0.018 and -0.046 on those types' rows.
- This is a legitimate reversal: a newer, better-read decision, not drift.
- Process point, not a consistency departure: the study's decision table (report.md line 728) assigns D13 to Andrej, "by
  Andrej in his folders, or with his release". The record and REVIEW show Lennart's decision but no release from Andrej.
  Confirm that he released it.

**d) heart_failure `time` (Lennart, 2026-09-30, dropped).** This is a real pair of similar cases decided the other way,
and the difference can be seen in the evidence.
- Follow-up ends at death OR censoring. That is structurally the row's "outcome or outcome-free criterion" branch, which
  keeps with a note.
- It was dropped, on its size: alone ROC AUC 0.84; with it LightGBM scores 0.90, without it 0.75.
- noaa's kept part is worth +0.012 to +0.021 RMSLE against a gain of about 1.3 over a constant, and the noaa prediction
  point is after the event has ended.
- So D13 is distinguished, but the row names no size limit. Read literally, it would have kept heart_failure's `time`.
- Suggestion: add heart_failure to the row as its counter-case, with the condition that a dominant worth goes under
  LEAK-6.

**e) bank_marketing `campaign` (Lennart, 2026-11-06, kept with a note under the same row).** Consistent with D13.
- The count of calls ends at a subscription or when the bank stops calling.
- Worth 0.006 ROC AUC overall, and 0.0013 to 0.0016 once the period is known (about one seed SD).
- The same day, bank_marketing dropped `day`/`month` of the last contact. That matches noaa dropping its end columns and
  keeping only the span.

**f) LEAK-10's second clause and LEAK-6 on size.**

- D13 is consistent on size with medical_facility_operational_data (Lennart, 2026-11-05). There, the whole-field worth
  is an upper bound and sits within about two seed SDs. D13's +0.012 to +0.021 sits against SDs of 0.016 to 0.030.
- It is unlike distribution_transformers_at_cauca_department (Lennart, 2026-10-21, dropped: a clear gain that could not
  be located).
- The same clause and the time-on-risk row (amended 2026-11-06) also say that where the late or outcome-set rows can be
  located, they are blanked. Precedents: zillow_prize and melbourne_housing_market (2026-10-21), frempl's located
  branch. Section 2 is about this.

**g) Drift and third exception.**

- No drift: Lennart's LEAK-10 keeps (2026-10-26, 2026-11-05, 2026-11-06) all rest on a small or no measurable gain.
- No third exception of one kind is due.
- But this keep sits under a Must and is written only as a Cases row. LEAK-10's text was amended in place for its two
  earlier keeps (window sums; late pulls), and LEAK-6's narrowing sentence names only the late pull and LEAK-41.
- Under principles.md, a keep under a Must is an amendment. LEAK-10 should get a third clause, or the row should be tied
  to the second clause's test. Otherwise the register will flag it like loan_default's exception_to_must.

**2. The departure without a stated reason: the located part**

- The definition's kept-with-note bullet says: "Which of the two set a given span is not recorded, so the part the
  damage set cannot be located row by row."
- But the same definition already blanks the estimated wind speeds by `magnitude_type`. EG and ES are speeds estimated
  from the damage, and 94.4% of 2024's EG Thunderstorm Wind entries had a first report "TSTM WND DMG" with no speed.
- For such an entry, no wind of 50 kt or more was reported, so the Sec. 46 begin ("When damage first occurred or winds
  50 knots ... were first reported") can only be the damage.
- Counts on the shipped container, among the five kept types:
  - EG/ES rows: 241,088 of 318,813 (75.6%). Thunderstorm Wind 228,978 EG and 56 ES; High Wind 11,018 EG and 1,036 ES.
  - Thunderstorm Wind with a measured speed under 50 kt: 435 more. Their spans must be damage-timed.
- Indicative probe (my own untuned LightGBM, 300 trees, 2 seeds, the shipped splits in container order; not the panel's
  setup):
  - Blanking the duration only on the EG/ES rows changes RMSLE on those rows by +0.041, +0.009 and +0.003.
  - Blanking it only on the other kept rows: -0.002, -0.008, -0.010 on the EG/ES rows. On their own
    rows: +0.032, -0.004, +0.053.
  - So where the column has worth, part of it sits on the rows that can be located. The numbers are noisy and need the
    panel's 4-seed rerun.

Reflection prompt, in the turn shape:

**Consistency check (AI, 2026-11-06):** Should the duration also be blanked on the wind entries the first report gives
as damage, since `magnitude_type` locates them?
   * **Problem:**
     - The note keeps the duration of the five types because the damage-set part "cannot be located row by row", but an
       estimated-speed entry (EG or ES) was reported as damage, so its span starts at the damage[^c1].
     - These are 241,088 of the 318,813 kept rows (75.6%), and `magnitude_type`, known at the first report, already
       drives the blank of their speed without a marker.
     - Where the rows can be located, the precedents blank them (zillow_prize, melbourne_housing_market, frempl), and
       keep with a note only what cannot be located[^c2].
   * **Experiments:** a rough check (2 seeds, untuned) puts blanking on those rows at +0.041, +0.009 and +0.003 RMSLE on
     their rows; the panel's 4-seed run would settle it.
   * **Consistency:** heart_failure's `time` was dropped on its size, and bank_marketing's `campaign` kept on its size;
     neither had a located subset.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Blank on EG/ES rows too | the duration is also blank where the speed was estimated from the damage; the note keeps the measured-gust and flood rows | follows the located-rows precedents; no new marker, the blank follows a known column; removes most of the damage-set spans | an inference from the NWSI wording, not a recorded field; loses whatever valid wind-criterion signal those rows hold |
     | b | Keep D13 as is (implemented) | the note stays, with the EG/ES fact and its measured worth added | keeps the signal; the worth is about one seed SD | the note's premise ("cannot be located") is no longer accurate |
     | c | Blank all five types | the duration is blank wherever the damage can set the span | no damage-set span stays | loses the flood and measured-wind signal, which is a first-report criterion |
     | d | Amend the rule | the spans row says a span is read type by type only, never located within a type | one reading for every dataset | goes against LEAK-7's smallest fix and the located-rows precedents |

   * **Recommendation:** a, after the panel's 4-seed rerun of the EG/ES blank. If that shows no gain, b with the note
     corrected. **Decision:** a, b, c or d?

   [^c1]: **LEAK-10** (Must): a feature never gives the target away; a consequence of the target is out. NWSI 10-1605
     Sec. 46: "When damage first occurred or winds 50 knots (58 mph) or greater were first reported".
   [^c2]: **LEAK-7** (Should): the smallest fix that keeps a valid signal. LEAK-10's second clause and the time-on-risk
     Cases row (2026-11-06): where the rows can be located, blank them; keep with a note only what cannot be located and
     shows no gain.

**3. Types the type-by-type reading left out (fix in the note; one small choice)**

App. A also times these types, still in the data, by "damage or" a criterion. The definition neither blanks them nor
covers them in its note:
- Hurricane (Typhoon), 482 rows: "When winds of 64 knots or greater first occurred or when a fatality, injury, or damage
  began". Kept branch.
- Tropical Storm, 3,837 rows: the same with 34 to 64 kt. Kept branch.
- Volcanic Ashfall, 77 rows: "disruption to transportation, commerce, fatality, injury, or damage". Kept branch, 0%
  positive.
- Seiche, 51 rows: "When water levels rose to initiate shoreline flooding, resulting in a fatality, injury or damage".
  The begin is conditioned on the outcome, close to Strong Wind, so under the row it would be blanked.

Flood and Flash Flood are timed by a "threat to life or property", a forecaster's judgement, not the damage, so I read
them as outside the row. Together these types are about 4,450 rows (0.5%).

Recommendation: list Hurricane, Tropical Storm and Volcanic Ashfall in the kept-with-note bullet, and decide Seiche
(blank, by the row). Without this, the claim that every type was read type by type does not hold for the whole set.

**4. Minor**

REVIEW.md issue 6, option A says "the six other damage-timed types". The list and the experiments count seven (Strong
Wind, Heavy Rain and the five). The issue is resolved, so this is text only.

</details>

<details><summary>Advocate</summary>

**Advocate, opening brief: noaa_storm_events_damage (exposure re-review, full tier, 2026-11-06)**

Position: ship as defined, after text fixes to the notes and the metric reason. None of the panel's findings touches the
task, the split, the target or the metric. Every problem found is fixed by rewriting a note (the "keep with a documented
note" step of the remedy ladder), plus at most one costless blank (Seiche, 51 rows).

1. The task is valid at the top ranks, and no agent disputes that (P3 USE-1/USE-5 Must, P5).
   - Evidence, use case: the domain practitioner says the label is "the real planning input and not a made-up quantity".
     Local hazard mitigation plans tabulate NCEI losses, and SHELDUS and FEMA's National Risk Index draw on Storm Data.
     The actor was set to the planner in issue 5 (Andrej, 2026-11-03).
   - Evidence, the data: the blind reviewer, working from the raw NCEI files, found the target equals
     log1p(DAMAGE_PROPERTY) in 100% of 9,527 matched 2024 rows. Blanks were dropped, not turned into $0. Its verdict is
     "Include with changes".
   - Why this outranks the objections: every objection below is P4 note completeness, P6 metric wording or P7
     bookkeeping. By principles.md, "A real task against a leak": fix the leak, keep the task.

2. The split is right, with no new problem (P4: SPLIT-10, SPLIT-13, SPLIT-9; LEAK-18).
   - The split auditor's verdict is "right".
   - The gap is 3 months against a measured public lag of 75-80 days.
   - 0 episodes have rows on both sides of any window, and 0 training events end after the cutoff.
   - Test rows whose county_zone is seen in train: 98.6-99.6%.
   - Once begin_time is included, 0.0% of test rows have an exact copy in train (leak probe).
   - The task gamer found no training row dated after its prediction point, and no gain from late labels.
   - Why it outranks: nothing the critic can raise on columns reaches the split, and P4's split half holds outright.

3. D13 is applied exactly and costs nothing (LEAK-10 Must, the LEAK-10/LEAK-37 Cases row on spans of 2026-11-06,
   LEAK-38).
   - The claim auditor found every App. A quote verbatim against the NWSI PDF.
   - The blank is 100% on Tornado, Strong Wind and Heavy Rain and 0% elsewhere, on both sides of all three windows. So
     it is a pure function of event_type and no outcome marker (LEAK-38).
   - Blanking Strong Wind and Heavy Rain is costless: 10 of 15 fits are better with the blank, and the old values show
     no leak signal (Heavy Rain AUC 0.402).
   - The task gamer, playing to win, "found no feature or rule that beats the honest model by more than noise plus about
     0.01 RMSE". The duration overall is worth a mean of 0.013.
   - The practitioner says D13's line is "the line between what I could and could not read off observations".
   - Why it outranks: under the Must, the curator's decision holds on the facts. The newer curator decision beats the
     older call (precedence in the process), and the precedent checker confirms the reversal "gives a fact for the
     reversal".

4. The kept spans are legitimate inputs. Their worth is understated, and I concede that; the fix is the number in the
   note (LEAK-37 Must, LEAK-6 Must, the Cases row).
   - Concede: the note's "+0.012 to +0.021, an upper bound" is the most favourable set-up. Over 15 fits the worth
     is -0.009 to +0.078, median about +0.03 (claim auditor T3). The study's own +0.020 to +0.038 sits in that range.
   - What keeps the column:
     - Even +0.08 is about 6% of the ~1.3 RMSLE gain over a constant.
     - The association is weaker where damage set the span than where a measured wind did. High Wind: EG AUC 0.459
       against MG 0.686. Thunderstorm Wind: EG Spearman 0.159 against MG 0.305. So the worth is the wind or flood
       criterion, not the damage.
     - The practitioner: the Thunderstorm Wind span is built from first-report times, and coastal flood spans come from
       tide gauges published in real time ("signal, not a leak").
   - LEAK-37: an input the actor knows at the prediction point is not a leak. LEAK-6: a slight optimism with a known
     cause stays with a note.
   - Mildest remedy: the claim auditor's wording, "+0.01 to +0.08 RMSLE on these types' test rows depending on the model
     (median about +0.03)", and drop "an upper bound". Mirror it in REVIEW.md issue 6 and the leak_checks.md Cases row.

5. The EG/ES "located subset" (precedent checker) is a wording fix, not a forced blank (LEAK-37 Must; LEAK-10's second
   clause by its scope; EV-1).
   - Concede: the note's premise that the damage-set part "cannot be located row by row" is inaccurate. magnitude_type
     marks 241,088 of the 318,813 kept rows as estimated (EG/ES). Correct the sentence.
   - Dispute that the precedents compel blanking:
     - LEAK-10's located-rows clause is about "a value read at a later pull": zillow, melbourne and aeolus are values
       looked up after the outcome.
     - A damage report's time is in the first report, at the prediction point. That the first report saw damage is
       admitted under LEAK-37 (settled with the 2024 LSR match). The task gamer calls the EG/MG distinction "signal at
       the stated prediction point, not an exploit".
     - Blanking these spans would remove a first-report fact. That is the opposite of LEAK-7's "smallest fix that keeps
       a valid signal".
   - The measured worth on those rows is +0.041/+0.009/+0.003 from 2 untuned seeds. That is inside the seed SDs of
     0.016-0.030 and the noise floor the claim auditor measured on small subsets.
   - Mildest remedy: option b of the precedent checker's prompt: keep, and state the EG/ES share and its measured worth
     in the note.
   - If the curator wants the fact settled first (EV-1), the 4-seed rerun decides between b and a. Either way it is a
     definition detail, not a reason against shipping.

6. Types the note does not name are a completeness fix in the note (LEAK-10/LEAK-37 Cases row; P7 writing).
   - Seiche (51 rows), Dust Storm (1,476), Volcanic Ashfall (77, all $0), Hurricane (482) and Tropical Storm (3,837) are
     timed "by damage or a criterion". About 0.7% of rows; the small types are too small to measure.
   - Mildest remedy: name them in the kept-with-note bullet. Seiche's begin is conditioned on damage, so blank its 51
     durations (costless) or note it. Reword "read App. A for every type".
   - Flash Flood (and Flood): three agents read "threat to life or property" as outcome-free (precedent checker,
     practitioner, claim auditor). The column auditor reads one of Flash Flood's four onset examples as damage, but it
     too "lean[s] keep".
   - The measured Flash Flood worth has no consistent sign: -0.011/+0.053/+0.071 by the column auditor, -0.125 to +0.098
     over 15 fits by the claim auditor.
   - So every agent lands on keep. The fix is one clause saying Flood and Flash Flood are timed by threat, judged
     outcome-free and kept, so no later reviewer reopens it.

7. Metric, value and the remaining findings are settled or are text fixes (MET-1/MET-11 Must; TP-3 Must; LEAK-25 as
   amended).
   - RMSLE suits the label and the task:
     - No source metric exists (claim auditor web search; Diaz and Joseph used MSE on log damage).
     - On raw dollars, 0.1% of rows hold 99.94% of the squared deviation.
     - 44% of the positive figures have one significant digit.
     - The practitioner: "As a planner ranking hazards and counties by order of magnitude, I could pick a model by it".
       The Tweedie switch is "a weighing call ... not a Must", and issue 3 settled RMSLE.
     - The stale "the manager" in the metric reason becomes "the planner" (text fix, MET-1).
   - Value (TP-3): the probe's no_spread flag compares untuned families (RF vs linear +0.051). The task gamer's LightGBM
     (2.83) against the probe's linear (3.24) and its own 100-round LightGBM (2.92) shows methods spread, and TP-3 says
     keep. The blind reviewer has R2 0.49 against 0.19 for an event-type mean.
   - The office $0 convention (blind reviewer's first concern) was decided for this dataset under LEAK-25 as amended
     (Andrej, 2026-11-02). The spread and drift are in the notes.
   - The blind reviewer's "undocumented masking" refers to task.md only. The definition documents the EG/ES blank, the
     duration blank and the dropped hazards.
   - Bookkeeping, all text: stale counts (1,072 to 918; 3.5-4.0% to 4.4-4.9%; 40%/37% to 30.1%; others), the
     unassessed-filter reason (re-ground it on 99.1% $0 / 0.5% of dollars), hail under 3/4 inch added to the damage-only
     list, and the record's leftover `No Good Target` marker on a `Yes`.
   - "Independent failures are not conflicts": none of these is a failed Must. Each is a correction of what the notes
     say about data that is right.

**Judgment record (advocate's reading)**

Verdict: ship after text changes.
Validity:
- USE-1 and USE-5 hold (approximate fit, issue 5).
- LEAK-10/LEAK-37 Cases row applied (D13 verified). The kept spans stay with a corrected worth and EG/ES statement; the
  missing types are named; Seiche is blanked or noted.
- LEAK-25 kept as amended.
- SPLIT-10 and SPLIT-13 hold.
- No weight or exposure: MET-14/MET-15/LEAK-41 do not apply.
Value: TP-3, methods spread (keep). RMSLE kept under MET-1/MET-11; reason re-worded to the planner.
Quality: stale counts and the record marker corrected.
For the curator:
- EG/ES option a or b, after the 4-seed rerun if wanted.
- Seiche: blank or note.

Sources: the panel's reports (claim auditor, column auditor, split auditor, domain practitioner, precedent checker,
blind reviewer, task gamer) and the task and leak probes; the rules (principles.md, leak_checks.md, metrics.md,
task_probes.md); the definition (the kept-with-note bullet).

</details>

<details><summary>Critic</summary>

**Critic, opening brief: noaa_storm_events_damage (exposure re-review, full tier, 2026-11-06)**

Position: ship only after changes. Nothing here excludes the dataset. The use case is real (issue 5), the split holds
(split auditor: no problem), and no exposure or weight ships, so MET-14, MET-15, MET-16 and LEAK-41 do not apply. That
leaves four problems. D13's keep-with-a-note rests on a premise the data refutes. Its reading of the event types is
incomplete. The worth it reports is the low end of what was measured. And the metric reason was never redone after the
use case changed. Ranked validity first, Must first.

1. The kept-span note says the damage-set part "cannot be located row by row". It can be located: `magnitude_type` EG/ES
   marks it. (P4; LEAK-10 Must, second clause; LEAK-7 Should; the time-on-risk Cases row: "where the data locates the
   cut row by row, fix it")
   - Problem: the definition keeps `duration_hours` for the five types because "Which of the two set a given span is not
     recorded, so the part the damage set cannot be located row by row" (dataset.py l.158). The same definition already
     uses `magnitude_type` to blank the speeds the preparer estimated from the damage (l.156, 234).
     - In 2024, 94.4% of EG Thunderstorm Wind events had a first report "TSTM WND DMG" with no speed (the definition's
       own LSR match).
     - For such an entry, Sec. 46 ("When damage first occurred or winds 50 knots ... were first reported") can only mean
       the damage.
     - The EG/ES rows are 241,088 of the 318,813 kept rows (75.6%), per the precedent checker. A further 435
       Thunderstorm Wind rows carry a measured speed under 50 kt, so their spans must be damage-timed too (column
       auditor, 92% positive).
   - Effect on the task: most of the kept rows carry a span the outcome sets, and those rows can be located. They are
     not an unlocatable remainder.
   - Evidence:
     - The precedent checker's report, section 2, with its probe. Blanking the duration on the EG/ES rows only changes
       RMSLE on those rows by +0.041, +0.009 and +0.003. This was 2 seeds and untuned, so it is indicative only and
       needs the panel's 4-seed rerun.
     - Precedents that blank located cells: zillow_prize, melbourne_housing_market, frempl (leak_checks.md l.93, 430,
       441).
     - A blank keyed on `magnitude_type`, which is itself a feature, makes no marker. The speed blank was accepted on
       exactly that ground.
   - Remedy (mildest):
     - Blank `duration_hours` on the EG/ES rows of Thunderstorm Wind and High Wind, and on the Thunderstorm Wind rows
       with a measured speed under 50 kt.
     - Keep the note for the measured-gust rows and the flood rows.
     - If the 4-seed rerun shows no gain on the EG/ES rows, keep the column instead, but rewrite the note: drop "cannot
       be located" and give the EG/ES fact and its measured worth.
     - This is the curator's call (option a or b of the precedent checker's prompt).

2. D13 claims to have read App. A for every type. It did not, so some damage-timed spans are neither blanked nor noted.
   (P4; LEAK-10 Must; LEAK-10 / LEAK-37 Cases row of 2026-11-06)
   - Problem: the CC line says "the study of 2026-11-05 read App. A for every type" (l.167). Three auditors found types
     it left out:
     - Seiche (Sec. 41), 51 rows, 57% positive. The begin is "When water levels rose to initiate shoreline flooding,
       resulting in a fatality, injury or damage", so it is conditioned on the outcome (claim auditor row 3; precedent
       checker section 3). Under the row's own reading this is closer to Strong Wind than to the kept branch.
     - Hurricane (482 rows), Tropical Storm (3,837), Volcanic Ashfall (77) and Dust Storm (1,476) are timed by "damage
       or" a criterion. That is the kept branch, but they have no note (precedent checker; column auditor problem 1).
     - Flash Flood, 74,914 rows (8.9%). One of App. A's four onset examples is water that "causes damage to an above
       ground residence or public building". Its worth on Flash Flood test rows is -0.011, +0.053 and +0.071 (column
       auditor, 4 seeds), which is above the five noted types. The claim auditor's blankFF contrast found no consistent
       sign (-0.125 to +0.098 over 15 fits), and the domain practitioner and the claim auditor read Flash Flood as
       threat-timed. That disagreement is the curator's to settle.
   - Effect on the task: the Must rule is applied unevenly across the types of one column, and the Cases row cites a
     reading that is not complete.
   - Remedy (mildest):
     - Blank the 51 Seiche durations, which costs nothing measurable.
     - Add Hurricane, Tropical Storm, Volcanic Ashfall and Dust Storm to the kept-with-note bullet.
     - Rule on Flash Flood (and Flood) explicitly: either keep it with a note giving its worth, or record it as judged
       threat-timed and outcome-free.
     - Reword "read App. A for every type", both in the notes and in the leak_checks.md Cases row.

3. The note understates the kept column's worth and calls it "an upper bound". (P4; the Cases row requires "a note
   giving its worth"; LEAK-6 Must: measure before acting; EV-2)
   - Problem: the note gives +0.012 to +0.021 RMSLE on the five types and calls it "an upper bound on that part".
   - Evidence:
     - Claim auditor, 5 set-ups by 3 years (t3_summary.txt): -0.009 to +0.078, median about +0.034.
     - The deterministic fit from the curator's own run gave +0.027 to +0.040 (out/duration_worth_summary.txt). Only the
       bagged mean of the small model was reported.
     - Task gamer, per-type gain: Thunderstorm Wind +0.025 to +0.057; High Wind +0.019 to +0.057.
     - The study's +0.020 to +0.038 sits in the same range.
   - Effect on the task: the curator weighed the keep against a number that is not a bound. The heart_failure
     counter-case shows that size decides between keeping with a note and dropping (precedent checker 1d), and that same
     counter-case shows the row needs a size condition.
   - I concede that even +0.08 is about 6% of the ~1.3 gain over a constant. The keep need not flip on this point alone,
     but the note must be true.
   - Remedy: write "+0.01 to +0.08 RMSLE on these types' test rows depending on the model (median about +0.03)" and drop
     "an upper bound". Make the same fix in REVIEW issue 6 and in the Cases row.

4. The metric reason names an actor the use case no longer has, and RMSLE was never checked against the planner's
   decision. (P6; MET-1 Must)
   - Problem: the reason reads "The manager ranks counties by orders of magnitude" (l.182). Issue 5 (B, 2026-11-03) made
     the actor a state hazard-mitigation planner. Issue 3 settled RMSLE for the triage framing only, and "metric
     unchanged" in issue 5 was not re-argued.
   - Evidence (domain practitioner, section 5):
     - The planner acts on expected annual loss per county and hazard, which is a sum of dollars.
     - RMSLE is minimised by exp(E[log(1+y)]) - 1. In 2024 the RMSLE-optimal constant is $16 against a mean of $355,555.
     - The $0 entries take 37-47% of the error, and part of that $0 is office convention.
     - On the other side: the label supports order of magnitude and no more (44% of positive figures have one
       significant digit), and RMSLE scores exactly that.
   - Effect on the task: the declared metric may rank models by a quantity the actor does not plan with.
   - Remedy (mildest):
     - Rewrite the reason for the planner.
     - Run the practitioner's probe: mean_tweedie_deviance (p = 1.5, on dollars) against RMSLE on the 3 windows. Keep
       RMSLE if both pick the same model, and say in the reason that this was checked. Switch only if they pick
       different models.
     - Fix the same stale actor in the REVIEW.md header and in the UNASSESSED filter's reason (claim auditor rows 14,
       27; USE-1).

5. The task's population is "events whose office later entered a damage figure", and nothing in task_summary says so.
   (P3; USE-3, reading what the row means; LEAK-25 as amended, settled, not reopened)
   - Problem: rows with a blank `DAMAGE_PROPERTY` are dropped.
     - The blank rate runs from 0% to 98% by office (EAX 98%, ALY 96%), and 22.7% of 2025 source rows are blank (task
       gamer).
     - At the prediction point the planner does not know whether a figure will be entered.
     - Among the non-blank rows, the positive share is 0.19 at offices with under 5% blanks and 0.25 at offices with
       over 70% blanks, so the drop slightly enriches positives.
   - Effect on the task: small, but a reader of task_summary would take the population for all logged events.
   - Remedy: one sentence in task_summary.row or known: "events with a damage entry; offices leave 0-98% blank". No data
     change. The settled LEAK-25 handling stands.

6. Stale and inaccurate text that a reader acts on. (EV; USE-3; LEAK-37 note completeness, Should; records.md)
   - `known` says "3.5-4.0% of test rows" are entered only with damage. Shipped: 4.4-4.9%, of which 95-96% are damaged
     (claim auditor row 19).
   - The type list leaves out Hail under 3/4 inch, which App. A enters only with damage or an accumulation: 504 rows,
     67-89% positive (column auditor problem 3). It also leaves out Dust Devil.
   - `changes` says 1,072 double entries. Shipped: 918.
   - Notes give 40% / 37% zone rows; shipped 30.1%. 8,135 codes; shipped 7,697. 167,629 episodes; shipped 140,270. EG
     254,988; shipped 252,451 (claim auditor rows 20-21).
   - The record carries a `No Good Target / Scientific Discovery` marker on a `Yes` suggestion (row 26).
   - REVIEW issue 6, option A, says "six other damage-timed types" where the list has seven.
   - Remedy: recompute the counts on the shipped rows, or date them "before the issue 2 drop". Update `known`. Remove
     the marker if the curator agrees.

7. Rule and process bookkeeping for a keep under a Must. (principles.md "Exceptions and amendments": a Must has no
   exceptions, a keep is an amendment; house rules on claims)
   - Problem 1, the rule text: the Cases row keeps a partly outcome-set column under LEAK-10 (Must), but LEAK-10's text
     has only two clauses, and LEAK-6's narrowing names neither. The row also sets no size condition, so read literally
     it would have kept heart_failure's `time` (precedent checker 1d, 1g).
   - Problem 2, the release: the study's decision table assigns D13 to Andrej ("by Andrej in his folders, or with his
     release"). REVIEW and the record show Lennart's decision but no release from Andrej (precedent checker 1c).
   - Remedy:
     - Amend LEAK-10 in place with a third clause for spans drawn "by the outcome or an outcome-free criterion". Tie it
       to the second clause's test: blank the located part, and keep the rest only when its worth is small. Name
       heart_failure as the counter-case.
     - Record Andrej's release of D13, or confirm that he gave it.

Not argued, because settled and not reopened by today's change:
- The office $0 convention (LEAK-25 as amended). The blind reviewer and the practitioner raise it again, with no new
  fact.
- `magnitude_type` as a feature. Settled by the LSR match. The task gamer agrees it is a first-report fact.
- Nominal dollars.
- The split and its gap.
- Exposure (county population does not scale).

Sources: the panel's reports (claim auditor, column auditor, split auditor, domain practitioner, precedent checker with
its probe, blind reviewer, task gamer); the definition (l.86-100, 156-158, 167, 182); REVIEW issue 6; the rules
(leak_checks.md: LEAK-6 l.51, LEAK-10 l.78-98, Cases rows l.430, 441, 442; principles.md).

</details>

<details><summary>Advocate rebuttal</summary>

**Advocate, rebuttal: noaa_storm_events_damage (exposure re-review, full tier, 2026-11-06)**

The critic and I agree on the verdict: ship after changes, with nothing that excludes the dataset. We disagree on two
things:
- Which way the EG/ES question should default (point 1).
- Whether the Tweedie probe and the rule amendment hold up shipping (points 4 and 7).

Point by point:

1. EG/ES locates the damage-set spans (LEAK-10 second clause, LEAK-7, the time-on-risk row). Concede in part; dispute
   the default remedy.
   - Conceded: "cannot be located row by row" is false. magnitude_type marks 241,088 of 318,813 kept rows. The note must
     say so and give their measured worth.
   - Disputed: that the located-rows precedents call for blanking here.
     - The rules the critic cites are about values that were never available at the prediction point:
       - LEAK-10's second clause covers "a value read at a later pull" (zillow, melbourne, aeolus).
       - The time-on-risk row covers an amount at risk cut short by the outcome (LEAK-41).
     - The rule written for this column is the later, specific row on spans (leak_checks.md l.442). It reads spans type
       by type.
     - The begin and end times of a damage report are in the first reports at the stated prediction point. LEAK-37
       (Must) already admits "whether damage was seen" there, and the LSR match settled this. The task gamer calls the
       EG/MG fact "signal at the stated prediction point".
     - The EG speed was blanked for a different reason: the preparer estimated that number from the damage, so it is a
       consequence of the target (LEAK-10). A report's clock time is not.
   - Data: the duration is weaker where damage set the span. High Wind EG AUC 0.459 against MG 0.686; Thunderstorm Wind
     EG Spearman 0.159 against MG 0.305 (claim auditor row 5).
   - The only worth measured on the EG/ES rows is +0.041/+0.009/+0.003, from 2 untuned seeds, inside seed SDs of
     0.016-0.030.
   - So under LEAK-7 (keep a valid signal) the default is b: keep, with the corrected note.
   - I accept the critic's tie-breaker (EV-1, facts first). If the 4-seed rerun shows a consistent gain on the EG/ES
     rows, take a, which is a definition fix. Either outcome ships.
   - The 435 measured-under-50-kt rows go with whatever is decided for EG/ES.

2. Types left out of the App. A reading. Concede.
   - Seiche (51 rows): blank it, which is costless.
   - Hurricane, Tropical Storm, Volcanic Ashfall and Dust Storm: add them to the note.
   - Reword "read App. A for every type" in the notes and in the Cases row.
   - Flash Flood and Flood: I agree it needs an explicit ruling. My reading is recorded as threat-timed and
     outcome-free, kept with a clause:
     - App. A's begin is "an immediate threat to life or property", and the damage case is one of four onset examples.
     - The end is threat-based.
     - The worth has no consistent sign over 15 fits (-0.125 to +0.098).
     - Every agent, the column auditor included, leans keep.
   - Whichever way the curator rules (with a note, or recorded outcome-free), the column stays.

3. Understated worth. Concede in full, with the critic's wording ("+0.01 to +0.08 ... median about +0.03", drop "an
   upper bound") in the note, REVIEW issue 6 and the Cases row.
   - The critic also concedes that +0.08 is about 6% of the gain over a constant and that the keep need not flip.
   - On heart_failure: its `time` alone scored ROC AUC 0.84 and moved LightGBM from 0.75 to 0.90. That is a dominant
     worth, not comparable with a few percent. The size test is met here at any of the measured numbers.

4. Metric reason names the old actor. Concede the rewrite; dispute that the probe gates shipping.
   - Conceded: "The manager" becomes "the planner" in the reason, the REVIEW.md header and the UNASSESSED filter's
     reason (MET-1, USE-1).
   - Disputed: that MET-1 is in doubt.
     - The practitioner, playing the planner, says "I could pick a model by it" and calls the Tweedie switch "a weighing
       call ... not a Must".
     - The label supports order of magnitude only: 44% of positive figures have one significant digit, and offices enter
       round values.
     - On dollars, 0.1% of rows hold 99.94% of the squared deviation.
     - No source metric exists (MET-11).
     - The $16-against-$355,555 gap is the geometric mean against the arithmetic one. It is a reason to say in the
       reason that RMSLE scores order of magnitude, not summed dollars, and the practitioner asks for exactly that
       sentence.
   - Running the Tweedie probe and recording the result is cheap and I support it. But a disagreement between the two
     metrics would be a weighing call under the "source's metric against a better metric" tension. It is not a failed
     Must, so it does not hold the dataset.

5. Population is the events with a damage entry. Concede the sentence, with no data change.
   - The notes already give the blank share (18.32% of 1,225,290, claim auditor row 22), and the drop is the settled
     LEAK-25 handling.
   - One line in task_summary ("events with a damage entry; offices leave 0-98% blank") makes it visible to a reader
     (USE-3).

6. Stale text. Concede every item:
   - `known`: 4.4-4.9%.
   - Hail under 3/4 inch and Dust Devil added to the damage-only list.
   - 918 double entries.
   - 30.1% / 7,697 / 140,270 / 252,451.
   - The record marker removed (curator's call).
   - "six" becomes "seven".
   - All are EV/USE-3 text fixes. None touches the data.

7. Rule and process bookkeeping. Concede that both should be done; dispute that either is a defect of the dataset.
   - The LEAK-10 third clause:
     - principles.md does say a keep under a Must is an amendment, so writing the Cases row into LEAK-10's text with a
       size condition is right.
     - That is maintenance of the rules. The dataset meets the rule either way: the spans are first-report facts
       (LEAK-37), and the worth is small and measured.
   - Andrej's release of D13: a process confirmation. Record it before merge.
   - Neither changes the definition.

Net:
- Conceded: points 2, 3, 5 and 6 in full; the text and process parts of 1, 4 and 7.
- Disputed: blanking EG/ES as the default (LEAK-37 and the span row over the later-pull clause; the data shows no damage
  concentration), and any reading of the Tweedie probe or the rule amendment as a condition for shipping. Both are a
  weighing call or rule maintenance, not a failed Must.
- Open for the curator:
  - EG/ES: a or b, after the 4-seed rerun.
  - Flash Flood: kept with a note, or recorded outcome-free.
  - The result of the Tweedie probe, as a weighing call.

Sources: the critic's brief and the phase A reports; the rules (leak_checks.md l.51-98, 273, 441-442; principles.md).

</details>

<details><summary>Critic rebuttal</summary>

**Critic, rebuttal: noaa_storm_events_damage (exposure re-review, 2026-11-06)**

Summary: I concede most of the advocate's brief. The task is real, the split is right, and most of what remains is text.
One real dispute is left: the advocate's point 5, the EG/ES spans. On that point the like-case rule (Strong Wind) and
the time-on-risk Cases row favour a blank, unless a proper rerun shows the blank buys nothing. I also keep a narrow
version of my metric point. No new points.

Advocate 1, valid task (USE-1, USE-5, P5): conceded. I never argued against shipping. My verdict is "ship only after
changes".

Advocate 2, the split: conceded. The split auditor found nothing new, and I raised nothing on the split.

Advocate 3, D13 applied exactly and costless: conceded for what D13 covers. The blank on Tornado, Strong Wind and Heavy
Rain is verified and is no marker (LEAK-38). This does not answer my points 1 and 2: they are about rows and types that
D13 left untouched.

Advocate 4, the kept spans and their worth: I concede the remedy, which is the same as mine (+0.01 to +0.08, median
about +0.03, and "an upper bound" dropped). I dispute one supporting argument.
- The advocate's argument: the worth is "the wind or flood criterion, not the damage", because within High Wind the
  any-damage AUC is 0.459 for EG and 0.686 for MG.
- Why that does not show it:
  - That AUC measures how well the duration separates damaged from undamaged rows within a group. EG rows are 62.5%
    positive, against 10.8% for MG (task gamer), so the label has little left to separate among EG rows. It says nothing
    about how much the model gains from the span.
  - On the positive amount, the Thunderstorm Wind EG Spearman is still 0.159 (claim auditor row 5).
  - The only direct measure of worth on the EG rows is the precedent checker's: +0.041 / +0.009 / +0.003.
- So the claim "the worth is not the damage" is unproven either way (EV-1: settle the fact with the decisive
  experiment).

Advocate 5, EG/ES is a wording fix, not a blank: disputed. The advocate concedes the note's premise is false. I dispute
the rest, on three grounds.

(a) Scope.
- The advocate says the located-rows rule covers only "a value read at a later pull".
- But the time-on-risk Cases row (leak_checks.md l.441, amended 2026-11-06) applies the same rule to a span cut short by
  the outcome: "where the data locates the cut row by row, fix it". That is not a later pull. It is the same kind of
  fact as here: a span whose end the outcome sets.
- The new spans row (l.442) allows a keep with a note only where a span is "drawn by the outcome or an outcome-free
  criterion". For an EG entry with no reported wind of 50 kt or more, there is no "or" left: Sec. 46's begin and end are
  "When damage first occurred" and "When damage ended".

(b) Like cases (principles.md, "treat like cases alike").
- Strong Wind was blanked because it is entered only with damage, and its span runs from the first damage to the last
  damage.
- The practitioner's reason was: "All I would have is the time of a damage report, not an end."
- An EG Thunderstorm Wind entry is the same fact. 94.4% of the 2024 entries had a first report "TSTM WND DMG" with no
  speed.
- The advocate's "a damage report's time is in the first report" covers the begin only. The end, "when damage ended",
  comes from the preparer merging the damage reports into a swath: the extent of the damage in time, which LEAK-10 calls
  "a consequence of the target".
- LEAK-37 admits that the first report says whether damage was seen. It does not admit how long the damage went on.
- Keeping the EG span while the Strong Wind span is blank treats two identical facts differently, with no fact that sets
  them apart.

(c) Size.
- The advocate says +0.041 / +0.009 / +0.003 sits within the seed SDs of 0.016-0.030.
- +0.041 is above that range.
- And this keep sits under a Must. LEAK-6 (Must) says "a confirmed leak goes even when small". It allows a keep with a
  note only for a slight optimism with a known cause, and the second clause of LEAK-10 allows it only "when the part
  that can be traced shows no gain". The traced part here is the EG/ES rows, and its first measurement shows a gain.
- LEAK-7 does not save the keep. Blanking only the located rows is itself the smallest fix: the measured-gust and flood
  spans keep their signal.

The rule that wins: LEAK-10 (Must), with its located-cells clause and the time-on-risk Cases row, over a keep with a
note, which applies only to the part that cannot be located.

Remedy, unchanged: rerun with 4 seeds on the shipped splits. If the blank of the EG/ES rows (and of the Thunderstorm
Wind rows under 50 kt) shows a gain, blank them (option a). If it shows none, keep the column and correct the note
(option b). I agree with the advocate that this is a definition detail, not a reason against shipping. I do not agree
that option b is the default before the rerun.

Advocate 6, unnamed types and Flash Flood: mostly conceded.
- I accept naming Dust Storm, Volcanic Ashfall, Hurricane and Tropical Storm in the kept bullet.
- I accept the clause recording Flood and Flash Flood as threat-timed, judged outcome-free and kept. Three agents read
  them that way, and the 15-fit contrast has no consistent sign.
- On Seiche I hold the blank as the reading the rule gives: its begin is drawn by "a fatality, injury or damage" alone,
  and only its end is outcome-free. Since it is 51 rows and costless, I accept "blank or note" as the curator's call.

Advocate 7, metric, value, bookkeeping:
- Conceded:
  - TP-3: methods spread, keep.
  - LEAK-25, the office $0 convention: settled, and I did not reopen it.
  - Every item of bookkeeping: they match my point 6.
- Disputed, narrowly: "issue 3 settled RMSLE".
  - Issue 3 settled RMSLE for the triage use case. Issue 5 then changed the actor and decision, and nobody re-argued the
    metric. MET-1 (Must) ties the metric to the use case's decision, so a changed use case reopens the question.
  - The practitioner's own evidence is the fact: the RMSLE-optimal constant is $16 against a mean of $355,555, and the
    planner plans with summed dollars.
  - I do not ask for a switch. I ask for the reason to be rewritten for the planner and for one probe: Tweedie p = 1.5
    against RMSLE, on the 3 windows. If both pick the same model, RMSLE stays, and the reason says it was checked.
  - That is cheap and settles the Must on evidence rather than on wording.

My points the advocate did not answer, which still stand:
- My point 5: one sentence saying the population is the events with a damage entry, with the 0-98% blank rate by office
  (USE-3).
- My point 7:
  - LEAK-10 amended with a clause for the spans keep, including a size condition, with heart_failure as the counter-case
    (principles.md: a keep under a Must is an amendment).
  - Andrej's release of D13 recorded.

Where we stand:
- Agreed: ship after changes, with no exclusion; the worth figure and every text fix; the missing types named; Flood and
  Flash Flood recorded as kept and outcome-free.
- Open for the mediator:
  - EG/ES: blank or note. I hold blank, decided by the 4-seed rerun (LEAK-10, the time-on-risk Cases row, like cases).
  - Seiche: blank or note (curator's call).
  - The Tweedie-against-RMSLE probe under MET-1.

Files: the advocate's brief; the rules (leak_checks.md: LEAK-6 l.51, LEAK-10 l.78-98, Cases rows l.441-442).

</details>
