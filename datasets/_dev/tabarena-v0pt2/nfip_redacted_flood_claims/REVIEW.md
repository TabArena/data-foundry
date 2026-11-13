# nfip_redacted_flood_claims

**Outcome:** added. The AI recommends shipping it after the panel's changes, which are made: the test windows are re-cut
to the half-years 2022H2, 2023H1 and 2023H2, the building fields a large loss can change are blanked where a later
policy term is located, `rateMethod` is dropped, the training sides leave out the test windows' storms and the claims
opened after a window starts, and a protocol line forbids using the test rows. FEMA's OpenFEMA NFIP Redacted Claims v3:
816,846 flood insurance claims with a loss in 2010-2023 (816,944 in the panel's reports: the 98 claims that no split
uses after the new training filters are dropped), for the NFIP's claims desk that sets a claim's first reserve when it
is opened (FEMA bulletins W-08095, W-10008); target the building and contents dollars paid (15.7% zeros), RMSE
fallback; 46 features; train sides of 743,644 to 803,452 claims, test windows of 52,972, 7,115 and 12,782.

Verdict: ship after changes (made).
Validity:
* The OpenFEMA terms allow the use ("decisions on program management"); advance payments and inspection triage stay
  outside the use case.
* The use case is real and now sourced by FEMA's reserving bulletins, with an approximate fit; the target is building
  plus contents, zeros kept.
* Values from a later policy term, three ways. Changed: the test windows were calendar years 2021-2023 and are now the
  half-years 2022H2, 2023H1 and 2023H2, because 71.8% of the old 2021 window carried a policy term from after the loss;
  the located late cells (5,218 rebuilt buildings, 24,358 policies started after the loss, Risk Rating 2.0 codes on
  264,880 earlier losses) are blanked; the unlocated residue in the 14 fields a large loss changes is issue 1.
* Labels still moving: the cut at 2024 holds (no second download to measure them, revisit 2027). The temporal regime
  holds.
* The California Atmospheric River spans the 2023 start, and claims opened after a window start must not train it.
  Changed: each train side now leaves out the test window's storms and the claims opened after its start (431, 2,502
  and 710 training rows dropped for 2022H2, 2023H1 and 2023H2).
* An evaluation leak (an event's final size counted over the test block: +10,396 RMSE on the old Ian window), fixed by
  a protocol line.

Value: a thin real signal. On the re-cut, early-stopped LightGBM beats the training mean on 2023H1 and 2023H2 by 1-4%
and loses on 2022H2 (Hurricane Ian, a county level never seen in training) under either metric (issue 3).

Quality: foundation code 0 set missing ("not collected" before Risk Rating 2.0); impossible elevations and two
coordinates set missing; occupancy codes stay as decoded (settled by the mediator); floors stay unordered; the notes
corrected where the panel refuted them.

Weighed: FEMA's system of record +; a sourced use case +; size +; insurance claims on temporal windows, a gap +; a thin
signal -; one event holds most of each window's error -.

Check: 0 errors, 1 warning (11,107 rows share all features with another and differ in the target: a result of the
blanking; acceptance proposed in issue 1). Leak probe 20 did not run on the final definition: its nearest-neighbour
step stops on the NaN cells that the blanking leaves. It runs after the rebuild with the missing values handled; until
then the leak checks rest on the panel's measurements.

**Main points:** Keep or drop the 14 building fields a large loss may have changed (issue 1; decide it with the
across-datasets late-values item and ny_wcb_assembled_claims_1m issue 1); RMSE or the Poisson deviance (issue 2); the
thin signal is a check to run, not a gate (issue 3).

**Issues for the curator:**

1. **Keep the 14 building fields a large loss may have changed, with a note, or drop them?**

   * **Problem:**
     - The record holds the policy's latest term; where that term is located the 14 fields are blank, but in 2022H2 Ian's claims are 96.8% coded by Risk Rating 2.0 (FEMA's rating scheme of October 2021, which reached existing policies only at renewal) against about 60% that the renewal schedule allows.
     - So some test rows, which no field identifies, may carry elevation or foundation values set after the flood (a building elevated after substantial damage).
     - The traced part shows a tiny positive gain, not none; the coverage, deductibles, zone and community on located rows are kept too, though 4,026 claims were paid above their building coverage (16.3% of located claims reach the cap against 22.5%).
   * **Background:** this dataset is one of those the curator's question on the leak rule's late values touches (kept for
     the review page, to be decided alike with ny_wcb_assembled_claims_1m issue 1): see the across-datasets item on
     unlocated late values, and answer both by the same reading of the clause.
   * **Effect on the task:** the 14 fields (elevation and floodproofing indicators, pre/post-FIRM, the elevation
     certificate, the four elevations, foundation, obstruction, basement type, construction and policy start dates)
     carry most of the thin signal in 2023: without them the 2023H2 model still beats the mean by about 4%, and 2023H1
     falls further below it.
   * **Experiments:**
     - Whole-field worth after the blanking: +738 / +1,018 / +481 RMSE on 2022H2 by seed (critic, 0.31%); with the
       event filters +909 / +487 / -279 (mediator, mixed sign; the second is on the shipped splits); 2023H1 +880 / +906 / +1,501 (1.1-1.9%); 2023H2
       +1,925 (2.6%, one seed).
     - The traced channel (elevated after substantial damage, +35 points difference in differences) reaches only the
       claims with an ICC payment: 0.39% of 2022's test rows; on 2022H2 its 215 rows carry about 0.007% of the
       window's squared error, positive in 3 of 3 seeds; on 2023H1 (5 rows) and 2023H2 (28) about none.
     - So the fields' worth sits on claims without substantial damage, consistent with information known at the loss
       (elevation and foundation are the core of flood rating).
   * **Check warning:** the blanking makes 11,107 rows (1.4%) identical in every feature but different in payout. The
     AI proposes accepting the check's warning; say if you disagree.
   * **Consistency:** distribution_transformers_at_cauca_department dropped untraceable late values with a possible
     gain; medical_facility_operational_data kept them, their worth within noise; tunisian_fraud_detection_challenge
     kept mechanism-free registry codes[^l10]. What could set nfip apart if kept: the traced channel carries about
     0.007% of the window's error.
   * **Panel:** keep, the advocate (the traced mechanism reaches next to nothing); drop, the critic (the clause's
     default for a value that may carry a gain; the whole-field worth exceeds two seed SDs; the burden is on the keep).
     Both concede the call is the case-by-case reading the clause leaves to you.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep with a note (implemented) | the fields stay; the note gives the traced reach and the whole-field worth | the traced channel carries next to nothing; the core of flood rating stays | the traced gain is small but not none |
     | B | Drop the 14 fields | removes them from every row | the clause's default; no doubt left | costs most of the thin 2023 signal (1-2.6%) |
     | C | Drop the elevation indicator and the elevation-certificate block only | removes where the traced mechanism sits | the smallest fix | not measured yet |
     | D | A, and also blank coverage, deductibles, zone and community on located rows | widens the blanking to every policy field of a later term | the clause's letter on located rows | no traced mechanism; removes the cap, the task's core input, from 270,000 rows |

   * **Recommendation:** A, with the note giving both numbers, decided together with the across-datasets late-values
     question; C if you read "shows none" strictly but want to keep the foundation and dates; not D. **Decision:** A, B, C or D?

   **Notes for the AI:**
   - The note under "Later policy term" in `curation_comments` names the unlocated part; on A add the two numbers
     (traced reach 0.007% of 2022H2's error; whole-field worth 1-2.6%). On B drop `LATE_FIELDS` in `_clean`; on C drop
     `elevatedBuildingIndicator`, `elevationCertificateIndicator` and the four elevations, and measure field by field
     after the rebuild. Re-run dataset check and the task probe.
   - On D blank `totalBuildingInsuranceCoverage`, the contents coverage, both deductibles, `ratedFloodZone` and
     `nfipRatedCommunityNumber` on the located rows too.
   - The check warns that 11,107 rows (1.4%) share all features and differ in the target, a result of the blanking
     (claims of one event and place whose differences sit in the adjuster's report). Proposed for acceptance under
     `accepted_check_warnings` with that reason, on your mark.
   - Re-run leak probe 20 with NaN imputed before the nearest-neighbour step.

   [^l10]: **LEAK-10** (Must), clause 2: late values that cannot be located row by row "go when they may carry a gain
     ... and stay with a note only when the part that can be traced shows none"; a case-by-case call of the curator.
     **LEAK-11** (Should): a late value that only weakens the signal may stay. **LEAK-7**: the smallest fix first.

2. **RMSE, or the Poisson deviance on the dollars?**

   * **Problem:**
     - Both metrics are minimised by the mean, so both score the summed reserve an event needs.
     - Under RMSE, condominium associations hold 83.7% of the Ian window's squared error, and the top 0.1% of claims 44.6% of it (14.9% under the Poisson deviance).
     - The source has no metric, so RMSE is the documented fallback; the deviance would come from context.
   * **Effect on the task:** RMSE ranks methods by a few hundred large association claims; the deviance weighs each
     dollar of reserve more evenly.
   * **Experiments:** on the re-cut (table in issue 3) neither metric separates the methods better: the model beats
     the mean on the same two windows of three under either. Tweedie at power 1.5 (noaa's choice) was rejected by both
     sides.
   * **Consistency:** noaa_storm_events_damage moved from RMSLE to a deviance from context on 2026-11-08; it never
     chose a deviance over RMSE, so it does not bind here. RMSE is 35 of the 88 regression tasks, and no insurance
     claim-amount task uses it[^met].
   * **Panel:** for RMSE the precedent checker and the advocate (the fallback; the coverage cap sets the case apart
     from noaa over all rows: top 0.1% hold 38.4% against noaa's 99.94%); for the deviance the critic and the domain
     practitioner (one dollar of error is one dollar of reserve; diversity; the cap fact fails on 2022H2, the window
     that decides).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | RMSE (implemented) | the regression fallback on the dollars | the source names no metric; simple; the cap limits the tail over all rows | a few association claims rank the methods on Ian; the most common metric already |
     | B | Mean Poisson deviance | a metric from context with a stated floor | scores each dollar of reserve; adds a deviance to the insurance tasks | a choice from context where the context is not explicit |

   * **Recommendation:** B, for the dollar-of-reserve reading and the diversity; A is fully defensible and the mediator
     left it open. The tuned check (issue 3) may change this. **Decision:** A or B?

   **Notes for the AI:** on B, `Metric` from context `mean_poisson_deviance` with `min_prediction` (MET-13; a floor
   such as $1, below every positive training mean), the reason naming W-10008's summed reserve; re-run dataset check
   and the task probe. On either answer the tuned check of issue 3 runs under both metrics.

   [^met]: **MET-11** (Must): a metric from context only when the context is clear; else the fallback. **MET-10**
     (Weigh): diversity of metrics across the benchmark. **MET-1** (Must): the metric scores the decision of the use
     case.

3. **Is the signal enough, given that the model loses to the mean on the Ian window?**

   * **Problem:**
     - On the re-cut windows a regularised model beats the training mean by 1-4% on 2023H1 and 2023H2 and loses on 2022H2.
     - The loss has a cause in the data: Hurricane Ian's south-west Florida claims sit at a county level that training never saw.
     - The untuned 400-tree model is fragile on 2023H1 (-1.4% to -1.6% by seed with the blanking).
   * **Effect on the task:** a thin task, where methods may not separate; the windows are dominated by one event each
     (Ian 98.5% of 2022H2's squared error of the mean, the April Florida flooding 62% of 2023H1's, Idalia 51% of
     2023H2's).
   * **Experiments:** mediator, early-stopped LightGBM with an inner validation year, one seed (positive = better than
     the training mean):

     | Window | Mean RMSE | Squared-error fit | Poisson fit (RMSE) | Poisson fit (deviance) |
     |---|---|---|---|---|
     | 2022H2 | 233,754 | -1.6% | -0.8% | -12.4% |
     | 2023H1 | 77,725 | +1.0% | +1.3% | +3.6% |
     | 2023H2 | 73,771 | +1.3% | +1.4% | +4.0% |

     The task probe on the final definition (untuned families, sampled) flags nothing: LightGBM skill +0.176 (SE
     0.064) over the training mean, ahead on 3 of 3 windows by RMSE on its samples, which are not the full windows (the full-window fits above
     lose on 2022H2); linear -0.037.
   * **Consistency:** noaa_storm_events_damage lost to the mean untuned, won tuned per window, and shipped with the
     numbers in its notes; forest_fires kept its split although the signal is small[^tp].
   * **Panel:** the mediator, advocate and critic agree this is a check to run, not a reason to refuse; the critic
     asks that a loss on two windows of three after tuning come back as a new issue.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Ship and run the tuned check (implemented) | keeps the task; the tuned results go into the notes | follows noaa_storm_events_damage; the loss on Ian has a cause in the data | the signal may stay thin |
     | B | Hold until the tuned check runs | waits for TabArena's tuned methods on the re-cut | decides on tuned numbers | delays a dataset whose validity is settled |
     | C | Leave it out | the record gets `No` | no thin task in the benchmark | a real, sourced task lost for a difficulty, not a defect |

   * **Recommendation:** A, with the tuned check as a TODO; a loss on two windows of three after tuning comes back to
     you. **Decision:** A, B or C?

   **Notes for the AI:** the tuned check: early-stopped, tuned fits per window under both candidate metrics (as
   noaa_storm_events_damage issue 10), numbers into the notes and into issue 2; re-run leak probe 20 then too.

   [^tp]: **TP-1** (Must): an untuned flag is a question, checked against tuned methods before acting. **TP-2**
     (Should): retire only for a concrete reason found in the task. Tension row "the right split against the score"
     (P4 over P6, forest_fires).

**Review panel:** ship after changes (mediator). Full panel on the builder's draft (calendar-year windows 2021-2023,
the later policy term kept with a note, `rateMethod` kept). The claim auditor, the column auditor and the split auditor
found the later term far larger than the note said (71.8% of the 2021 window located), a storm spanning the 2023 start
and several refuted numbers; the domain practitioner found the use case in FEMA's reserving bulletins; the blind
reviewer would include it with changes; the task gamer found one exploit (an event's final size over the test block,
4.7% on Ian). The advocate and the critic agreed on the re-cut, the blanking, the filters and the protocol line;
disputed: keeping the 14 fields (issue 1), the metric (issue 2), blanking on training rows (settled by
the mediator: blank on training rows too, the stronger leak rule over the weaker), occupancy harmonising (settled: keep the codes).

<details><summary>Mediator</summary>

```text
MEDIATOR REPORT: nfip_redacted_flood_claims (2026-11-09)
Read: principles.md (df-large), the mediator brief, PANEL_COMMON.md, builder_report.md, the seven evidence reports,
both briefs with rebuttals, the definition's notes, LEAK-9/10/11, TP-1/2/3, MET-10/11, CLEAN-12, noaa REVIEW.md.
Two experiments of my own (scripts and output in the scratchpad named at the end; thread caps 4).

=====================================================================================================================
1. RECOMMENDATION (judgment record)
=====================================================================================================================
Verdict: ship after changes.
Validity: SEL-1 holds (OpenFEMA program-management clause). USE-1 holds, fit approximate, now sourced (FEMA W-08095,
  W-10008). USE-5 holds (building + contents, zeros kept). LEAK-10 triggered three ways: later-term policy block on
  the 2021 window, fixed by re-cutting the test windows to 2022H2 / 2023H1 / 2023H2 (SPLIT-14 met, train sides 91-98%);
  located late cells (rebuilt buildings, NB after the loss, RR2.0 codes on pre-Oct-2021 losses), fixed by blanking;
  the unlocated residue in the fields a large loss changes, curator issue 1. LEAK-24 holds (cut at 2024). SPLIT-6
  holds. SPLIT-9 triggered (one storm spans the 2023 start), fixed by filtering. SPLIT-10 holds (no gap, an
  application) once training claims opened after a window start are dropped. LEAK-9 triggered (event size read from
  the test block), fixed by a protocol line.
Value: TP-2, a thin real signal on the re-cut (wins on 2023H2 under every fit; 2023H1 near the constant; 2022H2 lost
  to Ian's unprecedented county level). TP-1/TP-3 open until the tuned check runs on the rebuilt windows: a TODO,
  not a gate and not a reason for No (P4 over P6 tension row).
Quality: CLEAN-10 (foundation code 0 -> missing), CLEAN-11 (impossible elevations, coordinates), CLEAN-12 kept
  (occupancy codes stay as decoded), wording.
Weighed: source +, sourced use case +, size +, gap (insurance claims, temporal) +; signal -, one event per window -.
For the curator: issue 1, the 14 fields a large loss changes (LEAK-10 clause 2, a case-by-case call);
  issue 2, the metric (MET-11/MET-10, a weighing).

=====================================================================================================================
2. CHANGES TO MAKE NOW (no decision needed)
=====================================================================================================================
a. Re-cut the test windows to 2022H2 / 2023H1 / 2023H2 by date of loss (LEAK-10 Must, clause 2; remedy ladder step 2;
   SPLIT-14). Not an amendment: a fix in the definition exists, so the yearly-window fallback with an amended clause
   is not the mildest remedy and is out (principles step 5; a Must has no exceptions). Add the 2027 revisit (yearly
   2022 / 2023 / 2024 once 2024 settles) to splits_comment.
b. Blank, on located rows (rateMethod RE with a loss before 2021-10-01, originalNBDate after the loss, or
   originalConstructionDate after the loss), the 14 fields a large loss changes: elevatedBuildingIndicator,
   postFIRMConstructionIndicator, preFirmIndicator, elevationCertificateIndicator, baseFloodElevation,
   lowestFloorElevation, lowestAdjacentGrade, elevationDifference, foundationType, obstructionType,
   basementEnclosureCrawlspaceType, floodproofedIndicator, originalConstructionDate, originalNBDate (LEAK-10 Must,
   "located late cells are blanked"; zillow_prize, melbourne_housing_market). This covers the 5,218 rebuilt buildings
   and the 24,358 policies started after the loss. The note says the blank marks these rows. Measured cost: +577 /
   -19 / -65 RMSE on 2022H2, within seed noise (critic). See settled point S1 on why this holds on training rows.
c. Drop rateMethod (LEAK-10; 99.5% of the re-cut test rows are RE, so it carries only the scheme marker; costs
   nothing measurable: domain practitioner, critic).
d. In the splits, drop from each train side the claims of any event (floodEvent or event_code, and the 2022-12-27..31
   California Atmospheric River claims, which carry no code: match by DR-4683's incident period and counties, or by
   name) that has claims in that test window, and the training claims opened on or after the window start (SPLIT-9
   Must; SPLIT-10 Should). 431 / 2,502 / 710 rows on the re-cut windows (advocate).
e. Protocol line (LEAK-9 Should, the stricter wording both sides accepted): no feature or fit uses the test rows at
   all (counts, event sizes, other aggregates). The notes name the count of claims opened so far as a real deployment
   input that the batch protocol leaves out. Same form as medical_facility_operational_data's line.
f. foundationType code 0 -> missing before decoding, its label dropped (CLEAN-10; 99.97% of legacy rows, 0% of RE).
   Mask elevations above the state's highest point, -999.9 and |elevationDifference| > 100 ft; set the two impossible
   coordinates missing (CLEAN-11). Add the numberOfFloors note (CLEAN-14).
g. Texts (writing.md; USE-8, LEAK-26, SPLIT-20, LEAK-24): cite W-08095 / W-10008 and drop "no source names this use";
   SEL-1 note with the program-management clause, advance payments and inspection triage outside the use case;
   rewrite the later-term note with its true scope (the record is the policy's latest term in every window; located
   shares; what was blanked); fit_reason names the redacted inputs (earlier claims, first-notice description);
   "coverage caps most claims" -> 48,250 claims (5.9%) paid exactly a limit hold 21.2% of the dollars; "$250,000 by
   2010" -> $191,200 in 2010, $250,000 first in 2012; name Risk Rating 2.0 as a break inside the history; no second
   download was available for LEAK-24, revisit 2027; 2022 labels still move (3.61% of its dollars last paid in 2026);
   remove "no event spans a window start" and "events with no claim in training"; causeOfDamage reason replaced by the
   measured one (code 0 38.7% zeros, missing 91.4% zeros, worth 541 / 3,045 / 1,838 RMSE); 58.4% not 51%; 4.35%;
   2,276; probe 13 flags 2022Q3; restate the no-gap test in RMSE; one-event shares per window in splits_comment.
h. After the rebuild: dataset check, task probe and leak probe 20 on the new windows, and the tuned check of TP-1/TP-3
   (as noaa_storm_events_damage issue 10: tuned, early-stopped fits per window) under both candidate metrics; the
   numbers go into the notes and into issue 2.

=====================================================================================================================
3. ISSUES FOR THE CURATOR (ranked)
=====================================================================================================================
Issue 1 (P4, LEAK-10 Must, clause 2 on unlocated later-pull values). Keep the 14 fields a large loss changes with a
note, or drop them?
 Problem. After the re-cut and the blanking, the located later terms are gone from the test rows, but the record is
 the policy's latest term in every window. In 2022H2, Ian claims are 96.8% RR2.0-coded against about 60% that the
 renewal schedule allows, so a share of the test rows (not locatable row by row) may carry fields changed by the
 loss itself (elevation after substantial damage).
 Effect. The 14 fields' total worth on 2022H2, after change b: +738 / +1,018 / +481 RMSE (critic, no event filters;
 0.31%, 3 of 3 seeds). With the agreed filters (change d) I measure +909 / +487 / -279 (mixed sign). On 2023H1
 +880 / +906 / +1,501 (1.1-1.9%), on 2023H2 +1,925 (2.6%, one seed). Without them the 2023H2 model is still +4% over
 the constant; 2023H1 falls further below it.
 Keep (advocate): the traced mechanism (elevated after substantial damage, +35 points difference in differences)
   reaches only the ICC-paid rows: 0.39% of 2022's test rows and 0.1% of the constant's SSE. NEW (mediator): the
   fields' worth sits on the other rows. On 2022H2 the 215 ICC test rows carry +1.6e11 to +2.4e11 of SSE gain per
   seed (positive 3 of 3, about 0.007% of the window's SSE; 1-2% of the gain where the gain is positive); on 2023H1
   (5 ICC rows) and 2023H2 (28; 0.4% of the gain) about none. So the traced channel carries next to nothing; the bulk
   of the worth is on claims without substantial damage, consistent with at-loss information (elevation, foundation,
   flood-zone building facts are the core of flood rating).
 Drop (critic): the clause's default for unlocated values that "may carry a gain" is to drop
   (distribution_transformers_at_cauca_department); the traced part shows a small positive gain, not none (claim
   auditor +0.038 vs +0.021 R^2 on located 2021 rows; ICC rows positive in every seed); the whole-field worth exceeds
   two seed SDs on the critic's run, so medical_facility_operational_data's upper-bound route is not open; burden on
   the keep (ny_wcb mediator).
 Rule. LEAK-10 clause 2: unlocated values "go when they may carry a gain ... and stay with a note only when the part
 that can be traced shows none". Whether a positive but tiny traced gain counts as "none" is the case-by-case reading
 the clause leaves to you. Both sides concede that.
 Options: (a) keep with a note giving both numbers (traced reach and the whole-field worth by ICC split); (b) drop
 the 14 fields (costs 1-2.6% in the 2023 windows, most of the thin signal there); (c) drop only
 elevatedBuildingIndicator and the elevation-certificate block, where the traced mechanism is (LEAK-7, smallest fix;
 not measured).
 What would settle it: a test of the unlocated part itself is not available (no policy-term file). (c) can be measured
 field by field after the rebuild.
 Scope note: the clause's letter also covers coverage, deductibles, zone and community on located rows; change b
 keeps them, on the tunisian_fraud_detection_challenge line (no traced mechanism). The coverage hint (4,026 claims paid
 above the building limit; 16.3% vs 22.5% reaching the cap) goes into the note. Say if you want them blanked too.

Issue 2 (P6, MET-11 Must / MET-10 Weigh). rmse, or mean_poisson_deviance from context (min_prediction by MET-13)?
 Problem. Both are minimised by the mean, so both score the summed reserve. Under RMSE, condominium associations hold
 83.7% of the Ian window's squared error and Ian 98.5% of 2022H2's; the top 0.1% hold 14.9% under the Poisson
 deviance against 44.6% under RMSE. Tweedie at power 1.5 (noaa's choice) is rejected by both sides.
 Resolution on the re-cut, NEW (mediator, early-stopped LightGBM, inner validation = last 12 months of the train side,
 change b applied and change d filters; one seed):
   window   constant RMSE / Pdev   L2 fit RMSE        Poisson fit RMSE    Poisson fit Pdev
   2022H2   233,754 / 227,868      237,579 (-1.6%)    235,694 (-0.8%)     256,188 (-12.4%)
   2023H1    77,725 /  80,870       76,924 (+1.0%)     76,747 (+1.3%)      77,934 (+3.6%)
   2023H2    73,771 /  73,671       72,795 (+1.3%)     72,743 (+1.4%)      70,711 (+4.0%)
   (Positive = better than the constant.) Regularised fits beat the constant on 2 of 3 windows under either metric;
   the untuned Poisson loss on 2023H1 was overfitting. The 2023 inner validation year holds Ian, so early stopping
   chose 7 trees there: a weak proxy, not TabArena's tuned methods. So neither metric resolves better; MET-10's
   resolution factor is neutral.
 For rmse (precedent checker's a; advocate's default): the source has no metric; the coverage cap sets the case apart
   from noaa over all rows (top 0.1% hold 38.4% against noaa's 99.94%); rmse is the documented fallback.
 For the Poisson deviance (critic, domain practitioner): MET-1 (one dollar of error is one dollar of reserve, not
   squared on a few hundred association claims); MET-10 diversity (rmse is 35 of 88 regression tasks; no insurance
   claim-amount task uses it); noaa's decisive reason (summed dollars) holds here, and the cap fact fails in the
   window that decides (2022H2).
 Rule. MET-11 allows context "only when the context is clear"; MET-10 is a Weigh rule. The weighing is yours.
 Consistency prompt: the precedent checker's PROMPT A, with option b changed from Tweedie 1.5 to the Poisson
 deviance (noaa chose a deviance over RMSLE, never over RMSE, so it does not bind here).
 What would settle it: the tuned check of change h under both metrics; if both still split 2-1, the call stays a
 weighing of MET-1 and diversity against the fallback.

=====================================================================================================================
4. DISPUTED POINTS SETTLED BY THE RULES
=====================================================================================================================
S1. Blanking the located cells on training rows (the briefs crossed: the advocate withdrew it in rebuttal under
  LEAK-11, the critic conceded it). Blank (change b). LEAK-10's clause is a Must and does not limit itself to test
  rows; LEAK-11 (Should; narrows LEAK-10) wins only at equal strength (principles: Must over Should within a part),
  and its scope is a value that only weakens the signal. The located cells carry a traced gain channel (elevated after
  substantial damage, +35 points; rebuilt buildings $81k vs $18k median), not only a weakening. The task gamer's
  -771 / -777 / -66 concerns the explicit scheme markers, not these fields. Cost within noise.
S2. The thin signal (asked question 1). Not a gate and not a reason for No: a TODO (change h).
  - TP-1 (Must): an untuned flag is a question, checked against tuned methods before acting.
  - TP-2 (Should): retire only for a concrete reason found in the task. The 2022H2 loss has a cause in the data
    (Ian's SW Florida county level, never seen in training: blind reviewer), the task's difficulty, not a defect.
  - Tension row "the right split against the score" (P4 over P6, forest_fires): the split stays even if the signal
    is small. The re-cut is forced by a P4 Must, so the cost to P6 cannot undo it.
  - Fact for the notes: on the re-cut the signal is 2 of 3 windows at +1-4% (regularised) and fragile on 2023H1 (my
    untuned 400-tree L2 with change b: -1.4% / -1.6% / -0.3% by seed, against +0.9-2.6% without the blank: advocate).
  - noaa_storm_events_damage is the like case: untuned lost, tuned per window won, shipped with the numbers in the
    notes. If the tuned check later loses on 2 of 3 windows, that is a new issue for you, not a verdict by default.
S3. Occupancy harmonising (asked question 3): kept as decoded, no definition change. CLEAN-12 (Should) decodes a
  nominal code into its own words losslessly; the harmonising map merges condominium-association buildings into 5+
  units and single units in multi-unit buildings into single-family, on the 96.6-99.5% of test rows that carry RR2.0
  codes. Under the re-cut the scheme bit cannot reach a test outcome, and it stays readable at AUC 0.9987 without
  these fields (column auditor), so harmonising is no leak fix. The evidence for it is a model gain (critic's A2 - A:
  -1,129 / -770 / +2, about 2 SE; task gamer H1a +32 / +854 / -230), and types are not chosen by per-dataset model
  runs (your standing rule on dtypes from context). A model may merge the codes itself. The advocate conceded it as
  optional. A departure would be a P7 exception you record.
S4. The yearly-window fallback with an amended clause: out (ladder; see change a). It stays the alternative only if
  you choose to amend LEAK-10 clause 2 on purpose, together with ny_wcb_assembled_claims issue 1.

=====================================================================================================================
5. TASK GAMER'S EXPLOITS, MAPPED
=====================================================================================================================
1. Final event size counted over all rows: LEAK-9 (Should, evaluation leak). NEW: the definition has no
   "Potential leak, kept on purpose" note or protocol line for it. Gain +25 / +10,396 / +673 RMSE on the old
   windows (4.7% on Ian). Fix: change e. Not measured on the re-cut; 2022H2 holds Ian, so expect a similar gain.
2. Training claims opened on or after the window start: SPLIT-10 (Should) / SPLIT-9. NEW (the no-gap note does not
   cover openings). Gain +270 / +358 / +47, within noise. Fix: change d.
3. Post-loss policy markers (flaw A): LEAK-10 clause 2. KNOWN (the later-term "Potential leak, kept on purpose" note),
   but the measured scope differs from the note (71.8% of the 2021 window located against "cannot be located for most
   claims"; NB after the loss 4.8 / 2.7 / 1.3% against 2.7 / 1.3 / 0.6%): an issue, fixed by changes a-c. For a
   cheater it hurts (-771 / -777 / -66), so it is a validity flaw, not an exploit.
Found nothing: row order, copies (property repeats are signal, USE-10/SPLIT-13), formats, single features,
transforms, identifiers.

=====================================================================================================================
6. AGREED FACTS
=====================================================================================================================
- FEMA OpenFEMA v3, 2010-2023 losses, 816,944 claims; target building + contents paid, 15.7% zeros; ICC left out.
- The policy block is the policy's latest term at extraction: RR2.0 codes on 264,880 pre-Oct-2021 rows; 71.8% of the
  2021 test window located; the scheme carries a renewal (survival) bit (14.7% vs 20.7% zeros in a state-date cell).
- Blanking inside the 2021 window does not cure it (+8.2% RMSE; scheme readable at AUC 0.999).
- Re-cut windows 2022H2 / 2023H1 / 2023H2: 52,972 / 7,115 / 12,782 test claims; train sides 91.1 / 97.6 / 98.4%;
  0 RR2.0-located test rows; legacy-coded test rows 3.4 / 0.5 / 0.5%; located (NB or construction after the loss)
  1,381 / 184 / 81.
- One event per window: Ian 98.5% of 2022H2's constant SSE, April Florida flooding 62% of 2023H1, Idalia 51% of
  2023H2. Condominium associations 83.7% of the Ian window's squared error.
- Untuned signal on the re-cut: L2 -1.2 to -2.2% / +0.9 to +2.6% / +5.4 to +8.2% against the constant.
- 5,218 rebuilt buildings ($81k vs $18k median, 3.8% vs 15.8% zeros); 24,358 policies started after the loss.
- The California Atmospheric River spans the 2023 start (356 train, 1,405 test claims; DR-4683).
- event_code and floodEvent are a function of state and date (0 mixed cells): kept.
- causeOfDamage, the 30 adjuster/payment/current-map fields: rightly dropped.
- Release cut at 2024, history from 2010, no gap, no weight, building + contents: all hold.

=====================================================================================================================
7. CONSISTENCY WITH PRECEDENT
=====================================================================================================================
- Re-cut (LEAK-10 clause 2): follows Lennart's line from 2026-10-21 to 2026-11-05 (blank located cells; keep only
  without gain or mechanism) and LEAK-7's "drop the months where the feature misbehaves" (online_shoppers,
  sf_permit_time). ny_wcb_assembled_claims issue 1 (same batch, draft keep) is undecided, so it is no precedent; decide
  it by the same answer (clause as written, no amendment).
- Blanking located cells: zillow_prize, melbourne_housing_market. Keeping rating and occupancy codes with a note:
  tunisian_fraud_detection_challenge (mechanism-free registry codes kept, CTR_CESSAT dropped).
- Issue 1: between distribution_transformers (dropped, gain) and medical_facility (kept, worth within noise). The fact
  that could set nfip apart, if you keep: the traced channel carries about 0.007% of the window's SSE, and the
  fields' worth sits on the rows without substantial damage.
- Metric: departs from noaa only in the metric picked, not its reason; PROMPT A applies (issue 2).
- Release cut (tunisian), history start (chicago_traffic_crashes, noaa), no gap (lt_vehicle_loan_default_prediction),
  coverage as a feature (wisconsin, liberty_mutual), SEL-1 (lucas_topsoil, Zindi terms): consistent.
- LEAK-9 line: medical_facility_operational_data; stricter form (no test rows at all), simpler to check.
- Thin signal: forest_fires and noaa (TP-1, TP-2), consistent.

Mediator scripts and output (scratchpad, not in the repo):
tuned_recut.py, tuned_recut.json,
mit_split.py, mit_split.log (the run was stopped by its time cap after 7 of 9 fits; 2023H2 has one seed).
```

</details>

<details><summary>Claim audit</summary>

```text
CLAIM AUDITOR REPORT: nfip_redacted_flood_claims (2026-11-09)
Folder: datasets/_dev/tabarena-v0pt2/nfip_redacted_flood_claims/ (dataset.py, README.md)
Scripts, logs and cached frames: the run folder  (a1_load.py ... a12_small.py, a9_container.log, a11_model.log/json,
fields_api.json = the DataSetFields dictionary for NfipClaims v3, datasets_api.json = the catalogue entry).
Data: the 208 raw files re-read (2,725,989 rows, ids unique); the definition's row filters replicated with the id kept
(816,944 rows, identical counts: open 2,771, negative 73, clerical 37,328, double entries 1,338); the shipped frame
and splits built through load_definition(...).to_container() for the scorer test and two cross-checks.

VERDICT
Ship after one change and corrected notes. Every dropped field, the target, the filters, the release cut, the event
fields and the download held their test. The later-term policy fields are refuted: the problem is much larger than the
notes say. The README calls it "some claims" (44% of 2015-2019; policy start after the loss for 2.7/1.3/0.6% of
2021/2022/2023). In the data, 71% of the 2021 test window carries Risk Rating 2.0 codes before RR2.0 applied to it. The
policy start falls after the loss for 4.8/2.7/1.3% of the three windows. A later term is measured to carry part of the
outcome (buildings mitigated or rebuilt after a large loss), but that part reaches few test rows. LEAK-10's later-pull
clause asks that located late cells be blanked, and the README's numbers must be corrected.

TABLE (claim | source | test | result | evidence | rule)

Prediction point and dropped fields
- 9/30 dropped fields set in adjustment or payment | curation_comments "Dropped, set after", POST_OPENING | each of the 30
  against the v3 dictionary (DataSetFields API, read 2026-11-09) | HOLDS | the payments, nets, recoveries, payment and
  recovery dates, non-payment reasons and replacementCostBasis ("whether the building claim was settled") are the
  outcome; the property values are "as estimated by an adjuster"; the depths come from water marks; the duration is
  "hours flood water remained"; the zone and community are "where the insured property is currently located" (looked
  up at extraction); floodCharacteristicsIndicator is 0% filled in every year 2010-2023 | LEAK-10
- replacement costs from the same report, 99.9% agreement | curation_comments | fill pattern against the damage
  amounts and the adjuster's ACV; fill on the zero claims | HOLDS | the building replacement cost is filled exactly where
  buildingDamageAmount and buildingPropertyValue are (agreement 1.0000; 6 rows differ); contents agreement 0.9990. RC >=
  ACV on 99.7% of rows. RC > 0 on 36.5% of the claims paid 0 against 96.3% of those paid, and it is filled on 15.5% of
  the "06 Not actual flood" denials: the missingness encodes the outcome. The dictionary says "as reported by the
  insurer" (not "adjuster"), but the column as published belongs to the claim, not to the policy | LEAK-10 (missingness
  that encodes the outcome)
- causeOfDamage dropped as set in adjustment (unmeasured) | curation_comments; builder "Not verified" | the target by
  code, and the code against the non-payment reason | HOLDS, now measured | code 0 "Other causes" has 38.7% zeros against
  8.7-14.3% for the flood codes (4 rainfall, 2 river, 1 tidal), and 20.9% of code-0 claims carry reason 06 "Not actual
  flood" against 1.9% of the others; the 5,831 missing codes are 91.4% zeros. The handling codes B/C/D are almost absent
  (1.9% of 2020, at most 0.1% elsewhere), so they are not why the column goes: the column is the adjuster's call on
  whether it was a flood | LEAK-10
- the fields kept are a claim's at opening | fit_reason "The fields are a claim's at opening"; task_summary.known | see
  the later-term rows below | REFUTED for the policy fields | LEAK-10

Target and filters
- 11-13 target = building + contents paid, missing together, 108,690 coded 0 + 19,777 recorded 0, 15.7% zeros | notes
  | recount | HOLDS | 0 rows with exactly one amount missing (raw, 2010-2023, kept); 108,690 (all with a reason) plus
  19,777; 128,467 zeros = 15.73% | USE-5
- 14 median $18,560, p99 $350,000, max $10.8M (198-unit association, Ian) | notes | recount | HOLDS | 18,559.8 /
  350,000 / 10,841,477 (FL, 2022-09-28, code A, 198 units, coverage $49.5M) |
- 15 17,746 claims with an ICC payment | notes | recount | HOLDS | 17,746 |
- 16 filters 2,771 / 73 / 37,328 (4.0%) / 1,338; 2,279 claims with 98/99 on one coverage and a payment stay | notes |
  recount | HOLDS, wording off | counts identical; 37,328 is 4.35% of the 2010-2023 rows (3.81% of 2010-2026), not 4.0%;
  2,276 such claims after the double entries are dropped | writing
- the dropped "open" claims are not a selection of large claims (implied) | -- | damage and payment dates of the dropped
  rows by year | HOLDS | 0.24-1.7% of a year (2019 1.73%, 2023 1.04%, not rising toward the release end); median
  damage $0, no payment date, no ICC in any year | LEAK-24, LEAK-25
- non-payment reasons other than 98/99 are real outcomes (implied) | -- | the codes in the kept zeros | HOLDS | 20 "No
  demonstrable damage" 149k, 97 "Other" 95k, 01 "below deductible" 76k, 06 "Not actual flood" 71k, 08 "Failure to
  pursue" 8.8k: each is a claim a reserve would cover at opening |
- one record is one claim, not one transaction of several (implied by "claims transaction") | v3 page "details on flood
  insurance claims transactions" | groups of rows sharing every kept input | HOLDS | 11,070 rows in 3,672 groups; only 2
  groups split building-only and contents-only payments across records; 463 groups mix 0 and paid (0.06% of rows) |
  USE-5

Release cut (LEAK-24)
- 18 shares of late-paid dollars: 712 days is the median age of a 2024 loss, 982 days the youngest 2023 loss; 2.9-4.9%
  in 2017-2021 and 17.3% in 2022 beyond 712 days; 1.5-2.7% and 9.0% beyond 982 days | notes, decision table 1 | recomputed
  from mostRecentPaymentDate | HOLDS | 712 and 982 days exactly; beyond 712 days 4.1/4.9/2.9/4.1/4.4% and 17.3% (2022);
  beyond 982 days 2.2/2.7/1.5/2.5/2.5% and 9.0%. 121,354 rows of 2024-2026 left out | LEAK-24
- probe 13 "no single newest quarter out of band" | claims.md 43, builder report | the probe's own output | REFUTED
  (wording) | probes/leak.txt prints 2022Q3 (Ian) at p90 z +7.0 and mean z +5.7; the reading (an upward hurricane
  quarter, not a censoring drop) holds | EV-3
- the two-download test (LEAK-24's decisive experiment) | -- | no earlier download exists in the warehouse; the v2 API
  is retired | UNTESTED | LEAK-24

Later-term policy fields (LEAK-10, kept with a note)
- 32a 44% of 2015-2019 claims carry RR2.0 codes | notes | recount | HOLDS | 43.7%; rateMethod "RE" and the 2-digit
  occupancy codes agree on 99.98% of rows |
- 32b "some claims" carry a later term; located for few rows; the README's numbers 2.7%/1.3%/0.6% (2021/2022/2023) |
  notes "Potential leak, kept on purpose"; fit_reason; draft issue 4 "blanking reaches few test rows (0.6-2.7%)" |
  RR2.0 share by year and month; originalNBDate > dateOfLoss on the shipped frame | REFUTED | the RR2.0 share rises with
  every year: 8.9% (2010), 25.5% (2015), 50.1% (2019), 63.3% (2020), 75.6% (2021), 95.9% (2022). That is the pattern of a
  record pulled from the policy's latest term, not of the term at the loss (inference; FEMA does not document it).
  RR2.0 before 2021-10-01, a located later term: 264,880 rows (32% of the data) and 31,072 of the 43,494 rows of the
  2021 test window (71.4%; 73.9% of its constant-prediction SSE). Losses of Oct 2021-Mar 2022, when RR2.0 covered only
  new business and opt-in renewals: 78.1% RE (3,458 claims). Ian (Sep 2022): 96.8% RE, against roughly 60% the
  renewal schedule allows (inference), so the 2022 window is affected too, row by row unlocatable. Policy start after
  the loss on the shipped frame: 4.81% / 2.72% / 1.33% (2021/2022/2023), not 2.7/1.3/0.6. Foundation code 0 (the code
  the dictionary lacks) is another legacy marker: 91% of 2010 claims, 24% of 2021, 4% of 2022, 0% of 2023 | LEAK-10
  (later-pull clause)
- 32c "a later term carries a little of the outcome" (RE 41% at 0 to 47% over $150k) | notes, decision table 2 | the
  wrong test: a later term leaks through the fields that change because of the loss, not through the RE flag. Test:
  mitigation and rebuild fields by later term x ICC paid (substantial damage) | REFUTED in kind, HOLDS in size | 2015-2019,
  among substantially damaged buildings (ICC paid), elevatedBuildingIndicator is True on 79.4% of later-term records
  against 39.9% of the others; among the rest 27.1% against 22.9% (difference in differences +35 points). Construction
  date after the loss: 5,218 rows (2.0% of 2012, Sandy rebuilds), 68.5% of them with ICC, 3.8% zeros against 15.8%,
  mean $91.5k against $50.8k; later-term & ICC 14.9% against 3.4%. Reach in the test windows is small: ICC rows are
  0.32/0.39/0.17% of the 2021/2022/2023 test rows and 0.4/0.1/0.3% of the constant's SSE; 16/28/6 test rows have a
  construction date after the loss. Model check (2021 window, LightGBM 400 trees, train 2010-2020): the 12
  mitigation-prone fields add R^2 +0.038 on the later-term test rows against +0.021 on the others (squared error), +0.020
  against -0.001 (Tweedie). Consistent with a leak, but circumstantial: RR2.0 records fill more fields (foundation code
  0 drops to 24%), one fit, no SE | LEAK-10, EV-6
- 32d 4,409 claims paid above their coverage | notes | recount | HOLDS | 4,409 (building alone: 4,026). Among 2015-2019
  building payments over $100k, 16.3% of later-term records hit 99% of the stated coverage against 22.5% of the others
  (median coverage $250k against $200k): circumstantial evidence that coverage, the best single feature, is also a
  later term's |

Event fields (LEAK-10)
- 33 floodEvent and event_code known at opening; 13% zeros for named events against 24% | notes; draft issue 6 | Test:
  are the codes assigned per claim (missingness by outcome) or per state and date (the dictionary: "A public bulletin
  will designate the EDN number assignments by state with corresponding dates of loss")? Coded against uncoded claims
  in the same (state, dateOfLoss) cell | HOLDS | every (state, date) cell that holds a coded claim is fully coded:
  613,169 rows, 0 uncoded; the same for floodEvent (631,002 rows, 0 unnamed); each code covers one state. So the code is
  a function of state and date, not of the claim's outcome. The 13% / 24% split is an event effect (13.1% / 23.7% for
  coded / uncoded). Test codes in train: 0 / 0 / 0 (on the shipped splits). "California Atmospheric River" recurs in
  2023 (1,405 test rows) | LEAK-10
- the designation is known when the claim opens | -- | the bulletin dates are not in the data | UNTESTED | the exposure is
  limited to claims opened before their event's bulletin (the date of the code, not its value) |

History (SPLIT-20)
- 17 fill rates and coverage medians, the 2010 start, 1,746,181 claims before 2010, every train side over 1M with them
  | notes | recount | HOLDS, one phrase wrong | building description 8/44/61/78% (2000/09/10/11), basement 14/56%;
  1,746,181; with the full history the train sides hold 2.48-2.58M raw rows. "by 2010 the median building coverage
  has reached the $250,000 limit" is wrong: $191,200 in 2010, $250,000 first in 2012, then $159,500 (2013) and
  $200,000 (2019). A later break inside the kept history, RR2.0 recoding the policy fields, goes unnamed: the training
  side is 9-76% RR2.0-coded by year, the 2022/2023 windows 96-100% | SPLIT-20 (Should), writing

Split
- 38 windows of 19,897 / 55,699 / 43,494 rows, oldest train 697,854 (85%) | splits_comment | to_container | HOLDS |
  exact; train max 2022-12-31 / 2021-12-31 / 2020-12-31 | SPLIT-11, SPLIT-14
- 39 no event spans a window start; late-paid training dollars 2.4/2.7/10.6%; gap test 444/864/314 against 340/933/388
  | splits_comment | event spans; recount; signal.json | HOLDS | the 10 codes that cross a year boundary cross 2011-2013 or
  2015/16 only; 2.4/2.7/10.6%; 443.7/864.3/314.3 against 340.0/932.7/387.9. In 2021 the gap is 23% better, so the
  result is "mixed", not "no cost". 77% of 2022's dollars were last paid after 2023-01-01 (Ian, in the 2023 window's
  training side) | SPLIT-10 (Should), SPLIT-21
- no row is a copy across the split (implied) | probes | probe 5; the key with the date | HOLDS | 0.0% with the dates;
  exact duplicates share the date of loss | LEAK-16

Download and provenance
- 1 2,725,989 records, data refreshed 2026-09-09, issued 2019-06-01 | download_description | catalogue and an API
  count, 2026-11-09 | HOLDS | count 2,725,989; lastDataSetRefresh 2026-09-09T16:23; issued 2019-06-01; asOfDate a single
  value (2026-09-08) |
- 4 the bulk files answer 403 | download_description | HEAD request | HOLDS | 403 (the terms page also answers 403 to curl;
  WebFetch reached it). The $allrecords stream break was not re-run (UNTESTED) | PROV-13
- 5 two records overflow the int16 parquet schema | download_description | the API, both records alone, as JSON and as
  parquet | HOLDS | JSON returns id 6598548 (2011, numberOfUnits 99,999, condo code N, policyCount 1) and the 2023
  record (34,970); the same filter as parquet fails with "HTTP/2 stream 1 was not closed cleanly: PROTOCOL_ERROR"; both
  set missing in the frame | PROV-13
- 25 copies and constants | notes | recount | HOLDS | reportedCity "Currently Unavailable" on 2,725,989 rows; iccCoverage
  $30,000 on 790,995 kept rows and 0 on 4 ($15k/$20k occur only before 2010) |
- 29-31 decoding and cleaning counts | notes | recount | MOSTLY HOLDS | sentinels 2,945 / 1,370 / 167 / 5, construction
  placeholders 4,165, NB < 1968 28, ZIP 130 / 135 / 47: exact. "foundation code 0 (51% of the claims)" is wrong: 58.4%
  of the shipped rows (README table 58.37%), falling by year as above. Elevations of 999-8,885 ft stay; they are real
  (CO, ND, NE, ...) | CLEAN-10, CLEAN-12
- 7 nfip_redacted_claims is No / Duplicate | record | read | HOLDS | CC 2026-11-08 | PROV-4

Terms (SEL-1)
- 6 and the note: the terms forbid re-identification and individual determinations; the use case sets reserves |
  notes | the terms page (WebFetch, last updated 2025-01-22) | HOLDS | "the data cannot be used to make determinations
  that might affect an individual's rights or eligibility for benefits"; "The data can be used to make decisions on
  program management"; "agree not to reidentify nor attempt to reidentify"; the use allowed is "solely for statistical
  research or as a reporting record". A benchmark is statistical research, and a reserve decides neither a payment nor
  eligibility. No objection to ML use, so SEL-1 is not triggered; under EV-4 the terms are a note, never a reason | SEL-1,
  EV-4

Metric (claims 40-41; MET-1 to MET-3, MET-10, MET-11)
- the source defines no metric | metric.reason | v3 page, dictionary, catalogue; the two papers' abstracts | HOLDS | the
  v3 page: "not intended to be an official federal report"; no task or metric. Salas, Saha and Ravela (arXiv
  2212.08660) name only R^2 (0.807; regressors of claims amount, county-level); R^2 ranks models like MSE within a
  fold. The metric reason omits DELUGE (Kawakami et al., arXiv 2607.16050), which the record names: it uses a
  dollar-weighted PR-AUC on 1-km cell-days, another unit, so it does not change the fallback, but the "where we
  looked" list is incomplete | MET-1, MET-11
- computable on every fold | -- | scorer(c) on each fold with the training mean and with 0 | HOLDS | rmse(const)
  75,207.9 / 228,256.9 / 78,745.0, rmse(0) 89,874.6 / 242,578.4 / 90,635.2 (2023/2022/2021); no scoring columns, no
  weight needed (per-claim target; the coverage is a feature) | MET-2, MET-14, MET-15
- target scale: identity, dollars | -- | spec | HOLDS | target_transform identity | MET-3
- the comparison numbers | metric.reason | constants recomputed; LightGBM-L2 refit for 2021 | HOLDS | Tweedie (p 1.5)
  constants 401.4 / 770.4 / 433.3; L2 RMSE 2021 68,044 (reason: 68,023) |
- "coverage caps the payments, so RMSE is less tail-dominated" (what sets this apart from noaa_storm_events_damage) |
  builder issue 3 | squared-deviation share of the largest rows | HOLDS overall, FAILS in 2022 | over all rows the largest
  0.1% hold 38.4% of the squared deviation (noaa: 99.94%). In the 2022 window (Ian) the largest 0.1% hold 44.6% of the
  constant's SSE and the largest 1% 77.2%; the 357 claims over $1M (0.64%, condominium and commercial) hold 72.4%. 2023:
  11.2% / 44.9%; 2021: 18.2% / 48.5%. Resolution: LightGBM-L2 beats the constant by 1.2% / 2.9% / 13.6% against a
  bootstrap SD of the window's RMSE of 1.9% / 4.2% / 2.2% (unpaired; the paired SE was not run) | MET-10 (resolution),
  principles (consistent judgement, case 2)
- the fallback's own logic ("an event's loss is the sum of the reserves, which the mean minimises") is the same as the
  noaa precedent's reason for its Tweedie metric from context ("the planner sums the expected damage of events") |
  -- | read both | a consistency question, not a refutation: both metrics are minimised by the mean; the untuned
  LightGBM-Tweedie that loses to the mean in 2021/2022 is a fact about one model, not about the metric | MET-10, MET-11

Probes, cited (not re-run)
- 22, 42-44 | builder probes | read against probes/*.txt and signal.json | the numbers are as cited (0.714 / 0.735 /
  0.086 / 0.082; all features 0.056; skill +0.160; copies 0.8% / 0.0%), apart from the probe-13 wording above. 23: the
  earlier triage AUCs are cited from the record, not re-run (UNTESTED)

REFUTED AND UNTESTED, RANKED

1. (P4, LEAK-10 Must, later-pull clause) The later-term policy fields are understated, and the evidence offered is the
   wrong test. 71.4% of the 2021 test window (264,880 rows overall) carries RR2.0 codes before RR2.0 applied to it;
   2022 is affected and cannot be located; the README's policy-start numbers are wrong (4.8/2.7/1.3%, not 2.7/1.3/0.6);
   the fit_reason and `known` say the fields are a claim's at opening. A gain-carrying mechanism is measured (elevation
   after substantial damage +35 points; a construction date after the loss on 5,218 rows), but it reaches at most 0.4%
   of a test window's SSE. LEAK-10 says located late cells are blanked, and values that cannot be located stay with a
   note only when the traced part shows no gain; here the traced part shows a small one.
   Changes: a Must departure the builder did not raise as one; draft issue 4's premise ("blanking reaches 0.6-2.7%").
   Mildest remedy: blank the located late cells that carry the outcome: originalConstructionDate after dateOfLoss
   (5,218, a one-line mask next to the 1492 placeholder) and originalNBDate after dateOfLoss (24,358). Rewrite the note
   with the true scope (RR2.0 before Oct 2021: 71% of the 2021 window; the RE trend by year; foundation code 0 as a
   legacy marker; the ICC difference in differences; the reach in SSE). Re-pose issue 4 for the curator: blank the 12
   mitigation-prone fields on the 264,880 located rows, or keep them with the measured gain (+0.038 against +0.021 R^2
   in 2021, circumstantial). Leave fit `approximate`, but state the reason precisely.
2. (P4, LEAK-24, untested) There is no second download, so the release cut rests on the last-payment dates (which
   hold). Revisit with the 2027 re-download (builder issue 1c).
3. (P4, LEAK-10, untested) Event designation timing per claim is not in the data. The value is a function of (state,
   date), so only claims opened before the bulletin are exposed. Keep it, with the note naming this.
4. (P6, MET-10, MET-1) The metric reason's distinguishing fact holds overall but not in the hurricane window: under
   RMSE the 2022 window is decided by about 360 claims over $1M (72% of SSE). DELUGE is missing from "where we looked".
   Under RMSE the model's gain over the constant in 2023/2022 is within one unpaired bootstrap SD.
   Changes: issue 3's argument. Remedy: add these numbers and DELUGE to the reason, and ask the curator the
   consistency question with noaa_storm_events_damage (same aggregate-loss logic, Tweedie from context).
5. (P4/P7, SPLIT-20 Should, writing) "By 2010 the median building coverage has reached $250,000" is false ($191,200 in
   2010). RR2.0 recoding, a break inside the kept history, goes unnamed. Remedy: reword, and name the break.
6. (P7 and writing) Wrong numbers: foundation code 0 "51%" is 58.4%; clerical "4.0%" is 4.35% of 2010-2023; the claims
   with 98/99 on one coverage and a payment number 2,276 after dedup; probe 13 does show one quarter out of band (2022Q3,
   p90 z +7.0, Ian). Remedy: correct the text.
7. (P5, untested) The $allrecords stream break was not re-run, and the triage AUCs are cited, not re-run. No action.
```

</details>

<details><summary>Column audit</summary>

```text
COLUMN AUDIT: nfip_redacted_flood_claims (column auditor, review panel, 2026-11-09)
Definition: datasets/_dev/tabarena-v0pt2/nfip_redacted_flood_claims/dataset.py (47 features + target,
816,944 rows; windows 2023 / 2022 / 2021). Codebook: FEMA's v3 data dictionary (OpenFEMA DataSetFields, the builder's
scratch/fields.txt, 84 fields). Prediction point: the claim is opened, before the adjuster inspects.
Work, scripts and outputs: the run folder  (c1_load.py ... c7_scheme.py, *.txt, c5_gain.csv, dtype/).

VERDICT
Ship after changes, with one curator call. One LEAK-10 problem is larger than the notes say and has no clean fix: the
policy block is the policy's LATEST term, looked up at extraction, not the term in force at the loss. 71.8% of the
2021 test window can be located row by row as a later term, and the rating scheme this block carries (Risk Rating 2.0
or legacy) records whether the policy was renewed after the loss, which follows the outcome. A smaller, sharper
LEAK-10 is the 5,218 buildings rebuilt after the loss: located, cheap to blank. The latest-term block cannot be
separated: a blank of its located cells becomes the same marker, and the scheme can be read from the other fields
at ROC AUC 0.999. Everything else is P7 cleaning. The event fields, days_loss_to_open and the 30 dropped fields check out; causeOfDamage was dropped rightly
and is now measured.

Judgment record
  Validity: LEAK-10 triggered. (1) Policy block = latest term (located for 72% of the 2021 window; scheme marker
    carries the outcome inside a cell). Curator call, no clean fix. (2) Rebuilt buildings: blank them (LEAK-7).
    LEAK-37 holds for days_loss_to_open. The event fields hold LEAK-10's conditional test.
  Quality: CLEAN-10 (foundation code 0 = not collected), CLEAN-11 (elevations of 990 ft in Louisiana, two
    coordinates), wording of the cap (LEAK-26) and of the later term (fit_reason, notes, draft issue 4).
  For the curator: issue 1 (keep the policy block with a corrected note, which needs LEAK-10's second clause amended
    for this case, or drop the 2021 window, or neither).

=====================================================================================================================
A. COLUMN TABLE (column | meaning (dictionary) | known at prediction? | dtype and cleaning | verdict | rule)
"Later term" (LT) means: the value comes from the policy's latest term at extraction (issue 1). It is located for
RR2.0-coded claims with a loss before 2021-10-01 and for claims whose originalNBDate is after the loss.
---------------------------------------------------------------------------------------------------------------------
dateOfLoss | date water first entered the building | yes; the split axis | datetime, 0 missing | fine | USE-6
days_loss_to_open | built: openDate - dateOfLoss, in days | yes. The span runs from the loss to the opening, which
  is the prediction point. openDate is the first opening: FEMA's 2015-16 Sandy claims review reopened claims of about
  19,000 policyholders (from memory, not re-read), yet only 178 Sandy records open after 2015, and only 19 of the
  2,772 openings after more than 365 days have an earlier-opened twin with the same building fingerprint | float; 310 negative spans set missing | fine. Real signal: the zero share
  rises from 12.7% (0 to 7 days) to 64% (over 2 years) | LEAK-37, LEAK-10 third clause
event_code | built: EDN (from June 2020) else "FICO <n>" | yes. Measured as a pure function of state x date of loss:
  0 of 816,944 claims sit in a state-date (or county-date) cell with mixed coding, and a cell never holds more than
  one code. So no claim is coded by its outcome. The 13% vs 24% zero gap lies between cells (catastrophes against
  small floods) | category, 201 | fine | LEAK-10 conditional test (LEAK-38 form): passes
floodEvent | name of the flooding catastrophe | yes. Same test: 0 mixed cells; 17,833 coded claims have no name |
  category, 82; the probe's ordinal_like flag is false (names) | fine | LEAK-10
state | 2-letter state | yes | category, 56 | fine | -
countyCode | 5-digit FIPS county | yes | category, 2,709; strings with leading zeros (all 5 digits); the probe's
  numeric_levels flag answered (a code) | fine | CLEAN-14
censusGeoid | 12-digit census block group | yes (the building does not move) | category, 76,480; all 12 digits; the
  first 5 digits equal the county in 99.92% | fine | CLEAN-14
reportedZipCode | 5-digit ZIP reported by the WYO | yes | category, 18,176; 130 empty set missing, ZIP+4 cut, 47 leading
  zeros restored; 3 "99999" left | fine | CLEAN-14
latitude | latitude rounded to 0.1 | yes | float; 1 impossible value (an NC claim at -36.0, 174.0, New Zealand) |
  cleaning, trivial | CLEAN-11
longitude | longitude rounded to 0.1 | yes | float; also 1 GU claim at 14.6, 121.0 (Manila) | cleaning, trivial |
  CLEAN-11
nfipRatedCommunityNumber | 6-digit NFIP community used to rate the policy | LT | category, 12,561; state prefix
  equals the county's in 99.999%; the probe's quantity_words flag is false (an id) | fine dtype; LT caveat | LEAK-10
ratedFloodZone | FIRM zone used to rate the policy | LT | category, 65 | LT caveat | LEAK-10
rateMethod | rating method; "RE" = Risk Rating 2.0, from 2021-10-01 | NO for RE on a loss before 2021-10-01: the code
  did not exist at the loss. More generally the scheme says whether the policy renewed after the loss (issue 1) |
  category, 21, decoded | LEAK (issue 1) | LEAK-10
occupancyType | use and occupancy; the 2-digit codes are RR2.0's | same as rateMethod: the 2-digit codes coincide
  with RE (339,924 rows; 159 RR2.0 occupancy codes without RE) | category, 14, decoded; the probe's flag is false
  (nominal) | LEAK carrier (issue 1) | LEAK-10
foundationType | foundation type | LT; an RR2.0 field: code 0 on 99.97% of legacy rows and 0% of RE rows | category, 7.
  "Code 0 (not in the data dictionary)" holds 58.4% of the kept rows (the notes say 51%) and means "not collected
  before RR2.0" | cleaning: 0 -> missing (issue 4); carries the scheme marker | CLEAN-10, LEAK-10
crsClassCode | CRS class used to rate the policy: 1 to 10, discount 45% down to 0% in 5-point steps (SFHA) | LT;
  missing for 34% of RE rows vs 76% of legacy rows | float. A number is defensible: the class maps linearly onto the
  discount. The probe's code_name flag is answered | fine dtype; LT caveat | CLEAN-14
totalBuildingInsuranceCoverage | building coverage | LT: 4,026 claims were paid more building than this limit (329 of
  them with a limit of 0) | float | core input; LT caveat | LEAK-10, TP-4
totalContentsInsuranceCoverage | contents coverage | LT: 6,465 claims were paid on contents against a contents limit of
  0 (124 to 258 per test window) | float | core input; LT caveat | LEAK-10
building_deductible_usd | built: the deductible code in dollars (the dictionary's table) | LT. Circumstantial and not
  verified: 6% to 16% of the legacy claims of 2010 to 2013 carry code F ($1,250), a minimum deductible of HFIAA from
  April 2015 (44 CFR 61.5) | float; unmapped values are raw NaN | fine; LT caveat | CLEAN-12
contents_deductible_usd | built, the same | LT | float; 162,690 missing where there is no contents coverage | fine | -
elevationCertificateIndicator | rated with an EC | LT | category, 9, decoded; 73.5% missing (empty = not reported, by
  the dictionary) | fine; LT caveat | -
baseFloodElevation | BFE in ft, from the EC | LT | float; the >=9,000 sentinels are masked. Left: a 990-999 ft
  cluster (448 claims at 990, 237 of them in LA, where LFE is 991 and LAG 990), and 302 BFEs above the highest point
  of LA, FL, MS, DE or RI | cleaning (issue 5) | CLEAN-11
lowestFloorElevation | lowest floor in ft | LT | float; 9990 to 9995 masked; 990 to 992 left (about 200), 185 above the
  state's highest point; 2,378 zeros with BFE > 5 (a fill?) | cleaning (issue 5) | CLEAN-11, CLEAN-10
lowestAdjacentGrade | lowest adjacent grade. The dictionary calls it a difference, yet it tracks LFE (r = 0.966), so it
  is an elevation | LT | float; -999.9 left (1), 990 (137), 95 above the state's highest point; 15,399 zeros (2,178
  with LFE > 20 ft) | cleaning (issue 5) | CLEAN-11, CLEAN-10
elevationDifference | LFE - BFE, whole ft | LT | float; 9999 masked; 87 rows beyond +-100 ft (-1,978 to 987); 9 are
  contradicted by LFE - BFE, the rest come with equally extreme or missing LFE and BFE | cleaning (issue 5) | CLEAN-11
obstructionType | obstruction under an elevated building | LT | category, 19, decoded; the probe's flag is false
  (nominal) | fine | -
basementEnclosureCrawlspaceType | basement type | LT | category, 4 present, decoded | fine | -
locationOfContents | where the contents are | LT | category, 7, decoded. The probe's flags (ordinal_like, open_end)
  are answered: the levels mix a location with a mobile-home type, a second dimension, so unordered | fine | CLEAN-14
numberOfFloorsInTheInsuredBuilding | floors: 1, 2, 3+, split-level, mobile home, townhouse 3+ | LT | category, 6,
  decoded. Rightly unordered (building types beside the cut count), but the notes do not say what it holds (CLEAN-14
  open end) | fine; add a note | CLEAN-14
buildingDescriptionCode | use of the building | LT | category, 18, decoded; code 21 (2 claims) named | fine | CLEAN-12
condominiumCoverageTypeCode | condominium coverage type | LT | category, 5, decoded; the probe's flag is false | fine | -
disasterAssistanceCoverageRequired | agency that required the purchase as a condition of aid | LT. Aid after THIS loss
  would set it on a later term. It is the strongest single separator of the scheme (31% of the gain in c7) |
  category, 6; code 3 (9 claims) undocumented, named | LT caveat | LEAK-10
numberOfUnits | units covered by a condominium master policy | LT | float; >10,000 masked (2 rows); 0 on 8.4% of
  non-condominium rows (not applicable, written as 0 or 1) | fine | -
policyCount | insured units in active status (RCBAP counts many) | LT | int; equals numberOfUnits in 88% (not a copy) |
  fine | CLEAN-5
originalConstructionDate | original construction date | LT, and for 5,218 claims AFTER the loss: buildings rebuilt
  after this flood (issue 2) | datetime; 1492-10-12 and dates before 1700 masked; 47.9% on 1 January (year
  precision) | LEAK on the located rows (issue 2) | LEAK-10, LEAK-7
originalNBDate | original date of the flood policy | LT; 24,358 claims after the loss (3,872 test rows: 2,090 / 1,517 /
  265) = a policy written after the loss; inside a state-date cell they are 0 in 12.9% against 14.9% | datetime;
  dates before 1968 masked | LEAK carrier (issue 1) | LEAK-10
postFIRMConstructionIndicator | construction after the FIRM | LT; 97.7% True on the rebuilt rows | bool, 0 raw nulls.
  Both FIRM flags are False on 387,403 rows (47%; 73.6% of 2010) and both True on 1,320: False also stands for "not
  reported" (question 8) | LT caveat; question | CLEAN-10
preFirmIndicator | construction before the FIRM | LT | bool; see above | question | CLEAN-10
elevatedBuildingIndicator | NFIP elevated building | LT; 92.4% True on the rebuilt rows | bool | LT caveat | LEAK-10
primaryResidenceIndicator, rentalPropertyIndicator, smallBusinessIndicatorBuilding, nonProfitIndicator,
  stateOwnedIndicator, houseWorship, agricultureStructureIndicator, floodproofedIndicator | yes/no flags of the policy
  application | LT | bool, 0 raw nulls, only True/False | fine; LT caveat | CLEAN-14
TARGET amount_paid_building_contents_usd | building + contents paid, untransformed; 0 for a claim closed without
  payment (128,062 zeros carry a non-payment reason, 405 do not); ICC left out (a separate coverage, paid after the
  substantial-damage decision) | n/a | float, 15.7% zeros | fine. One wording fix: the notes say "the coverage caps
  most claims", but 48,250 claims (5.9% of all, 7.0% of the paid ones) are paid exactly a coverage limit, and they
  hold 21.2% of the dollars. Not a lookup: coverage alone R^2 0.063 (builder) | LEAK-26 (document the cap), TP-4

=====================================================================================================================
B. PROBLEMS, ranked by principles.md (P4 first, Must first, then by effect)

1. P4, LEAK-10 (Must), values looked up at extraction. The whole policy block is the policy's latest term, and its
   rating scheme records a later event (the policy renewed after the loss). This is larger than the notes say.
   Evidence:
   - The share of claims carrying RR2.0 codes rises steadily toward the extract: 48% of 2019Q1 losses, 54% of 2020Q1,
     66% / 70% / 78% of 2021Q1-Q3 (before RR2.0 existed on 2021-10-01), then 97-99% from 2022Q3. This is the pattern
     of the latest term joined to the claim. A term-at-loss pattern would be 0% before October 2021. Within a claim,
     the RR2.0 fields (rateMethod RE, 2-digit occupancy, foundation code other than 0) coincide (339,924 of 340,083).
   - Located as a later term (RR2.0 codes on a loss before 2021-10-01, or NB after the loss, or construction after the
     loss): 9% (2010), 28% (2012), 40-50% (2016-2019), 63% (2020) of the training years; in the test windows
     31,213 of 43,494 (71.8%) for 2021, 1,544 (2.8%) for 2022, 271 (1.4%) for 2023.
   - It carries the outcome. In state x date-of-loss cells, where the event code is constant, I compare the claims
     whose policy was renewed (RE) with the others. 2022-04 to 2023: zero share 14.7% vs 20.7%, mean log1p +0.59; in
     these windows a legacy code means the policy was not renewed after the loss (2,116 of 74,461 rows). 2021 before
     RR2.0: 16.7% vs 19.6%. 2016-2020 training: 14.7% vs 16.1%. 2010-2015: 10.6% vs 12.9%. NB after the loss: 12.9%
     vs 14.9%. The builder's unconditional table (41% to 47% RE) shows the same direction.
   - Other policy fields of another term: 6,465 claims were paid on contents against a contents limit of 0, and 4,026
     were paid more building than the limit. Code F ($1,250) on 6-16% of the legacy claims of 2010-2013 is
     circumstantial (the code's start date is not verified).
   - Strength at model level is small, and the scheme cannot be removed. Dropping rateMethod, occupancyType and
     foundationType changes LightGBM's RMSE, paired by seed (0, 1, 2), by +141 / +1,372 / +245 (2023), -824 / +109 /
     +62 (2022) and +69 / +294 / +433 (2021; +0.36% on average, 3 of 3 positive). The shipped model's seed spread is
     70,857-72,706 / 230,462-231,639 / 72,934-73,179. So the three fields are worth a little in 2021 and 2023, which is
     legitimate RR2.0 information or the survival bit; the two cannot be told apart. And the scheme stays readable
     from the other fields: ROC AUC 0.9987 without those three fields, and 0.921 from the
     missingness pattern alone (c7: disasterAssistanceCoverageRequired, basement type and numberOfUnits lead).
   - What the definition says, and must correct:
     - claims.md item 32 and the notes: "2.7%, 1.3% and 0.6% ... a policy start after the loss" and "cannot be located
       for most claims";
     - draft issue 4: "blanking reaches few test rows". It reaches 71.8% of the 2021 window;
     - fit_reason: "some claims carry policy fields of a later policy term".
   Remedies (mildest first). None separates the late values cleanly:
   (a) Keep the block, rewrite the "Potential leak, kept on purpose" bullet as "the policy fields are the policy's
       latest term at extraction", with the located shares per window, the in-cell zero shares and the model-level
       numbers above, and name it in fit_reason. LEAK-10's second clause allows a note only when the traced part shows
       no gain. Here it shows a small one (1.4 to 6 points of zero share in a cell; within noise at model level). So
       this is the curator's call, recorded as an amendment of that clause for a block that is the task's core and
       cannot be separated (a Must has no exceptions).
   (b) Also drop the 2021 window, where the scheme splits the test rows 76/24. 2022 and 2023 show it on 2.8% and 1.4%
       of the rows. This leaves two windows (SPLIT rules, TP-2); the windows could move one year earlier only at a
       worse share (2020: 63% located).
   (c) Blanking the located cells does not fix it. The blank itself becomes the "renewed after the loss" marker (the
       same bit), and on 2021 it costs RMSE +8.2% (72,934 to 78,917, legitimate information lost with it).
   (d) Dropping the policy block guts the task (USE-12 keeps the task).
   My reading: (a), with the curator's explicit decision. Also mention the precedent tunisian_fraud_detection_challenge
   (registry fields looked up at extraction kept with a note, but a status that records a later event of the entity,
   CTR_CESSAT, dropped). Here the status cannot be dropped, because the whole block encodes it.

2. P4, LEAK-10 (Must), a consequence of the target, located. 5,218 claims have originalConstructionDate after the
   loss: buildings rebuilt after this flood.
   Evidence: they are 97.7% post-FIRM and 92.4% elevated (36.3% / 26.1% for the others), paid a median $81,003 against
   $18,305, and 0 in 3.8% against 15.8%. Inside a state-date cell: zero share 3.2% vs 9.9%, log1p +1.65; within 19
   events, +1.49. By year: 2.0% of the 2012 (Sandy) training rows; 16 / 28 / 6 test rows.
   Remedy (LEAK-7, cheap): on rows with originalConstructionDate > dateOfLoss, blank the building fields
   (originalConstructionDate, postFIRM, preFirm, elevated, EC indicator, the four elevations, foundation, obstruction,
   basement). The blank then marks 0.6% of rows, beside 4,392 construction dates missing for other reasons; say so in
   the note. Measured with those fields blanked, paired by seed: 2023 +550 / +113 / -146, 2022 -56 / -1,017 /
   -1,253, 2021 +178 / -190 / +538. Mixed signs, within seed noise: the fix is cheap.

3. P4, LEAK-10, NB after the loss (24,358 claims; 3,872 test rows): the same survival mechanism as issue 1 (12.9% vs
   14.9% zeros in a cell). Blanking the NB date makes the blank the same marker. Handle it inside issue 1's decision:
   keep it with the note, or drop originalNBDate. The policy's tenure is legitimate for a term at the loss.

4. P7, CLEAN-10 (Should). foundationType code 0 means "not collected before RR2.0": 99.97% of legacy rows and 0% of RE
   rows carry it. It is a proxy for missing, not an undocumented code. Fix: set_missing({"foundationType": ["0"]})
   before decoding, and drop "Code 0 (not in the data dictionary)" from CODE_LABELS and the notes. The notes' "51% of
   the claims" is 58.4% of the kept rows. Measured: RMSE -63 / -861 / +196, within noise.

5. P7, CLEAN-11 (Should). Impossible elevations survive the +-9,000 ft mask:
   - a 990-999 ft cluster with relative values (BFE 990 on 448 claims, 237 in LA, with LFE 991 and LAG 990; LFE
     990-992 on about 200; LAG 990 on 137);
   - 302 BFEs, 185 LFEs and 95 LAGs above the highest point of LA (535 ft), FL (345), MS (806), DE (448) or RI (812);
   - LAG -999.9 (1 row);
   - elevationDifference beyond +-100 ft on 87 rows (-1,978 to 987; 9 contradicted by LFE - BFE, the rest beside
     equally extreme or missing elevations).
   Remedy: mask elevations above the state's highest point, -999.9, and |elevationDifference| > 100 ft. Or keep it all with a note (a few hundred cells, 66-68% of each elevation column is missing anyway).
   Question for the curator: LAG = 0 on 15,399 rows (2,178 with LFE > 20 ft) and LFE = 0 with BFE > 5 on 2,378 look
   like fills, not proven.

6. P7, CLEAN-11 (Should). Two impossible coordinates (NC -36.0/174.0; GU 14.6/121.0): set missing.

7. P7, writing / LEAK-26. The target bullet's "the coverage caps most claims" should read: 48,250 claims (5.9%; 7.0%
   of the paid ones) are paid exactly a coverage limit and hold 21.2% of the dollars (9,801 at the $250,000 building
   limit). The cap is a per-row feature (coverage), so documenting it is enough (TP-4: no lookup).

8. P7, CLEAN-10 question. preFirmIndicator and postFIRMConstructionIndicator are False together on 387,403 rows (47%)
   and True together on 1,320. A building is one or the other, so False also stands for "not reported" in one of the
   two flags. Ask the curator: keep with a note, or ship one FIRM-status category (pre / post / unknown / both)?
   Either the flags or their absence carry the regime too (issue 1).

9. P7, CLEAN-14 note. numberOfFloorsInTheInsuredBuilding stays unordered (floors 1, 2, 3+ beside split-level, mobile
   home and townhouse types). The notes should say so, as the open-end clause asks.

=====================================================================================================================
C. CHECKS THAT FOUND NOTHING TO CHANGE (asked in the prompt)

- floodEvent and event_code (builder issue 6) can be closed with evidence. The code is a deterministic function of
  state and date of loss: 0 claims in mixed cells, at most one code per cell. FEMA's bulletin "will designate the EDN
  number assignments by state with corresponding dates of loss" (dictionary), so no claim is coded by its handling or
  outcome. The coded share rises with the payment (62% at 0, 93% above $150,000) only between events. Timing: the
  bulletin may follow an opening on day 0-3, but it is designated by place and date, so a reserving desk knows it.
- days_loss_to_open (LEAK-37) holds: see the table. The span is drawn by the loss (the policyholder's report) and
  the opening (the prediction point). The outcome can draw neither end, and openDate is the first opening.
- The 30 POST_OPENING drops are each set during adjustment or payment, or looked up at extraction:
  - payments, nets, recoveries, the two non-payment reasons and the payment and recovery dates: the outcome;
  - replacementCostBasis: "whether the building claim was settled on a replacement cost basis";
  - damage amounts and property values: "as estimated by an adjuster";
  - buildingReplacementCost and contentsReplacementCost: "as reported by the insurer", and filled exactly where the
    damage amounts are (99.999%): 40.3% of the zero claims against 97.5% of the paid ones, so their fill encodes the
    outcome even if part of the value were the policy's;
  - waterDepth, exteriorWaterDepth, interiorWaterDepth: the adjuster's water marks (filled 17% / 13% for zero claims
    against 46% / 40% for paid ones);
  - floodWaterDuration: the adjuster's;
  - floodCharacteristicsIndicator: empty on every kept row;
  - floodZoneCurrent and nfipCommunityNumberCurrent: "where the insured property is currently located" (filled for
    96.6% of RE rows against 51.5% of legacy rows: an extraction lookup).
- causeOfDamage: the drop is right, and now measured.
  - Who sets it: missing on 4.1% of the zero claims against 0.07% of the paid ones. Code 0 "Other causes" is 0 in
    38.7% of its claims, against 8.7-14.3% for tidal, riverine and rainfall. The handling codes B, C and D (718
    claims) are adjustment choices. So the value is coded with the adjustment's finding: LEAK-10 (missingness and
    codes that track the outcome).
  - Worth: added as a feature, it lowers RMSE by 541 / 3,045 / 1,838 (2023 / 2022 / 2021; 2021 is about 14 seed SDs)
    and the log1p RMSE by 8% to 17% (4.13 to 3.81, 6.24 to 5.28, 4.58 to 3.79). Put this in the notes in place of
    "its worth was not measured".
- Dropped copies and constants: right.
  - iccCoverage is 30,000 or missing, and missing slightly more often for zero claims (6.0% vs 2.7%). Dropping it is
    right on both counts.
  - nfipCommunityName, reportedCity, asOfDate, yearOfLoss, id, openDate, eventDesignationNumber, ficoNumber: right.
  - The deductible codes are replaced losslessly by the dollar columns. The dictionary's table matches DEDUCTIBLE_USD,
    and no code is unmapped (every missing dollar value is a missing code).
- Decoded codes (CLEAN-12): the CODE_LABELS words match the dictionary for the 11 coded fields. The order was checked
  where a scale could exist: none needs an ordinal type (locationOfContents, numberOfFloors and EC mix dimensions;
  crsClassCode is a number).
- ZIP codes, county and block group: strings of 5, 5 and 12 digits with their leading zeros.
- int16 overflow records: numberOfUnits 34,970 and 99,999 are masked (> 10,000); the next largest kept value is 4,000.
- The 11 bool flags have no nulls in the raw API parquet and hold only True and False.

=====================================================================================================================
D. DTYPE PROBE (dtype_probes.py nfip_redacted_flood_claims --no-fetch; 11 of 33 flagged). Each flag answered:
- nfipRatedCommunityNumber (quantity_words): an id, so category is right.
- condominiumCoverageTypeCode, floodEvent, obstructionType, occupancyType (ordinal_like): nominal, unordered is right.
- locationOfContents and numberOfFloorsInTheInsuredBuilding (ordinal_like, open_end): a second dimension, so
  unordered is right; add the note (issue 9).
- crsClassCode (code_name): a discount class, linear, so a number is defensible.
- censusGeoid, countyCode, reportedZipCode (numeric_levels): geographic codes, category is right.
No count is typed categorical and no code numeric. The one coding problem the probe does not see is foundation code 0
(issue 4).

E. METHOD AND LIMITS
- The frame was rebuilt through dataset_io.from_definition(raw=True), joined to the raw rows by lineage, with thread
  caps of 4.
- LightGBM: L2 on dollars, 400 trees, 63 leaves, on the shipped splits. Seeds 0, 1 and 2 for the shipped model, for
  dropping the scheme fields and for blanking the rebuilt rows; one seed for the rest (V1, V3, V5), whose
  differences are read against the seed spread.
- Cell tests: state x date-of-loss cells holding both groups, weighted by the smaller group.
- Not verified: the start date of deductible code F; whether FEMA documents the policy-term join (no statement found
  in the dictionary).
```

</details>

<details><summary>Split audit</summary>

```text
SPLIT AUDITOR - nfip_redacted_flood_claims (folder datasets/_dev/tabarena-v0pt2/nfip_redacted_flood_claims, df-large)
2026-11-09. Read-only. Scripts and outputs: the run folder  (s1_load .. s7_repeat, *.txt, s5_models.json,
s6_history.json). Frame and splits loaded through dataset_io.from_definition(raw=True) (816,944 rows, 47 features);
models are untuned LightGBM (400 rounds, lr 0.05, 63 leaves, 4 threads), the builder's settings, scored by RMSE.

VERDICT: right with notes.
Temporal by dateOfLoss, three calendar-year windows (2023, 2022, 2021), expanding train from 2010, no gap: this
is the right regime for reserving at a claim's opening. It needs one fix and three corrected statements. The
"California Atmospheric River" storm spans the 2023 window start, so the texts saying that no event spans a start, and
that the test years' events have no claim in training, are false. The no-gap call holds, but its measurement should
be restated under the declared metric. One hurricane decides two of the three windows; that is a value note, not a
split error.

Judgment record
  Validity: SPLIT-1/3/6 hold (temporal, one regime); SPLIT-9/13 triggered (event spans the 2023 start), fix = filter
    356 training rows + correct 3 texts; SPLIT-10 holds (no gap, an application, numbers to restate in RMSE);
    LEAK-24 holds (cut at 2024 right; 2022 and 2023 labels still move a few percent, note); SPLIT-11/12/14 hold
    (85.4% / 90.7% / 97.6% train); SPLIT-20 holds (2010 start on a collection break; no _1m).
  Value: one event holds 98% (2022) and 75% (2021) of a window's squared error; rankings flip on it (TP-9 spread,
    metric question to MET-10/11). Not fixable by re-splitting.
  For the curator: finding 1 (filter or keep with a note); finding 5 (keep 3 windows or go to 5).

----------------------------------------------------------------------------------------------------------------------
REGIME (SPLIT-1, SPLIT-3, SPLIT-6, USE-10)  -- holds
- Use case: claims staff set a first reserve at opening and sum an event's expected loss. A refit model meets new
  flood events (cold start for the event) in known places with partly known buildings. A temporal split by date of
  loss makes the test events new and keeps the drift: nominal dollars (mean claim $21k-$94k by year) and Risk Rating
  2.0. A split grouped by event would test new events only and lose the drift, and SPLIT-3 allows one regime.
  Temporal is right.
- Places recur and are features (SPLIT-4): county 99.8% and census block group 86.9% of the test rows were seen in
  train (hidden-groups probe).
- Buildings recur (SPLIT-13). There is no property id, but an exact key (block group, rounded lat/lon, construction
  date, the policy's original date; complete on 98.9% of rows) finds an earlier claim in train for 22.7% / 10.4% /
  26.9% of the test rows (2023 / 2022 / 2021). The log-label correlation with that earlier claim is 0.24 / 0.12 /
  0.31. A reserving desk knows a building's earlier claims, so a known building is part of the task (USE-10). The
  SPLIT-9 channel, an earlier claim of the same building still being paid when the test claim opened, reaches
  0.70% / 0.17% / 0.38% of the test rows (139 / 92 / 166): negligible. The curation note "repeats cannot be found"
  understates this: they can be approximated (a possible feature, not a split matter).

FINDINGS, ranked (principles.md: P4 before P6, Must before Should)

1. [P4, SPLIT-9 (Must) / SPLIT-13] One event spans the 2023 window start; three texts say none does.
   Evidence:
   - "California Atmospheric River" claims are dated 2022-12-27..31 (356, in the 2023 train side) and
     2023-01-01..03-25 (1,405 test claims; 924 in January, 72 in February, 409 in March). The name occurs in no other
     year.
   - FEMA DR-4683-CA, "Severe Winter Storms, Flooding, Landslides, and Mudslides", has an incident period of
     Dec 27, 2022 - Jan 31, 2023 (fema.gov/disaster/4683). So the 996 January-February test claims (5.0% of the
     window) and the 356 training claims are one storm series. The March claims are a later storm.
   - 76.7% of the 1,405 test claims lie in counties of the late-December claims.
   - 93.9% of the 356 training claims were last paid after 2023-01-01: their labels were unknown at every test
     claim's opening.
   - None of these claims has an event code (event_code is NA on all 1,761). So the builder's code-based check
     ("no event code of a test window occurs in its training side") is true but misses the storm.
   Effect (LightGBM-L2 on the 2023 window, with vs without the 356 rows):
   - The mean prediction on the 996 January-February claims is $43,631 with them and $31,536 without; the actual
     mean is $40,287. The event's level transfers.
   - RMSE on those claims is 78,661 with and 78,048 without; the whole window 74,287 with and 74,963 without.
   - Both RMSE changes are within the refit noise (two equal-size subsamples differ by 550 on this window).
   - The 2022 and 2021 starts have no shared event names; the last 14 days before them hold 90 and 198 claims.
   Wrong texts:
   - splits_comment: "no event spans a window start".
   - task_summary.split: "the test years' floods are events with no claim in training".
   - Curation note: "one generic name recurs ('California Atmospheric River', 2023 and earlier years, 1,405 test
     claims of another storm)".
   - claims.md items 33 and 39.
   Mildest remedy: a filter in `_make_splits` dropping the training rows of an event (floodEvent or event_code) that
   has claims in the test window. Here that is the 356 rows of the 2023 train side (0.04%); the floor is unaffected.
   Correct the three texts either way. The alternative, keeping the rows with a corrected note (the effect is within
   noise), reads the event as a code shared by many claims (SPLIT-10). It is weaker: the link is one physical storm
   in the same counties, and its labels were unknown at the test rows' prediction point.

2. [P4, LEAK-24 (Must)] Release cut at 2024 (builder issue 1): right, option (a), revisit (c). Note that 2022 also
   still moves.
   Inside the window:
   - 2023's test labels are 982-1,347 days old at the extract.
   - In older years, claims last paid after 982 days hold 1.5-2.7% of a year's dollars (an upper bound on what is
     still missing).
   - 2.75% of 2023's dollars are in claims last paid in 2026.
   - For a window mean of $49k, a shift of 1-3% is negligible against an RMSE of about 75k.
   2024 would be worse:
   - A 2024 loss is a median 712 days old at the extract.
   - In older years, claims last paid after 712 days hold 2.9-4.9% of a year's dollars, and 18.2% for Ian.
   The 2022 window (Ian) is not settled either:
   - 3.61% of its dollars are in claims last paid in 2026 (2021: 0.50%).
   - Ian's late-payment curve tracks Sandy's: claims last paid after 365 days hold 34.9% of its dollars against
     38.2% for Sandy (Harvey 10.8%).
   - Sandy still had 14.8% of its dollars in claims last paid after 1,347 days (Harvey 0.9%).
   - So the 2022 labels may still grow by a few percent; the notes should say so.
   Open claims dropped by the filter (no amount and no reason), as a share of each year's records:
   - 2023 1.04%, 2022 1.23%, 2021 0.24%.
   - 2019 1.73% and 2020 1.37%; 2010-2018 0.03-0.24%.
   - A mild selection by outcome (open claims are the slow ones), similar across 2019-2023, so not specific to the
     release end. Worth one sentence in the notes.

3. [P4, SPLIT-10 (Should)] No gap: an application, as in lt_vehicle_loan_default_prediction; the measurement should
   be in the declared metric.
   Why no gap is needed:
   - Every claim is in the extract from its opening whatever its outcome, so the newest training rows are not the
     fast ones.
   - The training labels were read 1,347+ days after the loss.
   - What the rule guards against (selection by outcome) is covered by the collection.
   The delay itself is real:
   - Dollar-weighted time to the last payment (2010-2019): median 113 days, 75% at 248, 90% at 793.
   - Training claims last paid after the window start: 1.57% / 1.47% / 4.14% of training rows and 2.44% / 2.73% /
     10.61% of training dollars (2021 / 2022 / 2023 starts). This confirms the splits_comment.
   - Losses of the last 6 months before the 2023 start (Ian): 56.8% of the rows and 77.8% of their dollars were
     last paid after the start.
   Equal training size, LightGBM-L2, RMSE (the builder measured Tweedie deviance, not the declared metric):
   | window | no gap (2nd subsample) | 6-month gap | 12-month gap | closed by the start |
   |--------|------------------------|-------------|--------------|---------------------|
   | 2023   | 72,976 (72,426)        | 67,845      | 67,492       | 71,407              |
   | 2022   | 221,188 (222,230)      | 223,197     | 223,093      | 225,834             |
   | 2021   | 68,556 (67,732)        | 70,411      | 69,848       | 69,664              |
   - The newest labels, unknown at the start, help in 2021 and 2022 by 1-3% and hurt in 2023 by 7%. In 2023,
     Ian's level overshoots the next year's claims.
   - A shortcut would show a consistent gain, and there is none; nor is there any selection at the release end
     beyond finding 2's open claims.
   - A gap would keep the floor (a 12-month gap leaves 81.6% for the oldest window), so the floor is not the reason.
     The reason is that the measurements show neither condition of the amended SPLIT-10.
   Remedy: none to the split. Restate the equal-size numbers in RMSE in splits_comment, next to or instead of the
   Tweedie ones.

4. [P4, SPLIT-20 (Should), SPLIT-21] History from 2010 (builder issue 2): keep it; no _1m.
   - The reason is a break in the collection, which SPLIT-20 asks for: building description filled on 44% of claims
     in 2009 and 78% in 2011; median coverage at the $250k limit by 2010.
   - Before 2010 the claims are a different dollar regime:
     | period    | claims  | mean claim |
     |-----------|---------|------------|
     | 1978-89   | 494k    | $6.5k      |
     | 1990-99   | 512k    | $12.8k     |
     | 2000-04   | 227k    | $21.5k     |
     | 2005      | 254k    | $68.7k     |
     | 2006-09   | 186k    | $29.1k     |
     | 2010-23   | 817k    | $51.1k     |
   - The full history's train sides are 2.37-2.47M rows: a _1m version only.
   Alternative run (LightGBM-L2, RMSE, 2010 start / full history at equal n / full history 1M sample):
   | window | 2010 start | full, equal n | full, 1M |
   |--------|------------|---------------|----------|
   | 2023   | 74,123     | 70,798        | 70,913   |
   | 2022   | 221,557    | 223,265       | 223,911  |
   | 2021   | 68,049     | 69,103        | 69,595   |
   The results are mixed, and by SPLIT-21 they decide nothing; they give no reason to depart.
   - Another break, Risk Rating 2.0 (October 2021), falls inside the test period: the "Rating engine" share is
     75.6% of 2021's claims, 95.9% of 2022's and 99.5% of 2023's.
   - It also reaches back into every train side: 33.5% / 36.0% / 40.2% of the rows of the 2021 / 2022 / 2023 train
     sides carry RR2.0 policy fields. For the 2021 window all of them were set after its start (Oct 2021 or later).
   - These are feature values of training rows that did not exist at the window start. This is the builder's
     issue 4 (later policy term, LEAK-10), for the leak reviewers. The split cannot fix it.

5. [P6, TP-9 (target spread per window); a metric question for MET-10/MET-11] One event decides two windows.
   Concentration per window:
   - 2022: Ian is 82.1% of the rows and 93.4% of the dollars. It holds 98.3% of the training mean's squared error
     and 98.6% of LightGBM-L2's; the top 100 of 55,699 claims hold 54-55%. The RMSE without Ian is 70,743 against
     228,257 with it.
   - 2021: Ida holds 74.6% (mean) and 76.7% (L2) of the squared error.
   - 2023: no event dominates (Idalia 25-31%; top 100 claims 30-38%).
   Rankings flip on the event:
   - 2022: LightGBM-Tweedie ties the mean with Ian (228,270 vs 228,257) and beats it by 12% without
     (62,179 vs 70,743).
   - 2023: LightGBM-L2 beats the mean with Idalia (74,287 vs 75,208) and loses without (75,087 vs 72,784).
   - The per-claim bootstrap SDs of the paired differences (282-1,732) ignore that claims cluster in events, so they
     understate the noise.
   Re-splitting does not cure it. One event dominates most NFIP years (Sandy 91.8% of 2012's dollars, Harvey 85.0%
   of 2017's, Irene 55.5%), so the windows show the task as it is:
   - Two-year windows (2022-23, 2020-21, 2018-19) leave Ian at 94.6% of the squared error.
   - Five yearly windows (2019-2023; the smallest train side 77.5%) add 2020 (no event above 35%) and 2019 (Imelda
     39.8%). Then two of five windows are one-hurricane windows instead of two of three. That departs from SPLIT-15's
     three folds at this size and adds compute.
   - Under Tweedie-1.5 deviance, Ian still holds 90.0% of the constant's deviance, but the top 100 claims fall from
     54% to 12%. The event share is the data's; the tail share is RMSE's.
   Remedy: keep three windows with a note giving these shares (recommended), or five windows. The tail share goes to
   the metric issue (builder issue 3).

MINOR (no change needed beyond the wording)
- The time column is the loss date, while the prediction point is the opening. 2,473 / 896 / 952 training claims
  (0.31% / 0.12% / 0.14%) were opened on or after their window's start. This is harmless apart from finding 1.
- Calendar-year windows hold whole hurricane seasons (June-November), so no test window is cut mid-season. The
  1 January boundary does fall inside the West Coast winter-storm season (finding 1).
- splits_comment: "whose events make most of a year's payments (2021 Ida, 2022 Ian, 2023 Idalia)". Idalia holds
  39.4% of 2023's dollars (April Florida Flooding 25.1%), so not most.
- Confirmed as stated: window sizes 43,494 / 55,699 / 19,897; oldest train side 697,854 (85.4%); training dollars
  last paid after the start 2.4% / 2.7% / 10.6%.
- No training weight, so the cut of a time on risk does not apply.

Sources: https://www.fema.gov/disaster/4683 ; https://www.caloes.ca.gov/wp-content/uploads/2023/02/FACT-SHEET-FEMA-4683-DR-CA-REVISED-2.8.23.pdf
```

</details>

<details><summary>Domain practitioner</summary>

```text
DOMAIN PRACTITIONER REPORT: nfip_redacted_flood_claims (2026-11-09)
Role played: a Write Your Own (WYO) insurer's claims and reserving desk, and FEMA's NFIP actuaries, setting the first
reserve when a flood claim is opened, before the adjuster inspects, and adding up an event's expected loss.

VERDICT
Fit: approximate (keep). One sentence: the actor, moment and decision are real and are now sourced (FEMA's reserving
bulletins say the initial case reserve "may be a system-generated amount based on criteria established by the Company",
refined by the adjuster's reports), and one row is one claim's reserve, but the policy fields are those of the policy's
latest term (certain for 71.5% of the 2021 test window), inputs the desk always has are redacted (the property's earlier
claims, the exact address, what the policyholder reported), and the 2023 payments may still grow by a few percent.
Metric: partly. RMSE in dollars scores the right quantity (the mean, which adds up to an event's loss) in the right unit.
But it squares the dollars: in the Ian window, 56 claims (0.1%) hold 45% of the score and condominium-association
policies hold 84%. I would score with the mean Poisson deviance in dollars. I would not use Tweedie at power 1.5.
SEL-1: holds. A reserve is program management, which the OpenFEMA terms allow. It is not a determination of a
policyholder's rights. Advance payments and inspection triage would be determinations, so keep them out of the use case.

Work files: the run folder  (raw_checks.py/.txt, rr2_missing.py/.txt, concentration.py/.txt,
metric_checks.py/.json/.log). The raw checks use the definition's row filters on 2010-2023 (818,282 rows, before the
1,338 double entries are dropped). metric_checks uses the shipped frame and splits (ds.make_splits()) and untuned
LightGBM (400 rounds, 63 leaves).

--------------------------------------------------------------------------------------------------------------------
HOW THE DECISION IS MADE TODAY (sources at the end)
- The case reserve is "the company's estimate of the value of future payments for an individual claim". "The initial
  case reserve may be a system-generated amount based on criteria established by the Company or it may be an
  individually set case reserve based on the best knowledge of the loss at the time the initial reserve is set.
  Subsequent adjuster reports should refine the case reserve amount" (FEMA bulletin W-10008, 2010-02-04, updating
  W-08095, 2008-12-22). This is exactly the task's actor, moment and decision. The definition's use_case still says
  "no source names this use (ours)"; that should now cite these bulletins. The model is still ours.
- The same bulletin says: "Following a catastrophe, instead of case loss reserves for individual claims, a company may
  bulk reserve for catastrophe losses". It also says "Case loss reserves have no direct effect on the NFIP's balance
  sheet" and "Consistency is more important than target accuracy". So for catastrophe claims (75% of the rows carry an
  event code), what matters is the sum: a bulk reserve, which is a count of claims times a mean. The per-claim mean is
  what feeds that sum.
- The adjuster's Preliminary Report is due within 15 days of assignment. It recommends separate building and contents
  reserves from the first inspection. The task's prediction point (opening, before inspection) comes before this
  report, so dropping the adjuster's report fields is right (USE-3, LEAK-10).
- FEMA's event estimate for Hurricane Ian ($3.5-5.3B, 2022-11-10, about 44,000 claims, $437M paid by then) used
  "policy information, daily reports of claims and payments, historical patterns of reported claims and payments,
  current economic conditions, and claim adjuster observations". It straddled the attachment of the NFIP's
  reinsurance. This event-level estimate is where the stakes are. A per-claim mean at opening is one input to it.

--------------------------------------------------------------------------------------------------------------------
Q1. AT THE OPENING, DO I HAVE EACH INPUT?
I have them, from the policy in force at the loss and the first notice: coverage and deductibles, rated flood zone and
community, CRS class, elevation certificate data, occupancy, floors, foundation, basement, construction and policy
dates, the location (state, county, ZIP, block group), the date of loss, the days from loss to notice, and the event.
The event designation is set by bulletin within days. For Ian, W-22005 assigned FL0222 from 2022-09-26, and W-22015
adjusted the dates of loss later (from the search results; the bulletins themselves were not read). A claim opened in
the first days gets its code a few days later, and the desk knows the storm anyway. Keeping floodEvent and event_code
is right (issue 6).

Inputs I would NOT have at the opening:
(a) Policy fields of a later term (issue 4). This is larger than the notes say. Risk Rating 2.0 began on 2021-10-01
    for new policies and at renewals from 2022-04-01. So a claim with a loss before 2021-10-01 that carries rating
    method "RE" or a 2-digit occupancy code certainly holds a later term.
    - Share of the shipped frame certainly from a later term: 71.5% of the 2021 test window (Ida, August 2021), and
      33.2% to 35.7% of the training sides. By year of loss: 40% (2016), 47% (2017), 50% (2018-2019), 63% (2020),
      71% (2021). So the record holds the policy's latest term, not the term at the loss.
    - The latest term is chosen partly by the outcome. In 2021 losses before October the RE share runs from 72.2% of
      zero claims to 78.0% of claims paid over $150k. Among 2016 to September 2021 losses, RE claims are zero 16% of
      the time against 18% for the others.
    - The fill pattern differs too. CRS class is missing on 36% of RE records against 64% of the others, and the
      basement type on 40% against 64%. So the missing cells also mark a later term.
    - Ablation (LightGBM-L2, rateMethod and occupancyType dropped): RMSE moves +24 / -222 / -126 in 2023 / 2022 / 2021,
      the same or better. The two fields carry no measurable signal for a reserve, only the survival marker.
(b) Construction dates moved after the loss. When a building is substantially damaged and rebuilt, NFIP rating dates
    the construction to the improvement. In this data 5,218 claims have originalConstructionDate after the loss, a
    median of 1.2 years later. That share is 0.15% of zero claims, 1.52% of claims paid $50-150k and 1.25% of those
    over $150k. The mean paid is $91.5k against $50.7k. It is 2.3% of substantially damaged buildings (damage at
    least half of value) against 0.36% of the others. These are mostly training rows of 2011-2012 (Irene, Sandy: 1-2%
    of those years), 0.03-0.05% of the test windows. The cells can be found row by row (date after loss), so LEAK-10's
    later-pull clause says to blank them.
(c) originalNBDate after the loss: 2.6% of zero claims against 3.4-3.6% of claims over $50k. The cells can be found
    the same way, so blank them under the same clause. The notes keep them because few test rows have them, but the
    rule does not depend on the test rows.
Checked and clean: disasterAssistanceCoverageRequired does not rise with the payment (0.5% at 0, 0.5% over $150k). The
elevated-building and post-FIRM shares do not rise with the damage. policyCount is never 0.

Inputs I would ALWAYS have that are missing:
- The property's earlier claims (repetitive-loss status, the count of earlier claims). The policy file has them; FEMA
  redacts the property id. USE-10: a repeat claim on a building is a known entity whose history I would use.
- The exact address. Coordinates are rounded to 0.1 degree, but the census block group is kept, which is close
  enough for reserving.
- What the policyholder reports at first notice (water in the living area, a rough depth). This is the strongest
  thing a desk hears before the inspection, and it is not in OpenFEMA.
- The flood at the property for this event (modelled surge or rain depth, high-water marks). FEMA's estimate uses
  "claim adjuster observations" and the stream of early claims for this. Without it the year's level is not
  predictable from the policy fields (below).

--------------------------------------------------------------------------------------------------------------------
Q2. IS THE TARGET WHAT I ACT ON?
- Building plus contents in dollars (issue 5): yes. The incurred loss of a claim is all its payments. The Preliminary
  Report reserves building and contents separately, but the claim's reserve and the event's loss are their sum.
  Contents are 11% to 22% of a year's dollars, and contents-only policies (no building coverage) exist. A
  building-only target would drop both. ICC is left out correctly: it is a separate payment, made after the
  community's substantial-damage decision, never known at opening.
- The zero claims (15.7%): keep them. Every claim gets a reserve at opening. A claim closed without payment (below
  the deductible, not a flood, not covered) releases its reserve, and that is an outcome I must predict.
- A number (the expected payment), not a class or a probability. The mean, not the median, because reserves add up.
- Release cut (issue 1): option (a), cut at 2024. A reserve is for the final payment. The 2024 claims (Helene,
  Milton) are about 712 days old, and claims still being paid at that age hold 3-5% of a year's dollars, 17% after a
  major hurricane. That is an undeveloped label (LEAK-24). An actuary would not fit on it. Revisit in 2027 (option c).
- History (issue 2): 2010+ is reasonable. Before 2010 the policy fields are mostly empty, and the dollars span 45
  years of construction costs.
- Nominal dollars: an actuary would trend past losses to the cost level of the test year. Trees cannot extrapolate
  the date. Every LightGBM under-predicts the 2023 window's total by 19-23% while the training mean is 4% over. I did
  not test whether inflation causes this. A cost index at the month of loss, known at opening, would be an expert's
  feature.

--------------------------------------------------------------------------------------------------------------------
Q3. ONE ROW, ONE DECISION; IS THE TEST WHAT I FACE?
- One row is one claim, which gets one initial reserve (building and contents set together): yes.
- The test is next year's claims from new flood events, with a model trained on all earlier claims (SPLIT-6): that is
  how a desk or FEMA would meet the next season. Refitting before the hurricane season (June) instead of on
  1 January would be more natural, but the difference is minor.
- Not what I face: the 2021 window's policy fields (71.5% from a later term, Q1a). For a model deployed today every
  policy is Risk Rating 2.0, so the 2022 and 2023 windows (0% certainly later term, 99.5% RE in 2023) are the
  realistic ones.
- The window's level is set by its events. Every model is far off on the window totals:
  - 2022 (Ian): LightGBM -63% to -73%, training mean -49%.
  - 2021: LightGBM -23% to -57%, training mean +7%.
  - 2023: LightGBM -19% to -23%, training mean +4%.
  Error on the event sums (sum over event codes of |predicted - actual| / actual): the training mean is best in 2021
  (0.236 against 0.260 for LightGBM-L2) and in 2022 (0.554 against 0.649). LightGBM-Tweedie is best only in 2023
  (0.262 against 0.409). So none of the per-claim metrics picks the model that gets the event sums right in 2 of 3
  windows. The level is luck unless an input tells how severe the event is (Q1 missing inputs).

--------------------------------------------------------------------------------------------------------------------
Q4. WOULD I USE IT?
- Not as it stands for the event estimate: R^2 about 0.15 (builder) and window totals off by 20% to 70%. FEMA's
  practice calibrates the level with the first claims and adjuster observations.
- Yes as the system-generated initial case reserve, the bulletin's first option, set before any adjuster report: a
  claim-level mean from the policy, building, place and event beats the flat or by-coverage figure a desk otherwise
  uses. LightGBM beats the training mean in RMSE on all three windows (builder), and the ROC AUC of any payment is
  0.65 to 0.75.
- As a triage ranking (which claims go to a senior or large-loss adjuster): yes. This is a nearby use case (USE-9),
  but it moves toward deciding how a policyholder's claim is handled. Keep the use case on reserving.
- What would make me trust it: actual against expected by event, state and coverage band; no fields from a later
  term; a level that holds after a trend for costs.
- What makes me distrust it: the RE marker and other later-term fields, the condominium-association claims driving
  the score, and the year-to-year level swings.

--------------------------------------------------------------------------------------------------------------------
Q5. DOES THE METRIC SCORE MY DECISION? Partly.
Right: RMSE is minimised by the mean, the quantity a reserve and a bulk event reserve add up (MET-1), on the dollar
scale I reserve in (MET-3). No amount at risk is needed (MET-14/15, as the notes say: the coverage and deductibles are
features).
Wrong for the desk: squaring the dollars puts the score on a few claims. The builder's argument for issue 3 ("coverage
limits cap the payments, so RMSE is less tail-dominated") does not hold. Condominium-association master policies are
covered up to $250k per unit (the largest claim is $10.8M), so the cap does not bind them. Share of the score taken by
the top 0.1% of claims / condominium associations, under the constant predictor (concentration.txt):
  window   squared error    Tweedie 1.5    Poisson       absolute    (condominium-association share of claims / dollars)
  2021     18.2% / 8.6%     2.7% / 2.5%    5.6% / 3.3%   2.0% / 2.2%     1.5% / 2.1%
  2022     44.6% / 83.7%    8.6% / 39.8%   14.9% / 53.5% 5.2% / 31.1%    8.5% / 29.9%
  2023     11.2% / 20.6%    2.1% / 7.6%    4.0% / 11.1%  1.6% / 6.8%     2.9% / 6.9%
LightGBM-L2 in 2023: condominium associations hold 36.6% of its squared error. Without them its RMSE falls from 74,287
to 60,045 (the mean's from 75,208 to 67,995). A desk would set those reserves by hand, and they decide the Ian window's
RMSE.
Scores on the shipped windows (2023 / 2022 / 2021; train mean, LightGBM fitted with L2, Tweedie 1.5 and Poisson
objectives):
  RMSE        mean 75,208 / 228,257 / 78,745; L2 74,287 / 221,180 / 68,044; Tw 65,426 / 226,457 / 75,099;
              Poi 66,544 / 223,950 / 69,992
  Tweedie1.5  mean 401 / 770 / 433; L2 712 / 1,684 / 641; Tw 305 / 993 / 442; Poi 317 / 785 / 335
  Poisson     mean 76,243 / 219,811 / 80,752; L2 62,635 / 205,990 / 59,222; Tw 54,196 / 240,255 / 76,558;
              Poi 56,293 / 209,089 / 59,147
What I would choose: the mean Poisson deviance in dollars (Tweedie power 1; `mean_poisson_deviance`, with
`min_prediction` set by MET-13, for example $10 as in the builder's probe).
- Like RMSE and Tweedie it is minimised by the mean, so reserves add up.
- In the Tweedie family it is the one rule whose cost grows in step with the claim's dollars: an error of 10% on a
  claim twice as large costs twice as much (RMSE: 4 times; Tweedie 1.5: 1.4 times). For a reserve, a dollar is a
  dollar.
- It halves RMSE's concentration (top 0.1% in 2022: 14.9% against 44.6%).
- It still separates models from the constant in all three windows (L2-fitted LightGBM 62.6k / 206.0k / 59.2k
  against 76.2k / 219.8k / 80.8k).
Tweedie at 1.5 (the noaa_storm_events_damage precedent) is a pricing view. It scores relative errors with weights
growing only as the square root of the dollars, and it punishes heavily a low reserve on a claim that pays. It ranks
the model that is best on dollars in 2 of 3 windows (L2) below the constant in all three, and in 2022 the constant
beats every LightGBM. That is not how I judge a reserve.
This is my reasoning from the decision, not a source's metric. FEMA and the papers define no metric, so under MET-11
it is a "context" choice only if the curator finds it obvious. Otherwise keep the fallback `rmse` (MET-8) and add a
note on the condominium-association concentration. MET-10 diversity would favour the Poisson deviance over one more
RMSE. Not wanted: MAE (it estimates the median, which understates a sum with 15.7% zeros), relative error (undefined
at the zeros), Gini (it ignores the level, which is the reserve).

--------------------------------------------------------------------------------------------------------------------
GAPS BETWEEN THE DATASET AND THE REAL DECISION, ranked by how much they change the task
1. Policy fields of the latest term, not the term at the loss. Certain for 71.5% of the 2021 test window and about
   a third of every training side. The latest term is slightly chosen by the outcome. LEAK-10 later-pull clause; for
   the fit, a kept potential leak under USE-8.
2. The event's severity is not in the inputs: no flood depth or surge, and no early-claims signal. The window totals
   are missed by 20% to 70%, and on the event sums the training mean beats the models in 2 of 3 windows.
3. Redacted inputs the desk always has: the property's earlier claims (USE-10), the first-notice description, the
   exact address.
4. The metric's weight on condominium-association claims (84% of the squared error in the Ian window).
5. Nominal dollars without a cost trend: the 2023 total is under-predicted by about 20%.
6. The labels of the newest window are still developing: claims paid more than 982 days after the loss hold 1.5% to
   2.7% of a normal year's dollars and 9.0% of the Ian year's. Small; handled by the 2024 cut.
7. Construction and new-business dates after the loss (0.6% and about 3% of claims, mostly training rows). Small,
   and fixable.

WHAT AN EXPERT WOULD CHANGE (in the definition, no rebuild done here)
- Drop rateMethod. It describes how the policy was priced, not the loss, and its "RE" value marks a later term. Map
  the Risk Rating 2.0 occupancy codes 11-19 onto one coarse scheme with the legacy codes (single family, 2-4 units, 5+
  units or condominium association, mobile home, non-residential). Then neither field marks the term. The ablation
  shows no loss.
- Blank originalConstructionDate and originalNBDate when they fall after dateOfLoss (LEAK-10 later-pull clause;
  5,218 and about 2-3% of rows).
- task_summary.use_case: cite FEMA W-08095 / W-10008 for the system-generated initial case reserve. Drop "no source
  names this use (ours)"; the model stays ours.
- fit_reason: name the later-term fields as kept (USE-8 says a kept leak is not a gap). Name the redacted inputs and
  the still-developing payments as the gaps.
- Notes: add the OpenFEMA clause "The data can be used to make decisions on program management". Say that advance
  payments ($5k without inspection, up to $20k with photos or receipts) and inspection triage are outside the use
  case (individual determinations, SEL-1).
- Metric: the mean Poisson deviance in dollars (issue 3), or RMSE with a note on the condominium-association
  concentration. Not Tweedie at 1.5.
- Optional, a future version: a construction cost index at the month of loss, and an event hazard covariate (e.g.
  NOAA or USGS peak water level by block group), both known within days of the event.
Agree with the builder on: issue 1 (a), issue 2 (2010), issue 5 (building plus contents), issue 6 (keep the event
fields), the zero claims, ICC left out, no weight (MET-14/15), the temporal yearly windows (SPLIT-6).

--------------------------------------------------------------------------------------------------------------------
SOURCES
- FEMA NFIP bulletin W-08095, "NFIP Case Loss Reserving Procedures", 2008-12-22, and W-10008, "Update - NFIP Case Loss
  Reserving Procedures", 2010-02-04 (both read in full):
  https://agents.floodsmart.gov/sites/default/files/bulletins/W-08095/w-08095.pdf
  https://agents.floodsmart.gov/sites/default/files/bulletins/W-10008/w-10008.pdf
- OpenFEMA Terms and Conditions (read 2026-11-09): "solely for statistical research or as a reporting record";
  "cannot be used to make determinations that might affect an individual's rights or eligibility for benefits"; "The
  data can be used to make decisions on program management." https://www.fema.gov/about/openfema/terms-conditions
- FEMA's Hurricane Ian preliminary NFIP loss estimate, as reported by Insurance Journal, 2022-11-14:
  https://www.insurancejournal.com/news/national/2022/11/14/694956.htm (Artemis and Reinsurance News on the
  reinsurance attachment, search results only).
- Adjuster's Preliminary Report within 15 days, with recommended building and contents reserves (FEMA form 086-0-13 /
  FF-206-FY-21-146 and FEMA EMI course IS-1104, from search results; the form PDF could not be read).
- Risk Rating 2.0 dates: Consumer Compliance Outlook, fourth issue 2021,
  https://www.consumercomplianceoutlook.org/2021/fourth-issue/compliance-alert-highlighting-recent-regulatory-changes-flood-insurance
  (search result summary).
- Ian event designation bulletins W-22005 and W-22015, and NFIP advance payments ($5,000 without an adjuster visit,
  up to $20,000 with documents): FEMA and FloodSmart pages, from search results only.
- Salas, Saha, Ravela 2022, arXiv 2212.08660 (abstract): a county-level claims model from rainfall, not a reserve.
- The dataset folder (dataset.py, README.md), the record, builder_report.md, probes/signal.json.
```

</details>

<details><summary>Blind review</summary>

```text
BLIND REVIEW: nfip_redacted_flood_claims  (target amount_paid_building_contents_usd, regression, temporal on dateOfLoss, 3 test windows)
Inputs used: the clean room's task.md, the clean room's data.parquet (200,000-row sample of 816,944), the OpenFEMA NFIP Redacted Claims v3 page, and live queries to the v3 API. No other local files were opened.
Scratch scripts: the run folder: scripts/model*.py

VERDICT
Include with changes. The data is real and large, and the target is verified against the source. But the policy fields are a later snapshot and one of them leaks the outcome, the raw-dollar target is dominated by a few dozen condo master-policy claims, and under the stated temporal split the signal barely beats a constant. All of this needs fixing first. Drop the task if, after the fixes, the best model's gain over a dummy model stays within noise.

WHAT THE TASK IS
Each row is one NFIP flood claim with a date of loss from 2010 to 2023. The prediction is the gross amount paid on building plus contents. Who would use it: a Write-Your-Own insurer or FEMA at first notice of loss (the claim's openDate), to set case reserves, triage adjusters, or estimate an event's total NFIP loss. That is a real use. At that point the policy, location, event and days from loss to open are known, while damage, water depth and payment are not. The preparer left out the post-inspection fields (buildingDamageAmount, waterDepth, floodWaterDuration, causeOfDamage, net payments, ICC), which is the honest choice.
Target checked against the API on 6 rows matched by censusGeoid and dateOfLoss; all 6 match. The target is amountPaidOnBuildingClaim + amountPaidOnContentsClaim, with nulls (closed without payment) set to 0. ICC is excluded: one row with a $30,000 ICC payment has target 218,180.68 = 191,758.52 + 26,422.16. Payments are gross, not net of recoveries. days_loss_to_open = openDate - dateOfLoss, also verified (0, 21 and 199 days all match).

CONCERNS, MOST TO LEAST SERIOUS

1. The policy and building attributes are a later snapshot, not the policy in force at the loss, and one of them leaks the outcome. [evaluation honesty]
   - Raw API records show 2010 losses with rateMethod "RE" (the Risk Rating 2.0 rating engine) and occupancyType 11 or 18. FEMA's page says "2-digit codes are for Risk Rating 2.0 policies", and RR2.0 only began in Oct 2021. In the data, the share of rows with RR2.0 coding rises from 9% of 2010 losses to 100% of 2023 losses. foundationType is filled in exactly when RR2.0 coding is present. FEMA's page does not say which policy term the attributes describe.
   - originalConstructionDate is after dateOfLoss in 1,355 sample rows (0.7%). The median gap is 1.2 years, so these are buildings rebuilt after the flood. Their median payout is $80,569 vs $18,288 for other rows; zero rate 3.8% vs 15.8%; median paid/coverage 0.35 vs 0.09. Within Hurricane Sandy (870 rows) the median is $94k vs $36k. This is direct post-loss information about severe damage.
   - originalNBDate is after dateOfLoss in 5,925 rows (3.0%), and the latest value is 2026-10-21. The payout signal here is weaker: median $25.2k vs $18.4k.
   - Paid exceeds total coverage in 0.54% of rows. Two cases confirmed in the API: building coverage $10,000 with $191,758 paid on the building, and coverage $1,800 with $6,386 paid. Both look like coverage taken from a different policy term.
   Fix: set construction and new-business dates that fall after dateOfLoss to NaN, or replace them with building age at loss and null the negative values. Document that policy fields reflect the latest policy record. Consider dropping rateMethod and the RR2.0-only fields, or collapse them onto one shared code scheme plus a flag.

2. Under the stated temporal split the signal is close to nil, and the last window is worse than a constant. [worth benchmarking]
   Method: LightGBM on the 200k sample with expanding windows. Cut points tried: 2017-09-10, 2019-09-10 and 2021-09-01; then 2017-11, 2020-01 and 2022-01.
   - Raw-dollar R2 by window: 0.02 / 0.13 / -0.04 with L2 loss; 0.07 / 0.08 / -0.06 with Tweedie loss. Spearman 0.25 to 0.49.
   - Log scale (RMSLE): 3.70 vs 3.82 for a constant; 3.92 vs 4.17; and 4.76-4.97 vs 4.13 in the 2022-23 window (Hurricane Ian is 59% of that window).
   - The same model on a random 5-fold split reaches R2 0.47-0.53.
   - Why the last window fails: in the 2022+ window the model's mean log prediction is 6.55 against a true mean of 8.87. Per-feature contributions put the shift on countyCode (-1.08) and state (-0.61). Past events taught it that SW-Florida counties have small claims, and Ian broke that. How hard a place floods is specific to each event, and nothing in the table measures it (no surge, rainfall or depth).
   - Each window is dominated by one or two hurricanes: Irma/Florence, then Ida/Imelda/Sally, then Ian/Ida. With only 3 windows, model rankings will be noisy.
   Fix: add more, smaller windows, or evaluate leave-future-event-out. Report a dummy baseline next to every model. Optionally add hazard covariates.

3. The raw-dollar target is extremely heavy-tailed, and the tail is a different unit of analysis. [metric and target]
   - Median $18.6k, 99th percentile $350k, maximum $8.76M. Zeros are 15.7%.
   - The largest values are condo association or RCBAP master policies covering 22 to 367 units (policyCount), mostly from Ian.
   - In the last window the top 0.1% of rows carry 45% of the total sum of squares, and the top 1% carry 74%. RMSE or R2 on dollars therefore scores a few dozen Ian condo claims.
   Fix: score on the log scale (RMSLE) or with Tweedie deviance. Alternatively restrict to policyCount == 1 (98.1% of rows, 94.4% of dollars paid), or predict paid per unit or paid/coverage.

4. Window boundaries may split one hurricane between train and test, and the target is only known after a settlement lag. [split realism]
   Row quantiles of dateOfLoss fall inside Harvey (0.6 quantile = 2017-08-26), Irma (0.7 = 2017-09-10) and Ida (0.9 = 2021-09-01). When a cut lands mid-event, up to 26% of test rows share an event_code with training rows. A claim from two days earlier would not have settled at prediction time.
   Fix: put cuts between events, or leave an embargo of a few months between the end of training and the start of the test window. I could not see the real window boundaries.

5. Encoding problems. [preparation]
   - foundationType "Code 0 (not in the data dictionary)" is 58% of rows. It means "not collected for legacy-rated policies" and should be NaN.
   - occupancyType and rateMethod mix two code schemes for the same concept, e.g. "Single family residence" and "Single-family residential building (RR2.0)".
   - disasterAssistanceCoverageRequired has "Code 3 (not in the data dictionary)" (2 rows) and an empty "HHS" level.
   - originalConstructionDate holds the placeholder 1753-01-01 (the SQL minimum date) and other pre-1800 dates.
   - elevationDifference has values -1716 and 987. Elevations above 5,000 ft are plausible (mountain states).
   - censusGeoid is a categorical with 40,862 levels in 200k rows, a near-ID that one-hot models cannot handle. Lat/lon are rounded to 0.1 degree by FEMA.
   - event_code and floodEvent are almost duplicates. Test-window events are mostly unseen in training anyway (event_code overlap 0-0.1% when cuts fall between events).
   - Fix: map these to NaN, drop or hash censusGeoid, keep county and zip, and turn dates into numbers (age at loss, month).

6. Undocumented row filter. [provenance]
   The API holds 858,454 claims for 2010-2023 and the task has 816,944, so 41,510 rows (4.8%) were dropped. By zero counts, almost all of them are zero-payment claims: the API has 169,650 null-or-zero claims, the data has about 128,400. Non-payment codes 98 ("Error-delete claim") and 99 ("Erroneous assignment") cover 39,612 claims. Dropping those is sensible but should be documented; about 1.9k rows remain unexplained.

7. Minor issues.
   - 141 groups of exact duplicate rows (319 rows, 0.16%), usually at adjacent indices. They are probably double records of one claim; drop them.
   - Group Flood Insurance Policy rows have standardized payouts (repeated $29,900). They are genuine.
   - 2023 losses may still have open or reopened claims (the data is refreshed monthly).

SIGNAL, SIZE AND REALISM
Real FEMA data with plausible values. 817k rows, so each window holds about 70-90k test rows. Real signal on random splits (R2 about 0.5), but little of it carries over to future events.

COULD NOT CHECK
- The actual window boundaries and the benchmark metric.
- The full 816,944 rows; I saw only the 200k sample.
- The exact filter the preparer applied (98/99 is my hypothesis).
- Whether FEMA attaches the latest policy term to old claims. The code evidence says it does, but FEMA's page does not say.
- Whether removing the leaky dates measurably changes model scores. The leak covers only 0.7% of rows.
- The RR2.0 start date (Oct 2021) comes from my own knowledge, not the source page.
```

</details>

<details><summary>Task gamer</summary>

```text
TASK GAMER REPORT: nfip_redacted_flood_claims (target amount_paid_building_contents_usd, RMSE, temporal on dateOfLoss)
Kit: the participant kit   Scripts and logs: the run folder 
Splits: r0f0 = test 2023 (19,897 rows), r1f0 = test 2022 (55,699 rows, Hurricane Ian), r2f0 = test 2021 (43,494 rows).
All scores: RMSE in USD from score.py, listed as r0f0 | r1f0 | r2f0. Lower is better.

VERDICT
The task can be gamed only a little. One real exploit exists: the final size of each flood event, counted from all the
test rows, including claims opened later. It cuts RMSE by about 10.4K (4.7%) on the 2022 (Ian) window and by 0.7K or
less on the other two windows. The policy attributes recorded after the loss are a flaw too, but they lower the honest
score rather than help a cheater.

REFERENCE MODELS
  Constant train mean                    75,208 | 228,257 | 78,745
  Baseline (untuned LightGBM, 100 trees,  71,603 | 231,921 | 72,582   (work/01_baseline.py)
    features() with dates as day numbers)
  Baseline noise (random column added,   72,003 / 72,038 | 231,865 / 231,983 | 72,523 / 72,850
    bagging seeds 1 and 2)               -> spread about 0.4K | 0.1K | 0.3K
  Best honest model HB                   65,037 | 221,888 | 67,788   (work/14_combined.py)
    HB = baseline - floodEvent/event_code + post-loss markers masked + counts of claims opened so far
    + training rows opened after the window start dropped
  HB over 3 bagging seeds (mean, sd)     65,731 | 221,364 | 68,093,  sd 563 | 1,914 | 152   (work/17_counts_seeds.py)
  The RMSE is dominated by a few huge condo-association claims. In r1f0 the 10 worst rows carry 21% of the squared
  error and the top 100 carry 53%: Ian claims of 5-10.8M USD that the baseline predicts at 20-120K
  (work/02_error_anatomy.py). The untuned baseline is worse than the constant on r1f0.

EXPLOITS RANKED BY GAIN

| # | Exploit | Script | Honest score | Exploited score | Gain (per split) | Deployed model has it? | Fix |
|---|---|---|---|---|---|---|---|
| 1 | Final event size: count of claims per event x state, week x state, date x state/county/zip/block group over ALL rows, test rows included | work/14_combined.py, 17_counts_seeds.py, 18_counts_mechanism.py, 06_test_counts.py | HB, mean of 3 seeds: 65,731 / 221,364 / 68,093 | 65,706 / 210,968 / 67,420 | +25 / +10,396 / +673 (seed sd 563 / 1,914 / 152). On the baseline, final counts (E2) against so-far counts (H2): +126 / +944 / +922 | No. At first notice the system knows only the claims opened so far | No batch fix. Evaluate online, revealing test rows in open-date order, or document the weakness |
| 2 | Training rows opened after the window start (dateOfLoss + days_loss_to_open >= first test day): 2,473 / 896 / 952 rows, 0.12-0.31% of training | work/07_train_rows.py, 14_combined.py | HB without them: 65,037 / 221,888 / 67,788 | HB with them: 64,767 / 221,530 / 67,741 | +270 / +358 / +47 (noise). On the baseline: +612 / +391 / -34 | No. These claims did not exist yet when the window started | Drop training rows whose open date falls on or after the test start |
| 3 | Post-loss policy markers made explicit (RR2.0 coding on a pre-RR2.0 loss, construction date - loss, NB date - loss) | work/05_postloss_attrs.py, 14_combined.py | HB (masked): 65,037 / 221,888 / 67,788 | 65,808 / 222,665 / 67,854 | -771 / -777 / -66 (hurts). On the baseline E1: -178 / +32 / +449 (noise) | No | See flaw A |

Mechanism, exploit 1. In the 2022 window the final size of the event across the state has a Spearman correlation of
0.25 with the payout; the count of claims opened so far has a correlation of -0.01. Across the test rows the final
count is a median 1.7x the so-far count. Ian is a single event of 45,709 claims, and its condo associations had
unprecedented severity. Knowing the event's final size tells the model the event is a catastrophe before the claims
that reveal it have been opened. One count alone carries most of the gain: event x state final count gives 213,725 on
r1f0 against 221,888 for HB, and week x state gives 214,490 (work/18.log). The open-order percentile (so-far count /
final count) adds nothing (work/17.log, XP). The deployable counterpart, counts of claims opened on or before the
row's own open date, is honest signal. It is most of what the naive E2 gains over the baseline (H2 vs baseline:
+3.5K / +6.6K / +2.5K). The mildest fix: none inside a batch test set. Score with an online protocol (rows revealed in
open-date order), or state the weakness.

Mechanism, exploit 2. A model deployed on the first day of the window cannot know claims opened later. Keeping them
gives at most 0.6K, below or near seed noise. The fix costs nothing: filter training rows on
open date < first test day.

FLAWS THAT HURT AN HONEST MODEL

| # | What is wrong | Honest choice | Baseline score | Honest-choice score | Change | Fix to the task |
|---|---|---|---|---|---|---|
| A | The claim rows carry a policy snapshot taken after the loss: RR2.0 coding (rateMethod 'Rating engine', occupancyType '(RR2.0)', foundationType filled) on losses before RR2.0 existed (2021-10-01) for 33-36% of training rows and 71% of the 2021 test rows; originalConstructionDate after the loss (0.65% of training: rebuilt houses, mean payout 95K, 2-3% zero-paid); originalNBDate after the loss (3%) | Map occupancyType to the legacy codes; set rateMethod/foundationType to missing on RR2.0-coded pre-RR2.0 losses; null construction/NB dates later than the loss (work/05_postloss_attrs.py H1, work/13_h1_parts.py) | 71,603 / 231,921 / 72,582 | 71,271 / 229,780 / 72,117 | +332 / +2,141 / +465 (baseline noise 0.4K / 0.1K / 0.3K) | Take the policy attributes in force on the loss date (NFIP policy file by policy term); else drop rateMethod/foundationType, harmonise occupancyType, null dates later than dateOfLoss |

Mechanism, flaw A. For a pre-2021 loss, the RR2.0 coding means "the policy still existed after the RR2.0 rollout":
survivorship that the outcome itself shapes. From April 2022, every claim in the test windows is RR2.0-coded, so the
code means something else on the test side, and the model mislearns it. Masking alone (H1b) gives 71,392 / 230,374 /
72,533; harmonising the occupancy codes alone (H1a) gives 71,571 / 231,067 / 72,812. Their combination (H1) is best.
Coverage and deductible amounts may come from the same later policy. The kit cannot show this, but 0.2-0.4% of test
rows were paid more than their recorded building + contents coverage.

Other honest gains (not task flaws). Dropping floodEvent/event_code improves the baseline to 69,315 / 229,368 / 72,034,
because every test event is a category never seen in training. The so-far claim counts are deployable signal. HB
combines everything above: +6.6K / +10.0K / +4.8K over the baseline.

ATTACKS THAT FOUND NOTHING
- Row order: within each date the rows are shuffled. Spearman of target vs. relative position = -0.0005. Correlation of
  log target with the next row = 0.128, and 0.124 after a within-date shuffle (same-date similarity only).
- Copies across the split: 9-25% of test rows have an exact feature copy in training (ignoring date/event), and 16-36%
  match the same property (census block group + construction date + units + condo type). The property's prior claims
  are known to the insurer at first notice, so this is signal. Used as features (H4): 71,053 / 232,029 / 72,025 vs.
  baseline 71,603 / 231,921 / 72,582 (+550 / -107 / +557, noise level). Correlation of log y with the property's last
  log payout: 0.20-0.28. (work/09_copies.py)
- Formats: lat/lon all at 0.1 degree, elevations at 0 or 1 decimals. A value-free format model (missingness + number of
  decimals) scores 73,749 / 226,113 / 77,914, against the constant at 75,208 / 228,257 / 78,745. The missingness is
  substantive (no named event, no elevation certificate), not a recording artefact. A looser format model (adds last
  digit and trailing zeros, which encode values) scores 70,767 / 228,868 / 72,423. (work/08_formats.py,
  work/15_strict_formats.py)
- Single features / lookups: no column comes near HB. The best single column is totalBuildingInsuranceCoverage
  (73,030 / 221,197 / 74,975). No post-outcome column and no formula recovers the target. (work/16_single_features.py)
- Ratio-to-coverage target and 1000 trees (honest variants): no gain (73,099 / 232,068 / 77,298 and
  71,476 / 234,557 / 74,661). (work/04_honest_variants.py)
- Train-vs-test classifier: AUC 0.996-0.998, driven by floodEvent names (77-87% of gain), the expected time shift
  only. (work/10_adversarial.py)
- Transforms over all rows: none. Values are raw; no column is standardised, min-max scaled or ranked.
- Identifiers: no row id or asOfDate in the kit. event_code (EDN/FICO) and floodEvent are event names; the
  data dictionary says the EDN is assigned when the catastrophe happens, so they are available at first notice.
  censusGeoid / zip / community / county are geography.
- days_loss_to_open (late claims pay less: 64% zero-paid above 730 days) is known at first notice. If openDate were
  reset when a claim is reopened, it would carry post-loss information. The data argues against that (late claims pay
  less, not more), but the source does not say.
- Training rows with a loss in the last 180 days dropped (proxy for immature labels): 72,650 / 232,228 / 72,560, worse.
  The proxy is too crude to show anything (it removes Ian from the 2023 training set).
- Web: no competition, forum, leak or "magic feature" thread exists for this source. Papers that model NFIP claim
  amounts (Salas, Saha & Ravela, arXiv 2212.08660) name no leaky fields. Looking the rows up in the published OpenFEMA
  file would very likely recover the target (dateOfLoss, censusGeoid, construction/NB dates and coverages are
  unrounded), but I did not run it; it is not a flaw of the task.

WHAT THE PREPARATION CHANGED (compared with the OpenFEMA v3 dictionary)
- Dropped: payments, damage amounts, property values, replacement costs, water depth, cause of damage, non-payment
  reasons, ICC, recoveries, mostRecentPaymentDate, asOfDate, id, current flood zone/community.
- openDate became days_loss_to_open; deductible codes were decoded to USD; losses run 2010-2023.
- The latest open date is 2026-08, so labels come from a 2026 snapshot.
- Nothing was rounded beyond the source (the source already rounds lat/lon to 0.1 degree).

WHAT I COULD NOT CHECK
- Label maturity. A model deployed on the first day of a window would see partial payments for the claims of the
  months before (Ian, September 2022, for the 2023 window). The kit gives final 2026 amounts and has no close or
  payment date, so the gain from final labels in training cannot be measured.
- Whether coverage, deductible and the other policy fields come from the policy in force on the loss date. The RR2.0
  evidence says many do not; the policy file would decide it.
- When FEMA assigns floodEvent/EDN relative to each claim's open date (decides whether the named-event columns are
  fully available at first notice).

Sources: https://www.fema.gov/openfema-data-page/nfip-redacted-claims-v3 ; https://arxiv.org/abs/2212.08660 ;
https://www.fema.gov/flood-insurance/risk-rating (RR2.0 start dates: new policies 2021-10-01, renewals 2022-04-01)
```

</details>

<details><summary>Precedent check</summary>

```text
PRECEDENT CHECKER REPORT: nfip_redacted_flood_claims (2026-11-09)

Read: principles.md, metrics.md (MET-1 to MET-17 and Cases), leak_checks.md (LEAK-6, -7, -10, -24, -38, -41 and the
Mechanisms rows), splits.md (SPLIT-10, -20, -21), use_case.md (USE-5), selection.md (SEL-1), evidence.md (EV-4); the
definition and README (df-large); the record and nfip_redacted_claims; builder_report.md, signal.json, leak_raw;
register.json (34 flags, the decisions under LEAK-24, SPLIT-20, SEL-1, MET-14, MET-16, USE-5, LEAK-10); the
claim_auditor report (the only phase-A report written when I finished) and the column auditor's scratch
the run folder: c3_term.txt. Family precedents read in datasets/_dev/tabarena-v0pt2/: noaa_storm_events_damage
(dataset.py, REVIEW.md issues 4, 8, 10), pricing_game_2017_french_mtpl, pricing_game_2016_french_fleet, fremtpl2, bemtpl97,
australian_vehicle_insurance_2004_2005, frempl_french_motor_personal_line, spanish_* (3), allstate_* (2),
liberty_mutual_fire_peril_loss_cost, wisconsin_local_government_property_insurance_fund, porto_seguro; batch builder
reports of kumc_inpatient_aki_prediction, sinan_dengue_case_screening, wioa_employment_after_exit,
ny_wcb_assembled_claims; tunisian_fraud_detection_challenge, distribution_transformers_at_cauca_department.
My own measurements (scripts and output in the run folder ): pc1_tail_event.py / .txt (tail share of the
squared error), pc2_event.py / .txt (event code within state x date cells; it confirms the claim auditor's result).

VERDICT
Six of the eight calls follow their precedents. Two do not:
- The later-term policy fields depart from a Must (LEAK-10, later-pull clause). The stated reason, that the late cells
  cannot be located, is refuted by the data. The traced part carries a mechanism tied to the outcome. This is not a
  reasonable exception under the ranking: fix it, or amend the rule on purpose. ny_wcb_assembled_claims in this batch
  makes the same keep.
- The metric departs from the closest precedent (noaa_storm_events_damage, Tweedie from context, Lennart 2026-11-08). It
  has one real, now-measured fact that sets it apart: the tail share of the squared error. The builder's second reason
  (the signal under Tweedie) is the situation noaa's issue 10 already kept the deviance through, so it does not set the
  case apart. This is a weighing call for the curator.

SUMMARY TABLE (decision | verdict | closest precedents | what sets this case apart)
1 Metric: fallback rmse | departs from noaa, with a stated reason, half of it valid | noaa issue 8 B and issue 10 A
  (Lennart 2026-11-08); pricing_game_2017 Tweedie (Andrej 2026-11-03) | coverage caps payments: the top 0.1% of claims
  hold 11/45/18% of the squared error (2023/2022/2021) against noaa's 99.94%; the signal argument is no distinction
1b Coverage: a feature, no weight (MET-14 to MET-16) | consistent | wisconsin (2026-11-08), liberty_mutual var11 (Andrej
  2026-11-02), this record's assessment of 2026-10-30 | -
2 Target: building + contents, dollars, zeros kept | consistent | Andrej 2026-10-30 (total suggested; zeros, policy
  question 2); Lennart CC 2026-11-08 (left to /add-dataset); noaa dollars, untransformed | -
3 Release cut at 2024 (LEAK-24) | consistent | tunisian fiscal 2018 cut (Lennart 2026-11-04); batch: ny_wcb cut at 2020,
  wioa newest window kept with a ~0.9-point revision; kumc and sinan not comparable (labels final at release) | no
  second download: the payment dates stand in for LEAK-24's decisive test
4 Later-term policy fields kept with a note | departs, a Must, stated reason refuted | zillow_prize and
  melbourne_housing_market (located cells blanked, 2026-10-21); distribution_transformers (dropped, 2026-10-21);
  onlinenewspopularity (kept, no gain, 2026-10-26); medical_facility (kept, within noise, 2026-11-05); tunisian (registry
  kept, no mechanism; CTR_CESSAT dropped, 2026-11-05); batch: ny_wcb issue 1 (the same keep) | the fact the builder
  offered (not locatable, few test rows) does not hold
5 Event fields kept | consistent (codebook timing; measured: a function of state and date) | noaa issue 4 (Andrej
  2026-11-03, storm-size counts left out) is set apart | the designation is the source's per-state, per-date bulletin
  field; no claim's payment sets it
6 History from 2010, not 1978 as _1m (SPLIT-20) | consistent | chicago_traffic_crashes (Lennart 2026-11-04), noaa (2007),
  fraud_detection_in_electricity_and_gas_consumption_1m (Lennart 2026-10-26), aeolus (2026-10-12); batch ny_wcb (2015) |
  one supporting fact is wrong; one break inside the history is unnamed
7 causeOfDamage dropped | consistent now that it is measured (claim auditor); the stated reason was wrong | noaa
  TOR_F_SCALE dropped (damage-derived rating); LEAK-10 "missingness that encodes the outcome" | -
8 OpenFEMA terms (SEL-1) | consistent | EV-4: lucas_topsoil (2026-09-23), Zindi terms (2026-10-21); Pima (SEL-1 case);
  fema_ihp_valid_registrations (Andrej 2026-10-30, its SEL-1 question open) is set apart | -

DETAILS

1. Metric (MET-1, MET-10, MET-11; Tensions row "the source's metric against a better metric")
- Closest precedent: noaa_storm_events_damage, REVIEW.md issue 8, resolved B by Lennart on 2026-11-08 ("we should
  start from the right metric and maybe ignore prior claims if they dont match the task"). The mean Tweedie deviance at
  power 1.5 from context, with a $1 floor, on untransformed dollars. noaa's decisive reason was that the planner sums
  expected dollars. RMSLE, the alternative then on the table, is minimised by a geometric mean. RMSE was never an
  option in noaa. Its metric reason sets squared error aside in one sentence: "on the dollars the largest 0.1% of the
  entries hold 99.94% of the squared deviation".
- This case has the same logic. The use case says "to add up the expected loss of a flood event", and the metric reason
  says "an event's loss is the sum of the reserves, which the mean minimises". RMSE and the deviance are both minimised
  by the mean. So the fallback follows noaa's decisive reason and departs only from the metric noaa picked.
- Fact 1 offered, that coverage caps the payments so RMSE is less tail-dominated: measured, it holds. On the shipped
  windows the largest 0.1% of test claims hold 11.6% / 44.9% / 18.2% of the squared deviation from the training mean
  (2023 / 2022 / 2021). The largest 1% hold 45% / 77% / 49%. My pc1 output agrees with the claim auditor's 11.2 / 44.6 /
  18.2%, and 38.4% over all rows. noaa's figure is 99.94%. So this fact sets the case apart. It is weakest in the
  hurricane window: in 2022 the 357 claims over $1M hold 72% of the squared error (claim auditor).
- Fact 2 offered, that untuned LightGBM-Tweedie loses to the training mean in 2022 and 2021: this does not set the case
  apart. In noaa, issue 10 (Lennart 2026-11-08, A) kept the deviance after the task probe flagged no_signal under it, and
  declined option B, "back to RMSLE" for a clear signal. noaa's untuned 400-tree Tweedie also lost to the training mean
  in 2023 and partly in 2024, while 100 trees and tuning beat it. nfip's comparison is one untuned fit (400 trees, 63
  leaves, a $10 floor; scripts/nfip_signal.py). Under RMSE the gain is also within noise in two windows: 1.2% and 2.9%
  against a bootstrap SD of 1.9% and 4.2% (claim auditor).
- Other factors:
  - Diversity (MET-10, Andrej 2026-11-02). RMSE is declared by 35 of the working copy's 88 regression definitions; a
    Tweedie deviance by 3 (noaa, pricing_game_2017, pricing_game_2016 rescaled). When the call stays in doubt, the rarer
    metric wins.
  - The family. No insurance claim-amount task in the working copy is scored by RMSE. They use Poisson or Tweedie
    deviances, Ginis, or allstate_claims_severity's competition MAE. But MET-10 forbids a family-wide call, so the family
    pattern is context, not a rule.
- Drift: none. Lennart's metric calls since 2026-10-21 run consistently toward the metric the task makes obvious
  (diamonds; loan_default_prediction_imperial_college; noaa; pricing_game_2016's "use it going forward", which is scoped
  to rescaling markets).
- If the curator keeps rmse, the metric reason should:
  - lead with the tail numbers against noaa's 99.94%;
  - drop or demote the Tweedie-signal sentence;
  - add DELUGE to "where we looked" (claim auditor).
  If the deviance is chosen instead:
  - MET-13 needs a floor two orders below the smallest plausible mean, rounded down to a power of ten (noaa $1,
    pricing_game_2017 0.1 EUR). The $10 in the builder's comparison was not derived that way.
  - CLEAN-16 keeps the target untransformed, as now.
  - The signal should be checked with tuned, early-stopped fits, as in noaa's issue 10.
- Reflection prompt: PROMPT A below.

1b. Coverage: amount at risk or weight? (MET-14, MET-15, MET-16, LEAK-41)
- Consistent.
  - MET-14 covers an amount accrued over a varying amount at risk (time on risk, vehicle-years, area swept). A flood
    claim is one event, and coverage is a cap fixed at the policy's start, so it is not an exposure.
  - MET-15: the reserve is per claim and the event sum counts each claim once, so the score is unweighted with no
    sample weight.
  - MET-16: there is no survey or design weight.
- Precedents:
  - wisconsin_local_government_property_insurance_fund (property; building and contents sum insured): "the coverage is a
    feature" and "not an offset", LEAK-41 and MET-15 hold (REVIEW.md outcome, 2026-11-08).
  - liberty_mutual_fire_peril_loss_cost: var11, the sum insured, stays a feature (MET-2 amendment, Andrej 2026-11-02).
  - This record's AI assessment of 2026-10-30: coverage and deductibles as features.
- Caveat, a LEAK-10 matter and not an exposure one: the claim auditor finds circumstantial evidence that the stated
  coverage is itself a later term's (16.3% against 22.5% of claims over $100k reach the cap).

2. Target (USE-5; MET-3; CLEAN-16; MET-13 only if a deviance is declared)
- Consistent. The building plus contents total was the target the AI assessment of 2026-10-30 suggested, verified as
  screened by Andrej's CC of 2026-10-30. Lennart's CC of 2026-11-08 left the choice to /add-dataset, and the event-loss
  sum needs both coverages.
- Zeros kept, and a non-payment reason counted as 0: Andrej, 2026-10-30, policy question 2 ("We don't care. We want to
  add any relevant predictive task, independent if it is zero inflated or not"). noaa keeps 68% zeros. The claim auditor
  checked that the kept reason codes (01, 06, 08, 20, 97) are real claim outcomes and that 98/99 are clerical.
- Untransformed dollars: MET-3, scored on the scale the task means. It matches noaa (CLEAN-16 under a deviance).
- ICC left out: a separate coverage paid later on a substantial-damage finding. No precedent conflicts.
- The register's USE-5 flag (diabetes_3, xente, chicago_traffic_crashes) is about other mechanisms; not relevant here.
- Open, for the domain practitioner and not a consistency matter: whether reserves are set per coverage, which would
  argue for building only (draft issue 5).

3. Release cut at 2024 (LEAK-24, Must)
- Consistent.
- Curator precedent: tunisian_fraud_detection_challenge (Lennart 2026-11-04, "do the change"). The newest fiscal year
  was cut because its labels were materially incomplete (adjustments 3 times smaller, probe 13 z -6.7). The year before
  stayed because it was in band.
- nfip does the same: 2024 is cut, where the claims still being paid hold 2.9-4.9% of a year's dollars and 17.3% for a
  major hurricane year (Helene and Milton fall in 2024). 2023 stays, with an upper bound of 1.5-2.7% still to come (9.0%
  Ian-like), stated in the notes.
- Batch pairs:
  - ny_wcb_assembled_claims cuts at 2020, where outcomes are 88% complete for the rare classes. It is the same rule
    applied the same way.
  - wioa_employment_after_exit keeps its newest window with a revision of about 0.9 points (about 1.4% relative), noted
    as weak (its issue 3). That is the same residual size nfip keeps for 2023.
  - kumc_inpatient_aki_prediction (whole stays, no censoring) and sinan_dengue_case_screening (labelled years 2016-2021,
    long closed, plus a one-month gap) have final labels at release, so they set no threshold to compare with.
- Difference in evidence: LEAK-24 asks to "compare two downloads first". ny_wcb (a June 2021 copy) and wioa (successive
  files) had a second download; nfip has none (v2 retired, no archive), so the last-payment dates stand in. The claim
  auditor confirms the numbers. The notes should name that the decisive test was not available, and the 2027
  re-download (draft issue 1, option c) as the revisit.
- No gap (SPLIT-10): an application with its measurement, as for lt_vehicle_loan_default_prediction (Lennart
  2026-11-05) and ny_wcb in this batch. It adds no exception to the register's SPLIT-10 "amendment due" flag. The equal-
  size test is mixed: the gap is 23% better in 2021 (claim auditor).

4. Later-term policy fields, kept with a note (LEAK-10, Must, later-pull clause; LEAK-6, LEAK-7)
- The rule (clause amended 2026-10-26, Lennart): "A value read at a later pull goes where its late cells can be located:
  they are blanked ...; where they cannot be located row by row, the values go when they may carry a gain ... and stay
  with a note only when the part that can be traced shows none." Main text: attributes looked up after the outcome are
  out "unless the data shows they did not change".
- The builder's stated reason: the later term cannot be located for most claims, and blanking reaches few test rows
  (0.6-2.7%). Both are refuted:
  - Risk Rating 2.0 codes before October 2021 locate 264,880 rows (32% of the data) and 31,072 of the 43,494 rows of the
    2021 test window (71%).
  - The policy start falls after the loss on 4.8% / 2.7% / 1.3% of the three windows, not 2.7 / 1.3 / 0.6.
  - A construction date after the loss locates 5,218 rows.
  - Sources: the claim auditor; the column auditor's c3_term.txt.
- The traced part shows a mechanism tied to the outcome:
  - Among substantially damaged buildings (ICC paid), 79.4% of later-term records are elevated against 39.9% of the
    others (difference in differences +35 points).
  - The claims with a construction date after the loss are 3.8% zeros against 15.8%, with a mean of $91.5k against
    $50.8k.
  - Located later-term rows have fewer zeros in every year from 2012 to 2019 (column auditor).
  - The model gain is small and circumstantial: +0.038 against +0.021 R^2 on later-term against other test rows in 2021.
- Precedents:
  - zillow_prize and melbourne_housing_market (Lennart 2026-10-21): located late cells blanked.
  - distribution_transformers_at_cauca_department (Lennart 2026-10-21): changed for an unknown subset, a gain may sit,
    so dropped (ROC AUC 0.701 against 0.639).
  - onlinenewspopularity (Lennart 2026-10-26): kept, the traced part shows no gain.
  - medical_facility_operational_data (Lennart 2026-11-05): kept, worth within two seed SDs.
  - tunisian_fraud_detection_challenge (Lennart 2026-11-05): registry fields looked up at extraction "with no mechanism
    that ties a change of the attribute to the outcome" kept with a note; CTR_CESSAT, "a status that records a later
    event of the entity", dropped.
- Drift: none. Lennart's line from 2026-10-21 to 2026-11-05 is consistent: keep only with no gain or no mechanism; blank
  what can be located. The nfip keep would be the first departure from that line.
- Pairs:
  - nfip splits naturally along the tunisian line. The RR2.0 recodes (rateMethod RE, 2-digit occupancy, perhaps
    foundation code 0) have no outcome mechanism, like tunisian's registry codes. The fields a large loss changes
    (elevatedBuildingIndicator, originalConstructionDate, originalNBDate, floodproofing, obstruction, basement and
    foundation, lowest floor and elevation difference, perhaps coverage) are like CTR_CESSAT.
  - ny_wcb_assembled_claims in this batch (draft issue 1) recommends the same keep for its 2026 field values against a
    measured gain (0.071 log loss from restoring the June 2021 WCIO codes). If both keeps are accepted, two datasets in
    one batch would depart from a Must clause the same way. That is a rule change, not two exceptions, and the two
    should be decided together.
- Ranking: LEAK-10 is a P4 Must. The tension "a real task against a leak" (P3 and P4) says to fix the leak and keep the
  task, not to keep the leak. No higher-ranked Must overrides it, so a keep with a note is not a reasonable exception:
  it needs the fix or a deliberate amendment.
- Reflection prompt: PROMPT B below.

5. Event fields kept (floodEvent, event_code; LEAK-10, LEAK-38)
- Consistent.
- The codebook dates the designation to the event. FICO: "Number assigned at the time of a significant flooding event".
  EDN: "A public bulletin will designate the EDN number assignments by state with corresponding dates of loss".
- Measured (my pc2, matching the claim auditor): within every (state, date of loss) cell the claims are all coded or all
  uncoded; 613,169 coded rows share their cell with no uncoded claim. So no claim's handling or payment sets the code,
  and the 13% / 24% zero split is an event effect.
- LEAK-38 (keep with a note) does not apply, since this is not challenge data. Its conditional test (fill given the
  covariates known at the prediction point differs by outcome) passes anyway, so LEAK-10's codebook test decides, and it
  holds.
- noaa issue 4 (Andrej 2026-11-03: storm-size counts left out) is set apart. Those counts were built by us over entries
  some of which exist only because of damage. Here the designation is the source's own per-state, per-date field, and
  the claim volume behind a FICO office counts claims, zero-paid ones included, not payments.
- Residual: claims opened before their event's bulletin, untested (no bulletin dates in the data). The note should say
  this; the claim auditor agrees.

6. History from 2010, not 1978 as _1m (SPLIT-20 Should; SPLIT-21 Must)
- Consistent. Every precedent starts the training side at a recording or rule break:
  - chicago_traffic_crashes (Lennart 2026-11-04): training from citywide coverage;
  - noaa (2007): the entry-format change;
  - fraud_detection_in_electricity_and_gas_consumption_1m (Lennart 2026-10-26): a measured step;
  - aeolus (Lennart 2026-10-12): a recent stretch;
  - ny_wcb in this batch: the EDI break, 2015.
  None kept a full history as _1m across such a break. The choice was not made from a window comparison (SPLIT-21
  holds).
- Two gaps in the stated reason (claim auditor):
  - "By 2010 the median building coverage has reached $250,000" is false: $191,200 in 2010, $250,000 first in 2012.
  - Risk Rating 2.0 (October 2021) is a rule and recording break inside the kept history and the windows, and goes
    unnamed. SPLIT-20 asks for breaks to be named. chicago_traffic_crashes (Lennart 2026-11-05) accepted a recording step
    as drift with a note, so a note here would be consistent.
- The fill break (2009-2011) alone carries the call.

7. causeOfDamage dropped without measurement (LEAK-6, LEAK-7, LEAK-10)
- At build time this departed from LEAK-6 ("Measure before acting"). The stated reason, the handling codes B, C and D,
  does not hold: those codes appear on at most 0.1% of a year's claims (1.9% in 2020).
- Now measured by the claim auditor:
  - code 0 "Other causes" carries 38.7% zeros against 8.7-14.3% for the flood codes;
  - 20.9% of code-0 claims carry the denial "06 Not actual flood", against 1.9% of the others;
  - the 5,831 missing codes are 91.4% zeros.
  So the column records the adjuster's call on whether it was a flood, and its missingness encodes the outcome.
- With that, the drop is consistent with LEAK-10 ("missingness that encodes the outcome"; a consequence of the target)
  and with noaa's drop of TOR_F_SCALE, a rating "based on the amount and type of damage".
- LEAK-7 (blank only some codes) gives no smaller fix, since the flood/non-flood codes themselves carry the denial. The
  builder's probe 20 also had the column alone below the dummy (R^2 -0.0085).
- The notes bullet should replace the B/C/D reason with these numbers.

8. OpenFEMA terms (SEL-1 Must; EV-4)
- Consistent.
- SEL-1's case (Pima) is about subjects or creators who object to ML use. The OpenFEMA terms (2025-01-22) object to none
  of it:
  - they forbid re-identification and "determinations that might affect an individual's rights or eligibility for
    benefits";
  - they allow "decisions on program management";
  - they allow use "solely for statistical research or as a reporting record".
  A benchmark is research, and a reserve sets neither a payment nor eligibility.
- Under EV-4 (lucas_topsoil 2026-09-23; Zindi terms 2026-10-21) the terms are a one-line note and a release-checklist
  item, never a reason.
- The sibling fema_ihp_valid_registrations (Andrej 2026-10-30, `TBD -> 2nd Tier`) left its SEL-1 question open. That
  task's target is itself a benefit award, the kind of determination the terms name, so it is set apart.
- Quasi-identifiers (census block group, ZIP, rounded coordinates, dates) parallel ny_wcb's issue 5 in this batch (ZIP
  kept because the state publishes it). A weighing note at most.

REGISTER FLAGS READ
None of the 34 flags is about this dataset. The related ones:
- LEAK-10 exception_to_must (loan_default_prediction_imperial_college, Andrej 2026-11-03): aggregates of a hidden x, not
  the later-pull clause, so it does not count toward a third exception of item 4's kind.
- SPLIT-10 amendment_due: nfip's no gap is an application, not an exception.
- USE-5 opposite outcomes: other mechanisms.

PROMPT A (item 1, metric; for the curator's review file)

**Consistency check (AI, 2026-11-09):** Score this task by RMSE on dollars, although for noaa_storm_events_damage's sum
of expected dollars you chose the Tweedie deviance on 2026-11-08?

   * **Problem:**
     - Both use cases add up expected dollars over an event; RMSE and the deviance both score that through the mean, and
       noaa's reason set squared error aside because its largest 0.1% of entries held 99.94% of it.
     - Here coverage caps each payment, and the largest 0.1% of claims hold 12%, 45% and 18% of the squared error in
       2023, 2022 and 2021, though in 2022 the 357 claims over $1M (Ian) hold 72%.
     - The builder's other reason, an untuned Tweedie fit losing to the training mean in two windows, is the weak
       signal you kept the deviance through in noaa's issue 10, and it comes from one 400-tree fit.
   * **Background:**
     - Under RMSE, LightGBM beats the constant by 1.2%, 2.9% and 13.6%, within one bootstrap SD in 2023 and 2022.
     - RMSE scores 35 of the working copy's 88 regression tasks and a Tweedie deviance 3; no insurance claim-amount task
       uses RMSE.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | RMSE, the cap as the fact that sets it apart (implemented) | keeps the fallback; the reason leads with the tail shares against noaa's 99.94% and drops the Tweedie-signal argument | the measured difference from noaa; an error in reserve dollars | 2022 still decided by about 360 large claims; one more RMSE task |
     | b | Treat it like noaa | mean Tweedie deviance at power 1.5 from context, a floor by the collection's rule, dollars untransformed | the same metric for the same summed-dollars use; a rarer metric in the collection | the signal under it is untested with tuning |
     | c | Probe first | tuned, early-stopped Tweedie fits on the three windows as in noaa's issue 10, then a or b | settles whether the weak signal is the untuned fit | a probe to run before deciding |
     | d | Change the rule | a summed expected dollar amount is scored by a Tweedie deviance unless a fact sets it apart | ends the case-by-case call | a family-wide metric call, which the rules declined on 2026-11-02 |

   * **Recommendation:** a, with the reason rewritten around the measured tail shares, because noaa's decisive fact (a
     metric minimised by the mean) holds under both; b if you read the call as still in doubt, since the diversity
     factor then favours the deviance. **Decision:** a, b, c or d?

   [^pa1]: **MET-11** (Must): fallback only when the task makes no metric obvious; context when it does. **MET-10**
     (Weigh): resolution on our folds, diversity "when the call stays in doubt" (Andrej, 2026-11-02), no family-wide
     call. noaa_storm_events_damage REVIEW.md issue 8 (Resolved B, Lennart 2026-11-08) and issue 10 (Resolved A,
     Lennart 2026-11-08). **MET-13** (Must): the floor of a deviance.

PROMPT B (item 4, later-term policy fields; for the curator's review file)

**Consistency check (AI, 2026-11-09):** Keep the later-term policy fields with a note, although a third of them can be
located and the located part carries a mechanism tied to the payment?

   * **Problem:**
     - Every precedent blanks located late cells; here Risk Rating 2.0 codes before October 2021 locate 32% of the rows
       and 71% of the 2021 test window, not the few test rows the draft issue counted.
     - The located part is tied to the outcome: after a substantial loss 79% of later-term records show an elevated
       building against 40% of the others, and claims with a construction date after the loss are 4% zeros against 16%.
     - The recodes with no such mechanism (rating method, occupancy) match tunisian_fraud_detection_challenge's registry
       fields, kept with a note, while its cessation status, a later event of the entity, was dropped.
   * **Background:** ny_wcb_assembled_claims in this batch recommends the same keep against a measured gain; two such
     keeps would change the rule rather than make an exception.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep, the task's core as the fact that sets it apart (implemented) | keeps every policy field with a note rewritten to the true scope; records that the later term spans the whole policy record and its mechanism reaches at most 0.4% of a window's squared error | the task's core inputs stay whole | a Must has no exceptions, so this needs d; the stated reason (not locatable) does not hold |
     | b | Treat it like the precedents | blank, on the located rows, the fields a large loss changes (elevation, construction date, policy start, floodproofing, obstruction, basement, foundation, lowest floor, elevation difference); keep the rating and occupancy recodes with a note | follows zillow_prize and melbourne_housing_market for located cells and tunisian for mechanism-free codes; coverage and deductibles stay | the unlocated 2022 rows (Ian, 97% recoded) keep the risk; models meet blanks on about a third of the rows |
     | c | Blank every policy field on the located rows | as b, for coverage, deductibles, rating and zone too | removes the located later term completely, coverage included | 71% of the 2021 window loses its core inputs |
     | d | Change the rule | amend the later-pull clause: a later term of the task's core record stays with a note when its measured reach is small | a deliberate rule; ny_wcb would follow it | loosens a Must on circumstantial measurements |

   * **Recommendation:** b: it is the mildest fix that follows the precedents, and it keeps coverage, the task's core,
     while the note states the unlocated 2022 risk and the coverage evidence. **Decision:** a, b, c or d?

   **Notes for the AI:** on b, mask in `_clean` on rows with `rateMethod == "RE"` and a loss before 2021-10-01, or a
   policy start or construction date after the loss; list the masked fields and counts in the notes; re-run
   `dataset check`, the task probe and leak probe 20; decide ny_wcb_assembled_claims' issue 1 by the same answer.

   [^pb1]: **LEAK-10** (Must), later-pull clause (amended 2026-10-26, Lennart): located late cells are blanked;
     unlocated values stay with a note only when the traceable part shows no gain. Mechanisms rows: zillow_prize and
     melbourne_housing_market (2026-10-21), distribution_transformers_at_cauca_department (2026-10-21),
     onlinenewspopularity (2026-10-26), medical_facility_operational_data and tunisian_fraud_detection_challenge
     (2026-11-05). **LEAK-6** (Must): measure before acting. principles.md, Tensions, "A real task against a leak":
     fix the leak and keep the task. "Exceptions and amendments": a Must has no exceptions.
```

</details>

<details><summary>Advocate</summary>

```text
ADVOCATE OPENING BRIEF: nfip_redacted_flood_claims (2026-11-09)

POSITION
Ship after changes. The task is real and FEMA's own bulletins describe it. The data is FEMA's system of record, and
four independent audits upheld every validity check except one. That one is real: the policy block holds the
policy's latest term (LEAK-10). The rules as written allow a fix for it: move the test windows past the Risk Rating
2.0 changeover. The other problems the panel found have mild fixes that need no decision from the curator.

Judgment record, as I argue it
  Verdict: ship after changes.
  Validity: SEL-1 holds (program-management clause); USE-1 holds, fit approximate, now sourced (W-08095, W-10008);
    USE-5 holds; LEAK-10 triggered twice: rebuilt buildings (fixed by blanking those rows' building fields) and the
    latest-term policy block (fixed by re-cutting the windows, the unlocated residue noted);
    LEAK-24 holds (cut at 2024); SPLIT-6 holds; SPLIT-9 triggered (356 rows, filtered); SPLIT-10 holds (no gap, an
    application); SPLIT-20 holds; LEAK-9 triggered (event size read from the test block: a protocol line).
  Value: TP-2 holds (a small real signal on 3 of 3 windows); TP-9 holds (thousands of claims per window).
  Quality: CLEAN-10, CLEAN-11 fixes; wording.
  Weighed: source +, sourced use case +, size +, gap (insurance claims, temporal) +; signal -, event concentration -.
  For the curator: the window re-cut (or keep the yearly windows with a LEAK-10 amendment, decided with ny_wcb
    issue 2); the metric (rmse or the mean Poisson deviance).

POINTS, STRONGEST FIRST

1. The task is real and sourced, and the data's terms allow it. [P1 SEL-1 Must; P3 USE-1, USE-5, USE-12 Must]
   - FEMA bulletin W-10008 (2010, updating W-08095 of 2008; the domain practitioner read both in full): "The initial
     case reserve may be a system-generated amount based on criteria established by the Company ... Subsequent
     adjuster reports should refine the case reserve amount." That is this task's prediction point (the opening,
     before the adjuster) and its decision: a per-claim mean, which also sums to an event's bulk reserve.
   - OpenFEMA terms: "The data can be used to make decisions on program management." A reserve decides neither a
     payment nor eligibility (claim auditor, domain practitioner, precedent checker).
   - Target: building plus contents in dollars, with the zeros kept. Every reviewer who checked it agrees
     (USE-5; Andrej 2026-10-30).
   - Against the objections: the fit stays approximate (later-term fields, redacted inputs, payments still
     developing). USE-12 (Must, P3) says a leak is no reason to reject a real task: fix it and keep the task.
   - Changes needing no decision: use_case cites W-08095 and W-10008 and drops "no source names this use"; the
     SEL-1 note quotes the program-management clause and leaves advance payments and inspection triage out of the
     use case.

2. The other P4 checks held under independent audit. The problems they found have mild, agreed fixes.
   [LEAK-10, LEAK-24, SPLIT-6, SPLIT-9 Must; SPLIT-10, SPLIT-20 Should]
   - Held:
     - The claim and column auditors checked each of the 30 dropped fields against the v3 dictionary.
     - Dropping causeOfDamage is now backed by numbers: code 0 is 38.7% zeros against 8.7-14.3% for the flood
       codes, and missing codes are 91.4% zeros.
     - event_code and floodEvent depend only on state and date: 0 of 816,944 claims sit in a state-date cell
       with mixed coding.
     - The release cut at 2024 is option (a) for the builder, the claim auditor, the split auditor, the domain
       practitioner and the precedent checker.
     - Temporal by date of loss, no gap (an application, as in lt_vehicle_loan_default_prediction), history from
       2010 at a break in how fully the fields were filled: the split auditor rates the split "right with notes".
   - Fixes:
     - (SPLIT-9) Drop the 356 training rows of the California atmospheric river that span the 2023 start
       (0.04%; FEMA DR-4683 runs from 27 Dec 2022 to 31 Jan 2023; 93.9% of those rows were paid after the start).
     - Drop the training rows opened on or after their window's start (2,473 / 896 / 952). The task gamer
       found this costs nothing.
     - (LEAK-10 later-pull clause, located cells) Blank the building fields on the 5,218 claims whose
       construction date falls after the loss. These are rebuilt buildings, with a median paid of $81k against
       $18k. Paired by seed, the scores move within noise (column auditor V4), and only 16 / 28 / 6 test rows
       change.
     - Correct the wrong texts: "no event spans a window start", "events with no claim in training", "$250,000
       by 2010", the later-term numbers, the probe-13 wording. Restate the no-gap measurement in RMSE.
   - Why these do not block shipping: each is a separate failure with its own fix in the definition (ladder
     step 2). None calls for dropping the dataset.

3. There is a real signal, and the windows are large. [TP-2 Should; TP-9 Must; TP-1 Must]
   - LightGBM beats the training mean on 3 of 3 windows (builder: skill 0.160, SE 0.053).
   - A Poisson-objective LightGBM scored by RMSE: 66,544 / 223,950 / 69,992 against 75,208 / 228,257 / 78,745,
     that is -11.5% / -1.9% / -11.1%. The unpaired bootstrap SD of a window's RMSE is 1.9% / 4.2% / 2.2%.
   - Under the mean Poisson deviance, every fitted LightGBM beats the mean in all three windows: 62.6k / 206.0k
     / 59.2k against 76.2k / 219.8k / 80.8k (domain practitioner).
   - The blind reviewer's "close to nil" used its own cuts, on a 200k sample, falling inside Harvey/Irma and Ida.
     The shipped windows avoid such cuts.
   - TP-9 asks about a handful of positives per window. These windows hold 19,897 to 55,699 claims. One event
     holding 98% (2022) or 75% (2021) of the squared error is how this data is: Sandy is 91.8% of 2012's
     dollars, Harvey 85% of 2017's, and no re-split cures it (split auditor). The 2022 window is hard, not empty
     (TP-2). Give the shares in splits_comment.

4. The policy block holds the latest term. I concede it, and the fix is a re-cut of the windows, not a rule change.
   [P4 LEAK-10 Must, later-pull clause; SPLIT-14 Must; the remedy ladder]
   - Conceded:
     - 71.8% of the 2021 test window (31,213 of 43,494) can be located as a later term.
     - The renewal that term records follows the outcome. Within a state-date cell, zeros are 14.7% against
       20.7% from April 2022, and 16.7% against 19.6% in 2021.
     - The notes understate all of this. A keep with a note fails the clause as written.
     - Blanking the located cells does not cure 2021: the blank carries the same bit and RMSE worsens by 8.2%
       (column auditor V1). The scheme stays readable from the other fields at AUC 0.999.
   - Fix: the bit reaches a test row's outcome only when the test window comes before the changeover, so move the
     three windows after it, to half years 2022H2, 2023H1 and 2023H2. My count on the column auditor's frame
     (the run folder: clean.parquet):

     | window | test claims | train side | coded RR2.0 | located later term | legacy code after Apr 2022 |
     |---|---|---|---|---|---|
     | 2022H2 | 52,972 | 91% | 96.6% | 2.7% | 3.4% |
     | 2023H1 | 7,115 | 98% | 99.5% | 2.6% | 0.5% |
     | 2023H2 | 12,782 | 98% | 99.5% | 0.7% | 0.5% |

     The current 2021 window has 71.8% located.
   - On the training side, follow the clause:
     - Blank the located cells of the fields a large loss changes (the precedent checker's option b).
     - Drop rateMethod and map the 2-digit occupancy codes onto the legacy classes. The task gamer's H1 makes
       this change and improves the honest RMSE on all three current windows: +332 / +2,141 / +465, beyond seed
       noise in 2022 and 2021. Dropping rateMethod and occupancyType costs the domain practitioner nothing.
       Dropping the three scheme fields costs the column auditor 0.36% in 2021 (3 of 3 seeds); it could not
       separate legitimate RR2.0 information from the survival bit.
   - The unlocated residue is Ian: 96.8% coded RR2.0 against about 60% the renewal schedule allows. Its traced
     mechanism, elevation after substantial damage, reaches the ICC rows: 0.39% of the 2022 test rows and 0.1% of
     its constant's SSE (claim auditor). It stays with a note if the curator reads that as no gain. Otherwise the
     fields a large loss changes go, and coverage, deductibles, zone, occupancy and place stay.
   - Why this outranks the alternatives:
     - The ladder puts a re-split (step 2) before a note or an amendment, and a Must has no exceptions.
     - It meets SPLIT-14 (3 windows, every train side above 50%). Dropping only the 2021 window would not.
     - It handles the case the way ny_wcb was handled: its late values were dealt with under the clause as
       written, with no amendment.
     - The domain practitioner: "For a model deployed today every policy is Risk Rating 2.0, so the 2022 and 2023
       windows ... are the realistic ones." The yearly cadence was ours anyway (SPLIT-12), and the practitioner
       finds a refit before the season more natural.
   - Costs, stated:
     - Ida's window goes.
     - Each window is more dominated by one event: Ian 98.5%, the April Florida flooding 62% and Idalia 51% of
       the constant's SSE.
     - Nobody has run models on the new windows.
     - The event-span filter applies at every window start.
   - Alternative for the curator: keep the yearly windows under the column auditor's option (a), an amendment of
     the clause, decided together with ny_wcb issue 2.

5. The event-size exploit is an evaluation leak, fixed by a protocol line, not a data change. [LEAK-9 Should]
   - The only exploit that pays counts each event's final size over the test rows: -4.7% RMSE on 2022 (10,396),
     and +25 / +673 on the other windows (task gamer). A deployed model has no such count.
   - LEAK-9 (amended 2026-11-05, medical_facility_operational_data): when a model can read other test rows, the
     fix is a protocol line the benchmark checks.
   - Change: add the line. The notes say that the count of claims opened so far is a real input at deployment,
     which the batch protocol forbids.
   - Every other attack found nothing: row order, copies, formats, single features, transforms, ids.

6. The metric is a weighing call and blocks nothing. [MET-10 Weigh; MET-11 Must; MET-13 Must]
   - rmse is a legitimate fallback (MET-11). Its distinguishing fact against noaa holds over all rows: the largest
     0.1% of claims hold 38.4% of the squared deviation, against noaa's 99.94%. It fails in 2022, where
     condominium associations hold 84%.
   - The domain practitioner's mean Poisson deviance:
     - keeps noaa's decisive reason (the mean, summed dollars);
     - halves the 2022 tail share (top 0.1%: 14.9% against 44.6%);
     - separates models from the constant in all three windows (point 3);
     - adds diversity (rmse scores 35 of the 88 regression tasks), MET-10's tie-break.
   - Tweedie at power 1.5 puts the model that is best on dollars below the constant in all three windows.
   - My reading: the mean Poisson deviance from context, with min_prediction set by MET-13, if the curator finds
     it obvious. Otherwise rmse with the reason rewritten: the tail shares, a condominium note, DELUGE added.
     The dataset ships under either.

7. The cleaning gaps are P7 and cheap to fix. [CLEAN-10, CLEAN-11 Should; principles, step 3]
   - Foundation code 0 to missing: it is on 99.97% of legacy rows and 0% of RR2.0 rows, so it means "not
     collected". Scores move within noise (column auditor V5).
   - Mask elevations above the state's highest point, -999.9, and |elevationDifference| > 100 ft. Set the two
     impossible coordinates missing.
   - Add a note on numberOfFloors.
   - Correct the wording: 58.4% not 51%; 4.35% not 4.0%; 2,276; the cap (48,250 claims paid exactly a limit hold
     21.2% of the dollars).
   - The FIRM flags that are both False (47%) are a question for a note.
   - "A very real task carries cleaning imperfections when they are written down" (principles.md).

Rebuttal

The critic and I agree on the verdict (ship after changes) and on most fixes. One new fact first, because both
questions put to me depend on it.

NEW FACT: signal on the half-year windows, 3 seeds per objective.
- Setup: untuned LightGBM with the column auditor's encoding and parameters (c5_gain.py). The critic's point-3
  filters are applied: event-span training rows and training rows opened after the window start are dropped
  (431 / 2,502 / 710 rows). Script and output: scratchpad recut_signal.py and recut_signal.txt (paths in the
  hand-back).
- Change against the training-mean constant (positive = better):

  | window | L2 fit, RMSE | Poisson-objective fit, RMSE | Poisson-objective fit, Poisson deviance |
  |---|---|---|---|
  | 2022H2 (Ian) | -1.2 / -1.3 / -1.6% | -1.2 / -1.2 / -1.3% | -30 / -28 / -28% |
  | 2023H1 | +1.5 / +2.6 / +0.9% | +1.0 / +0.9 / +0.6% | -8 / -8 / -9% |
  | 2023H2 | +7.3 / +8.2 / +5.4% | +5.6 / +5.8 / +6.4% | +12 / +14 / +15% |

- Paired bootstrap SD over claims of the RMSE gain (seed 0): 0.1% / 0.8% / 0.5%. It ignores clustering in events,
  so it understates the noise.
- This confirms the critic's single seed and gives its sign on every seed.
- Since the deviance pays only on 2023H2 (half-year windows), the yearly 2023 window's DP win (-26%) must come
  mostly from H2. A score on these windows depends on the one event each window holds.

Q1. Does the task still clear TP-2 and TP-3 under the re-cut?
- TP-2 (Should): yes.
  - The signal is real and concrete in 2 of 3 windows: +5-8% in 2023H2, and +1-3% in 2023H1 at about 2 SDs.
  - The Ian loss has a cause found in the task: a level no training event showed (the blind reviewer traced it
    to the SW Florida county effects). It is not new to the re-cut. On the yearly 2022 window, the column auditor's
    L2 fit (231,639) and the task gamer's baseline (231,921) also lose to the constant (228,257).
  - TP-2: "Retire, fix or keep a task for a concrete reason found in the task itself; until one is found, the
    task stays."
- TP-3 (Must): cannot be decided yet. It asks about tuned methods, and none exist for a new dataset.
  - TP-1 (Must) makes an untuned loss a question for tuned, early-stopped fits.
  - The like case is noaa_storm_events_damage (Lennart, 2026-11-08). Untuned fits lost to the mean there; tuned
    ones won 3 of 3 windows, and it shipped.
- The order of the rules:
  - The tension row "the right split against the score" (P4 over P6) says a small signal under the right split
    is no reason to retire. I keep the re-cut.
  - I concede the cost is larger than my brief said. The strongest window (2021, +13.6%) goes, and the other two
    get thinner.
  - Ask for the tuned probe on the new windows before the build. It answers TP-3 and also the metric (Q2).

Q2. The metric switch: the curator's call, not a change without decision.
- MET-11 (Must) allows "context" "only when the context is clear; otherwise the fallback". Whether it is clear is a
  judgment. MET-10 is a Weigh rule, and principles.md sends weighing calls to the curator. The noaa consistency
  question goes to the curator as a question (consistent judgement, case 2), never as an override.
- The new fact weakens the case for the switch. Under the re-cut, the Poisson deviance puts untuned fits below the
  constant in 2 of 3 windows, against 1 of 3 for RMSE. So the resolution argument (MET-10) that the domain
  practitioner and the critic made on the yearly windows does not carry over.
- I revise my opening reading. Put it as an issue with options:
  (a) rmse, with the reason rewritten (tail shares, condominium note, DELUGE);
  (b) mean_poisson_deviance from context, with min_prediction set by MET-13;
  (c) decide after the tuned probe on the chosen windows.
  I recommend (c), with rmse as the default if the probe does not settle it.

The critic's points, one by one
1. Later-term block, re-split [LEAK-10 Must]: agreed, the same windows. Two concessions:
   - Training rows: the critic's LEAK-11 (Should, narrows LEAK-10) is the rule's text. A value after the outcome
     that only weakens the signal stays, with a note. The task gamer's explicit markers cost the honest model
     771 / 777 / 66, so I withdraw my blanking of the located training cells.
   - Harmonising rateMethod and occupancy becomes optional. It is a modelling choice, not required.
   - The critic's "SPLIT-20" cost is real: 2023H1 holds no hurricane season and 2022H2 is one hurricane. SPLIT-20
     is a Should and loses to the LEAK-10 Must in the same part.
2. Rebuilt buildings and policy dates [LEAK-10 Must, located cells]: conceded in full.
   - Blank originalNBDate where it falls after the loss, as well as the rebuilt-building fields.
   - My brief left NB inside the policy-block decision. Under the re-cut it is located on 1,381 / 184 / 81 test
     rows, and the clause blanks located cells.
   - The note says that the blank marks these rows (12.9% against 14.9% zeros within a cell).
3. The storm spanning a start, and rows opened after the start [SPLIT-9 Must, SPLIT-10 Should]: agreed (my
   point 2). The filter works on the new windows: it drops 2,502 rows before 2023H1.
4. Protocol line [LEAK-9 Should]: agreed, and the critic's wording is better than mine.
   - Counts that use only the claims opened before the row's opening are what the desk has at deployment. The
     task gamer: the so-far counts are honest signal.
   - The curator should confirm it, because medical_facility_operational_data's line forbade any use of other
     test rows.
5. Metric [MET-1, MET-10, MET-11]: the facts are agreed (condominium associations hold 83.7% of 2022's squared error
   under the constant). The remedy is disputed: it is the curator's call, after the probe (Q2).
6. CLEAN-10 and CLEAN-11 [Should]: agreed, the same fixes.
7. Writing [USE-8, LEAK-26, SPLIT-20, LEAK-24]: agreed, every correction. Also add: the windows' signal on untuned
   fits (the table above) in splits_comment, and the 2027 revisit for yearly 2022 / 2023 / 2024 windows.

What remains open for the curator: the re-cut against the yearly windows with an amendment, decided with
ny_wcb issue 2; the metric; the causal count clause. Each depends on, or is helped by, a tuned probe on the new
windows.
```

</details>

<details><summary>Critic</summary>

```text
CRITIC, OPENING BRIEF: nfip_redacted_flood_claims (2026-11-09)

Read: dataset.py and README.md (df-large), principles.md, leak_checks.md (LEAK-6, -7, -9, -10, -11, -24, -26),
splits.md (SPLIT-1, -9, -10, -14, -20, -21), metrics.md (MET-1, -8, -10, -11, -13), task_probes.md (TP-1, -2, -3, -9),
builder_report.md, the seven phase-A reports, and ny_wcb_assembled_claims' mediator report. One measurement of my own:
the run folder: resplit.py and resplit.txt (the windows of remedy 1, on the column auditor's clean.parquet).

VERDICT: do not ship as defined. Ship after changes 1 to 3 (validity), with 4 to 7 made at the same time. The task is
real (USE-1, USE-12), and nothing here argues for excluding it.

Judgment record (as I argue it)
  Validity: LEAK-10 triggered (clause 2): the keep with a note rests on a refuted premise; fix = re-split away from
    the 2021 window (point 1). LEAK-10 located cells: blank them (point 2). SPLIT-9 triggered: one storm spans the 2023
    start; filter it (point 3). LEAK-9: protocol line (point 4).
  Value: MET-1 / MET-11: rmse scores a few hundred condominium-association claims; Poisson deviance from context
    (point 5). TP-2: the signal is small but real.
  Quality: CLEAN-10 foundation code 0, CLEAN-11 elevations (point 6). Writing: refuted statements (point 7).

---------------------------------------------------------------------------------------------------------------------
1. [P4; LEAK-10 Must, clause 2 (later pull); SPLIT-1 Must] The 2021 test window is scored on a policy record that did
   not exist at the loss.
 Problem. The policy block is the policy's latest term at extraction, not the term in force at the loss. The note keeps
   it because the later term "cannot be located for most claims", and draft issue 4 says blanking "reaches few test rows
   (0.6-2.7%)". Three auditors refute both premises.
 Evidence.
   - Risk Rating 2.0 codes (in use from 2021-10-01) appear on 264,880 rows with a loss before that date (32% of the
     data). In the 2021 window that is 31,072 of 43,494 test rows, and 31,213 (71.8%) with NB or construction dates
     after the loss (claim and column auditors). The RE share rises by quarter toward the extract: 48% in 2019Q1, 78%
     in 2021Q3. That is the pattern of a latest term.
   - The scheme records a later event: whether the policy was renewed after the loss. Compared inside state x date-of-
     loss cells (the event fixed), the zero share is 16.7% (RE) against 19.6% in 2021 before RR2.0, 14.7% against 20.7%
     in 2022-04 to 2023, and 10.6% against 12.9% in 2010-2015 (column auditor). After a substantial loss (ICC paid),
     79.4% of later-term records are elevated against 39.9% of the others, a difference in differences of +35 points
     (claim auditor).
   - No fix works inside the window. Blanking the located cells turns the blank into the same bit and costs +8.2% RMSE
     on 2021. Dropping rateMethod, occupancyType and foundationType leaves the scheme readable from the other fields
     at ROC AUC 0.9987, and at 0.921 from the missingness alone (column auditor).
   - The worth at model level is small and points one way: the three scheme fields are worth +0.36% RMSE on 2021,
     positive for 3 of 3 seeds (column auditor).
 Effect. In 2021, three of four test rows carry features of a rating scheme that existed neither at their loss nor on
   the window's refit date, and the scheme carries a survival bit. A model deployed today meets RR2.0 at the loss
   (domain practitioner, Q3: the 2021 window is "not what I face").
 Rule. Clause 2 lets values that cannot be located stay with a note "only when the part that can be traced shows
   none". Here the traced part shows a mechanism and a difference in the same direction in every period. A Must has no
   exceptions. Precedents: tunisian_fraud_detection_challenge dropped CTR_CESSAT, "a status that records a later event
   of the entity", and the renewal scheme is such a status. distribution_transformers_at_cauca_department dropped its
   fields. ny_wcb_assembled_claims, in this batch, dropped every field whose traced gain exceeded 2 SE (mediator), and
   the burden was on the keep. A keep here would be the first departure from Lennart's line (precedent checker).
 Remedy: fix the definition by re-splitting. LEAK-7 names "drop the months where the feature misbehaves"
   (online_shoppers) and "cut the censored years" (sf_permit_time) as smallest fixes.
   - Drop 2021 as a test window. Meet SPLIT-14's three windows after the RR2.0 renewal start (2022-04-01), for example
     half-years 2022H2 / 2023H1 / 2023H2. My measurement: 52,972 / 7,115 / 12,782 test claims; train sides 91.1% /
     97.6% / 98.4%; 0 located RR2.0 codes in test; legacy-coded test rows (the "not renewed" bit) 3.4% / 0.5% / 0.5%,
     against 24.4% in the shipped 2021 window.
   - The 2021 rows stay in training. There a later term can only mislead: made explicit, the markers cost the honest
     model 771 / 777 / 66 RMSE (task gamer). That falls under LEAK-11 (Should), with a note.
   - Costs, stated: one untuned L2 LightGBM seed scores -2.3% / +1.0% / +7.7% RMSE against the constant on these
     windows. The signal is thin, but P4 outranks P6 ("the right split against the score"; TP-1, TP-2), and the task
     probe decides on tuned fits. 2023H1 holds no hurricane season (SPLIT-20, Should). That is the price of three
     windows in 21 months. Revisit with the 2027 download: yearly windows 2022 / 2023 / 2024 once 2024 settles.
   - Rewrite the later-term note, fit_reason and draft issue 4 with the true scope.
   If the curator keeps 2021, that is a deliberate amendment of clause 2, decided together with ny_wcb (which went the
   other way). It is not a note.

2. [P4; LEAK-10 Must, located late cells; LEAK-7] Rebuilt buildings and policies written after the loss.
 Problem and evidence.
   - 5,218 claims have originalConstructionDate after the loss: buildings rebuilt after this flood, a median of
     1.2 years later. They are 3.8% zeros against 15.8%, with a median of $81,003 against $18,305; 97.7% are post-FIRM
     and 92.4% elevated. Inside a state-date cell log1p is +1.65, within 19 events +1.49 (column auditor).
   - 24,358 claims have originalNBDate after the loss: a policy written after the loss, 4.8% / 2.7% / 1.3% of the
     2021 / 2022 / 2023 windows, not the 2.7 / 1.3 / 0.6 the notes give. In a cell they are 12.9% zeros against 14.9%.
 Effect. A consequence of the target used as a feature, mostly on training rows (2.0% of 2012; 16 / 28 / 6 rebuilt
   test rows).
 Rule. Located late cells are blanked (clause 2; zillow_prize, melbourne_housing_market).
 Remedy. In _clean, where construction is after the loss, blank originalConstructionDate and the building fields the
   rebuild sets (post-FIRM, pre-FIRM, elevated, EC indicator, the four elevations, foundation, obstruction, basement).
   Blank originalNBDate where it is after the loss. The measured cost is within seed noise (column auditor). The note
   says that the blank marks these rows.

3. [P4; SPLIT-9 Must; SPLIT-10 Should] The 2023 window start splits one storm, and the train sides hold claims not
   yet opened.
 Evidence.
   - The "California Atmospheric River" has 356 training claims dated 2022-12-27..31 and 1,405 test claims dated
     2023-01-01..03-25. FEMA DR-4683-CA gives an incident period of 27 Dec 2022 to 31 Jan 2023. 76.7% of the test
     claims are in the counties of the December claims. 93.9% of the 356 were last paid after 2023-01-01.
   - None of these claims has an event code, so the builder's code check missed the storm.
   - With the 356 rows, the mean prediction on the 996 January-February claims is $43,631, against $31,536 without
     them (actual $40,287). The event's level transfers; the RMSE change is within noise (split auditor).
   - Separately, 2,473 / 896 / 952 training claims were opened on or after their window's start (task gamer, split
     auditor).
 Rule. SPLIT-9: a training label that tells a test row's outcome and was unknown at its prediction point is removed
   "whatever it costs". The link is one physical storm in the same counties, not a code shared by many entities
   (SPLIT-10's diffuse case). SPLIT-10: a refit at the window start knows only the claims that exist.
 Remedy. In the splits, drop from each train side:
   - the claims of any event (floodEvent or event_code) that has claims in that test window (356 rows, 0.04%);
   - the claims opened on or after the window start.
   Correct the three texts that say no event spans a start. The filter applies unchanged to point 1's windows (2023H1
   starts on the same date).

4. [P4; LEAK-9 Should] An evaluation leak through the test block: the final size of each event.
 Evidence. Counts of claims per event x state (or week x state, date x place) over all rows, test rows included, cut
   RMSE by 10,396 on 2022 (4.7%; seed SD 1,914) and by 673 on 2021 (SD 152). The deployable count, claims opened so
   far, does not carry it: Spearman with the payout 0.25 for the final count against -0.01 for the count so far (task
   gamer).
 Effect. A transductive method would rank above honest ones on the Ian window.
 Rule. LEAK-9: an evaluation leak is fixed by a protocol line the benchmark checks, not in the data. A method that
   learns from the test block is called out.
 Remedy. A protocol line in the notes: no feature or fit uses the test rows (counts, event sizes, other aggregates); a
   per-row count uses only the claims opened before the row's opening.

5. [P6; MET-1 Must, MET-11 Must, MET-10 Weigh] RMSE scores a few condominium-association claims, and the reason given
   for setting the case apart from noaa fails in the window that decides.
 Evidence.
   - Under the constant, condominium associations hold 83.7% of 2022's squared error, the top 0.1% of claims 44.6%,
     the 357 claims over $1M 72.4%, and Ian 98.3% (domain practitioner, claim and split auditors). The cap does not
     bind an association ($250k per unit; the largest claim is $10.8M on 198 units).
   - Resolution: under RMSE, LightGBM-L2 beats the constant by 1.2% / 2.9% / 13.6%, within one bootstrap SD in 2023
     and 2022 (1.9%, 4.2%) (claim auditor).
   - The mean Poisson deviance in dollars is minimised by the mean, as RMSE is, so reserves still add up. Its cost
     grows in step with the dollars, and the top 0.1% hold 14.9% of 2022. The same L2 LightGBM beats the constant by
     18% / 6% / 27% (62,635 vs 76,243; 205,990 vs 219,811; 59,222 vs 80,752) (domain practitioner).
   - Tweedie at power 1.5 (noaa) fits worse here: in 2022 the constant beats every untuned LightGBM.
   - Consistency: the metric reason's own logic ("an event's loss is the sum of the reserves, which the mean
     minimises") is noaa's reason for a deviance from context (Lennart, 2026-11-08). RMSE scores 35 of 88 regression
     definitions, and no insurance claim-amount task uses it (precedent checker).
 Effect. The score of the Ian window, and so the ranking, is set by a few hundred association claims that a desk would
   reserve by hand.
 Rule. MET-1: score the decision, at the unit the actor acts on. MET-11: context when the task makes a metric obvious.
   MET-10: resolution, and diversity when in doubt. Principles, consistent judgement, case 2 (noaa).
 Remedy.
   - Declare mean_poisson_deviance on untransformed dollars from context, with min_prediction set by MET-13's rule
     (noaa: $1). The library already has the metric.
   - At the least, put the noaa consistency question to the curator with these facts (precedent checker, prompt A).
   - Add a note on the one-event windows: Ian holds 98.3% of 2022's squared error and Ida 74.6% of 2021's, and
     rankings flip on the event (split auditor). TP-9's Too Small does not apply, since the spread is there.

6. [P7; CLEAN-10 Should, CLEAN-11 Should] Codes and values that stand for "missing". Quality only, no reason to
   exclude.
 Evidence.
   - foundationType code 0 is on 99.97% of legacy-rated rows and 0% of RE rows: "not collected before RR2.0". It
     covers 58.4% of the rows; the notes say 51% (column and claim auditors; the blind reviewer reads it the same way).
   - Impossible values remain: elevations in a 990-999 ft cluster, 302 BFEs above their state's highest point, an
     elevationDifference beyond +-100 ft on 87 rows, and two coordinates (New Zealand, Manila).
 Remedy. Set foundation "0" to missing before decoding and drop its label (RMSE -63 / -861 / +196, within noise). Mask
   the impossible elevations and coordinates, or note them.

7. [writing.md; USE-8 Must, LEAK-26 Must, SPLIT-20 Should, LEAK-24 Must] Statements the panel refuted.
 - use_case says "no source names this use (ours)". FEMA bulletins W-08095 (2008) and W-10008 (2010) describe the
   initial case reserve as "a system-generated amount based on criteria established by the Company", refined by the
   adjuster's reports. Cite them; the model stays ours. fit_reason names the later-term scope (point 1) and the inputs
   a desk has that are redacted: the property's earlier claims and the first-notice description.
 - SEL-1 note: add the OpenFEMA clause "The data can be used to make decisions on program management". Keep advance
   payments and inspection triage outside the use case: they are individual determinations.
 - LEAK-26: "the coverage caps most claims" is wrong. 48,250 claims (5.9%) are paid exactly a limit, and they hold
   21.2% of the dollars.
 - SPLIT-20: "by 2010 the median building coverage has reached $250,000" is false ($191,200 in 2010; first $250,000 in
   2012). RR2.0 (October 2021) is a break inside the history, and it goes unnamed.
 - LEAK-24: the two-download test was not available (no archive). Say so, and name the 2027 revisit. The 2022 labels
   still move: 3.61% of 2022's dollars are in claims last paid in 2026.
 - causeOfDamage: replace the B/C/D reason (those codes are at most 0.1% of a year) with the measured one. Code 0 has
   38.7% zeros, the 5,831 missing codes are 91.4% zeros, and the field is worth 541 / 3,045 / 1,838 RMSE.
 - Numbers to correct:
   - clerical rows: 4.35% of 2010-2023;
   - one-coverage 98/99 claims kept: 2,276;
   - probe 13 flags 2022Q3 (p90 z +7.0);
   - the equal-size gap test, restated in RMSE: mixed; a gap is 7% better in 2023.

=====================================================================================================================
Rebuttal
=====================================================================================================================
The advocate and I now agree on the core: the keep with a note fails clause 2, and the fix is to re-cut the windows
after the Risk Rating 2.0 changeover. My new measurement on those windows is in the run folder: recut_b.py and
recut_b.log. Setup: the column auditor's frame; untuned LightGBM, 400 trees, bagging 0.8; three seeds on 2022H2 for
the training-side variants, one seed for the Poisson fits. Every number is RMSE unless marked otherwise.
  2022H2, constant 233,758 (paired by seed 0 / 1 / 2):
    base (as shipped)                                            238,645 / 238,756 / 239,389
    A  = option b blank on located rows + rateMethod dropped    239,222 / 238,737 / 239,324   (A - base +577 / -19 / -65)
    A2 = A + occupancy harmonised                               238,093 / 237,967 / 239,326   (A2 - A -1,129 / -770 / +2)
    B  = A, the 14 fields a large loss changes dropped          239,960 / 239,755 / 239,805   (B - A +738 / +1,018 / +481)
  Poisson-objective fit against the constant, 2022H2 / 2023H1 / 2023H2:
    RMSE 240,302 / 77,582 / 69,172 against 233,758 / 77,725 / 73,770
    mean Poisson deviance ($1 floor) 368,948 / 90,397 / 66,470 against 227,913 / 80,869 / 73,668

A1 (the task is real and sourced; SEL-1). Concede. These are the same changes as my point 7.

A2 (the other P4 checks; mild fixes). Concede. One addition: originalNBDate after the loss (24,358 claims) is also a
   located late cell and gets blanked (clause 2). The advocate's point 4 option b covers it; list it in the change so
   it is not lost.

A3 (a real signal on 3 of 3 windows). Dispute in part, on a new fact.
   - Every number the advocate cites is on the shipped windows. They include 2021, which we both now drop and which
     holds the largest gain (-11% to -14%).
   - On the re-cut windows the untuned fits are thin. L2: -2.2% on 2022H2 (worse than the constant, 3 of 3 seeds),
     +1.0% on 2023H1, +7.7% on 2023H2. Poisson objective under the Poisson deviance: worse than the constant on
     2022H2 and 2023H1, +9.8% on 2023H2.
   - Untuned flags are questions (TP-1). The split still wins over the score (P4 over P6; TP-2), so this is no reason
     to keep 2021.
   - But the judgment record cannot say "a small real signal on 3 of 3 windows" for the windows it proposes. The
     task probe with tuned methods runs on the re-cut before the curator decides (TP-1, TP-3).

A4 (later-term block; re-cut). Concede the re-cut and the advocate's table (my counts agree). On the training side:
   (a) Blank the located cells of the fields a large loss changes: concede.
       - Under the re-cut, the located RR2.0 cells are all on training rows: 268,716 of them. In 2022H2 only 1,408
         located test rows remain, all with an NB or construction date after the loss. So the blank cannot carry the
         renewal bit to a test outcome, which was my objection in 2021.
       - It is the clause's own remedy (zillow_prize, melbourne_housing_market).
       - It also cuts the channel through which the residue pays: a model can no longer learn "elevated after a large
         loss, so a large payment" from the located training rows.
       - Measured cost, A against base: +577 / -19 / -65, within seed noise.
   (b) Drop rateMethod: concede. 99.5% of the re-cut test rows are RE, so nothing is lost there; it is in A.
       Harmonise occupancy: dispute as a change to the definition, concede it as no blocker.
       - It is not a leak fix. The scheme stays readable at AUC 0.9987 without these fields (column auditor), and
         under the re-cut the bit cannot reach a test outcome anyway.
       - It is lossy where the test rows live. 96.6-99.5% of them carry RR2.0 codes, and the map merges condominium-
         association buildings (15) with 5+ unit buildings and single units in multi-unit buildings (16) with
         single-family homes.
       - CLEAN-12 (Should): the type follows from the source's context "never from model runs; ... lose no
         information". The advocate's case is the task gamer's H1 score, and that is masking and harmonising
         together on the old windows. Harmonising alone (H1a) gave +32 / +854 / -230.
       - My A2 against A on 2022H2 is -1,129 / -770 / +2: a small gain on 2 of 3 seeds, within about 2 SE.
       - So: a P7 question, kept as the codes; a model may merge them itself.
   (c) The Ian residue "at 0.1% of the window's squared error". Dispute the evidence offered, and its scope.
       - 0.1% is the reach of the ICC rows in the constant's SSE, not a gain. Clause 2 asks about a gain, and ny_wcb's
         mediator set the bar: measured, above 2 SE, with the burden on the keep.
       - The residue is not Ian's alone. The record is the latest term in every window. RR2.0 only made it visible
         before October 2021, and NB dates after the loss still locate 2.6% / 2.6% / 0.6% of the re-cut test rows.
         The note must say this for all windows.
       - What can be measured: the 14 fields a large loss changes, with A in place, are worth +738 / +1,018 / +481 on
         2022H2. That is 0.31%, 3 of 3 seeds, about 4.8 SE. This total includes the legitimate at-loss information,
         so it neither proves the residue a gain nor clears it. The traced part stays the claim auditor's +0.038
         against +0.021 R^2 on the located 2021 rows (one fit, circumstantial).
       - Clause 2 is a case-by-case call of the curator, so I concede that this decision is the curator's. The
         curator should decide it on these two numbers, not on the 0.1%:
         - keep, with a note giving both;
         - or drop the 14 fields, at a measured price of about 0.3% on the Ian window. The default of the clause
           for unlocated values that "may carry a gain" (distribution_transformers_at_cauca_department).
   Fallback (yearly windows with an amendment, decided with ny_wcb issue 2): dispute.
       - The ladder: a fix in the definition exists (the re-cut), so an amendment is not the mildest remedy
         (principles, step 5). A Must has no exceptions.
       - ny_wcb issue 2 offers this amendment as its option (c). Its mediator does not recommend it: "Almost every
         looked-up attribute would qualify, and you declined this on 2026-10-21" (distribution_transformers). Tying
         nfip to it asks the curator to reverse that decision for two datasets at once.
       - The window an amendment would buy back is the one whose gain cannot be told apart from the later term.
         Blanking its located cells takes the model from 72,934 to 78,917, at the constant's 78,745 (column auditor).
         Part of that is legitimate coverage lost with the blank, so this is a caution, not proof.
       - Even amended, 71.8% of the 2021 rows are scored on a scheme no deployment meets at the loss (domain
         practitioner, Q3). SPLIT-1 asks for the split that mirrors the application, and an amendment of LEAK-10 does
         not touch that.

A5 (event-size exploit; LEAK-9). Concede, including the advocate's stricter line: the test rows are not used at all,
   and the count of claims opened so far is noted as a deployment input that the batch protocol leaves out. That is
   simpler for the benchmark to check than my causal count.

A6 (the metric blocks nothing). Concede that it blocks nothing: it is P6, a change to the definition, not an
   exclusion. I narrow my case on a new fact.
   - On the re-cut windows, the Poisson deviance does not resolve better on untuned fits. The Poisson-objective model
     loses to the constant under it on 2022H2 and 2023H1, and RMSE has the L2 model losing on 2022H2.
   - So the resolution argument from the shipped windows does not carry over. My preference for the mean Poisson
     deviance now rests on MET-1 (one dollar of error is one dollar of reserve; condominium associations hold 84% of
     the Ian window's squared error, and Ian 98.5% of 2022H2) and on MET-10's diversity tie-break.
   - Ask: score the tuned probe on the re-cut under both metrics, and let the curator weigh it with those numbers
     (precedent checker, prompt A).

A7 (cleaning, P7). Concede.

Where we stand. We agree on: the re-cut; option b blanking with rateMethod dropped; the rebuilt and NB blanks; the
storm and opened-later filters; the LEAK-9 line; the cleaning; the texts. We differ on:
  - occupancy harmonising (keep the codes);
  - the residue (decide on the measured worth, not the reach, and note it for every window);
  - the fallback (no amendment while a fix exists).
New for the curator: the re-cut's signal is thin on untuned fits, so the tuned probe runs before the decision.
```

</details>
