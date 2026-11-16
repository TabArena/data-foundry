# nyc_motor_vehicle_collisions

**Outcome:** added. NYPD's police crash register on NYC Open Data, 630,838 crashes from 2020-04-06 to October 2026, with "anyone injured or killed" as the target, tested on three later three-month windows; the AI recommends shipping it once the curator, with Andrej, settles the borrowed site-ranking use case against the Thailand rejection (issue 1).

**Main points:** Does the site-ranking analyst borrowed from Chicago hold against Andrej's rejection of the Thailand crash register; Score by ROC AUC or log loss (issue 2)? Drop the house-number address column (issue 3)? The codes-vs-words point (the 12-kind vehicle mapping) and the late-filled values (the blank vehicle type, the backfill) are with the across-datasets items.

**Record fields that disagree with the definition:**

- `year`: record `2012`, definition `2026`.

**Record judgment:** valid with an approximate fit. An official city register with a clear target; the panel found no exploitable leak (the task gamer's best attack gains 0.0017 ROC AUC from address formats a deployed model also sees). The use case is the open question.

**Value:** ROC AUC about 0.74-0.75 against 0.50 for a dummy, at least 8,115 positives per test window.

**Weighed:** large (+), a second city beside Chicago (+), three recording changes in 18 months (-), an approximate fit (-).

**Issues for the curator:**

1. **Does the borrowed site-ranking analyst hold against the Thailand rejection?**

   * **Problem:**
     - The injury flag sits on the same police report as every input, and the use case borrows Chicago's analyst who estimates each crash's chance of injury to rank sites.
     - On 2026-11-03 Andrej rejected the Thailand crash register because once a crash is in the register its outcome is in the same record; the AI had offered him this same site-screening reading and he declined it[^thai].
     - Chicago shipped with the analyst two days later without naming what sets it apart[^chi], so this dataset inherits the unaddressed pair.
   * **Effect on the task:** either two city registers ship on a reading another curator rejected, or the whole family of crash registers is decided one way.
   * **Experiments:** a candidate fact that sets the city registers apart: they hold every reported crash at a site, so the per-site sum of probabilities smooths a rate (empirical-Bayes site screening), while Thailand was read as one count per crash. Its weak point: Thailand also holds mostly non-fatal crashes (87.6% with no death), so the fact may not hold.
   * **Consistency:** treating like cases alike is the rule; rank cannot settle two curators' applications of the same Must[^use1].
   * **Panel:** the blind reviewer, without our notes, named a city-safety analyst, EMS and insurers; the domain practitioner (a DOT Vision Zero analyst) would use it for expected-severity smoothing and says "ship, approximate", but also that there is "no moment at which I hold these inputs and not the label". The critic leans on that and on the Thailand pair; the mediator hands it to the curator.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep the borrowed analyst, add the per-site fact as the exception (implemented) | as shipped: the analyst kept, the fact not yet written; on this option, record that a city register holds every reported crash of a site, so the model smooths a per-site rate | keeps two shipped siblings; names the fact for later registers | the fact may not separate Thailand and is not yet written in the definition; needs Andrej's view |
     | b | Treat like Thailand | `No`, No Good Target, for this dataset | consistent with Andrej's call | reopens chicago_traffic_crashes (Myunghwan's) too |
     | c | Reopen Thailand | the Thailand register gets the site-ranking reading | one stance for the family | overrides another curator's decision |
     | d | Amend the use-case rules with Andrej | write when a register's outcome on the same report still makes a task | settles the family once | slower; a rule change |

   * **Recommendation:** a, if Andrej agrees the per-site fact holds; otherwise d. **Decision:** a, b, c or d?

   **Notes for the AI:** on a, add the fact to `curation_comments` (prediction point bullet) and a USE-1 Cases row; never edit chicago_traffic_crashes (Myunghwan's) or the Thailand record without the curator. On b, set this record to `No` with the Thailand markers; Chicago is not touched; the curator raises it with Myunghwan. Also put the question to Andrej.

   [^use1]: **USE-1** (Must): a use case names an actor, a moment and a decision; **USE-2** (Must): a task no decision fits is out.
   [^thai]: thailand_road_accident_register_2019_2022, CC 2026-11-03, Andrej: `No` + No Good Target, "as glioma_grading" (USE-1 Cases): the model "predicts a count already on file".
   [^chi]: chicago_traffic_crashes, CC 2026-11-05, Lennart, issue 7 (A); USE-9 Cases row.

2. **Score by ROC AUC, as the rule says, or by log loss?**

   * **Problem:**
     - With no metric from the source, binary tasks fall back to ROC AUC[^met8].
     - The stated analyst sums the probabilities per site, which needs calibrated probabilities (probabilities that match the observed rates, so their per-site sum is a usable count), which ROC AUC does not score.
   * **Effect on the task:** ROC AUC ranks models by ordering only; log loss also rewards calibrated sums per site.
   * **Experiments:** no source metric: RaX-Crash (arXiv 2512.07848) reports accuracy, kappa, macro F1 and fatal recall and names no single criterion[^met5].
   * **Consistency:** churn_telco_south_asia kept the fallback; chicago_traffic_crashes' log loss is its multiclass fallback, not a deliberate choice, so there is no pair (precedent checker).
   * **Panel:** the domain practitioner, the claim auditor, the critic and the advocate all lean log loss; the mediator leans log loss but ties it to issue 1: if the analyst goes, so does the reason.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | ROC AUC (implemented) | the fallback | follows the rule; no exception | does not score the calibration the analyst needs |
     | B | Log loss, as an exception | `Metric.from_context("log_loss", ...)` with the reason | strictly proper, rewards per-site sums; Chicago also scores by log loss, though there as its multiclass fallback | an exception, resting on the analyst of issue 1 |

   * **Recommendation:** B if issue 1 keeps the analyst, else A. **Decision:** A or B?

   **Notes for the AI:** on B, declare `log_loss` from context with the reason "the analyst sums the probabilities per site (MET-1)", add a MET-8 Cases row as an exception, re-run `dataset check` and the task probes.

   [^met8]: **MET-8** (Should): with no metric from the source, binary classification is scored by ROC AUC.
   [^met5]: **MET-5**: a source that reports several metrics without naming one leaves the fallback; **MET-1**: the metric serves the use case's decision.

3. **Drop the house-number address column `off_street_name`?**

   * **Problem:**
     - The column holds an address (house number and street) when the crash is not at an intersection: 120,191 distinct values, 71% blank, 87% of sampled values seen once.
     - It is no leak and no row id; the question is whether a near-identifier location belongs in the table.
   * **Effect on the task:** removing it moves ROC AUC by at most 0.004 (with against without: 0.7403 vs 0.7396 in one run, 0.723 vs 0.727 in another, so no consistent direction).
   * **Experiments:** the task gamer finds no exploit in it; the address-against-intersection signal (30% against 53% injured) survives in the missingness of `on_street_name`.
   * **Consistency:** zillow_prize dropped near-identifier location parts (the block group and block, 8,334 and 55,601 levels)[^c14]; width alone is no reason to drop a column[^c22].
   * **Panel:** the column auditor raised it; the mediator leans drop, following zillow_prize.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as text (implemented) | the address stays a string column | information the analyst has | departs from zillow_prize without a stated fact |
     | B | Drop | the column leaves | follows zillow_prize; the signal stays in the other street columns | loses a little text a model could use |
     | C | Has-address flag | a yes/no flag replaces the address | keeps the form signal, no near-identifier | one more derived column |

   * **Recommendation:** B, following zillow_prize. **Decision:** A, B or C?

   **Notes for the AI:** on B, drop `off_street_name` in `_clean` (STREETS keeps on and cross street) and update the notes; on C, add `has_address` as a categorical; then `dataset check` and the leak probes.

   [^c14]: **CLEAN-14** Cases: zillow_prize, 2026-10-26, Lennart: near-identifier parts of a location code dropped.
   [^c22]: **CLEAN-22**: a column is not dropped for its width alone.

**Review panel:** ship after changes, once issue 1 is answered (mediator). Made: the taxi pattern matches LIVERY only as a word (1,259 delivery vehicles were taxis), new-list "Utility" masked to other, the blank-vehicle note rests on its pedestrian mechanism (cost 0.0005 ROC AUC), the factor-drop reading corrected (78% of the gain is the party count), the gap reasoned on measured arrival lags, RaX-Crash named in the metric reason, and notes on the zero coordinates (the 2026-11-06 backfill), the reporting threshold, the borough drift, address against intersection and e-scooter injuries. Claim audit: two wrong rule citations corrected, the numbers hold. Blind review: would benchmark, named a city-safety analyst without our notes. Task gamer: no exploit beyond +0.0017. Debate: advocate and critic converged on the fixes, so the rebuttal round was skipped; disputed: the use case (issue 1), the metric (issue 2), the address column (issue 3).

<details><summary>Mediator</summary>

MEDIATOR REPORT: nyc_motor_vehicle_collisions (2026-11-09)

I did not write the run folder mediator.report.txt, because my role forbids editing files. The full report is below; please save it to that path. I ran no new experiment. The panel's measurements settle every disputed fact except one, which needs the Person-table check described below.

**Summary (15 lines)**
1. Verdict: ship after the changes below, once the curator answers issue 1 (the use-case precedent).
2. No leak can be exploited. The gamer's best attack gained +0.0017 AUC, and it uses address-format signal a deployed model also has.
3. Change now: the taxi rule matches LIVERY inside DELIVERY (1,332 crashes, +0.0014 AUC). Fix it to `\bLIVERY\b` and re-measure the vehicle-mapping check.
4. Change now: map 'Utility' to other/unknown, following the force_2020 rule that an unchecked conversion is masked, not guessed.
5. Change now: keep the blank vehicle type (option A), but rewrite its note. It rests on LEAK-6, not LEAK-38, and the blank marks a pedestrian crash (13.7% of pedestrian-only crashes vs 0.19% of motorist-only).
6. Change now: correct D3 and the notes on why the contributing factors were dropped. 78% of their gain is the party count, and 13.4% of crashes have a factor but no vehicle type.
7. Change now: base the gap reason on the measured arrival lags (median 3-5 d, 99% within 22-48 d; SPLIT-10 as amended), not on Chicago.
8. Change now, text only: name RaX-Crash (arXiv 2512.07848) in the metric reason; correct the reason for the zero coordinates (the 2026-11-06 backfill); fix the PROV-7 cite; write down the selection rule (injury or >= $1000 damage) and the borough-missing drift.
9. Issue 1 (P3, Must): the borrowed site-ranking actor against Andrej's Thailand rejection of 2026-11-03. This is a conflict between precedents, not a rule I can settle, so it goes to the curator.
10. Issue 2 (P6, Should): metric. MET-8 gives roc_auc. log_loss would be an exception backed by the per-site sums (MET-1). Curator call; I lean log_loss.
11. Issue 3 (P7): off_street_name. It is not a leak and not a row id, but zillow_prize dropped near-identifier location parts. I lean drop; the curator decides.
12. Optional: a Person-table check of uninjured pedestrians in the blank-type crashes would confirm the pedestrian mechanism. Run it before a rebuild, not before shipping.
13. No precedent prompt needed for 3 windows (Chicago's 9 is the outlier, SPLIT-15), the era start, the ZIP typing, PROV-9 or the reload.
14. The gamer's exploits are all new. None is a leak; none needs a `Potential leak` note.

**Judgment record**
```text
Verdict: ship after changes (after the curator answers issue 1).
Validity: SEL-1, SEL-2 hold. USE-1 holds as approximate; the actor is borrowed from chicago_traffic_crashes and conflicts with the thailand_road_accident_register_2019_2022 precedent (issue 1, curator). USE-9: the blind reviewer, without our notes, named an EMS/insurer/city-safety analyst; the domain practitioner (DOT Vision Zero) says "ship, approximate".
  LEAK-10 triggered, fixed: injury/death counts and contributing factors dropped (the factor reasoning needs correcting, not the drop). LEAK-13 triggered, fixed: time floored to the hour.
  LEAK-6: blank vehicle type kept, a scene fact (pedestrian crash). Its note moves off LEAK-38.
  LEAK-19 holds (229 copies dropped). SPLIT-6/20 hold (era start confirmed by NYPD p0403b). SPLIT-10: 1-month gap, reason to be rewritten on measured lags. SPLIT-14/15 hold (3 windows).
  PROV-4/7 hold (same task, another source as Chicago; fix the cite). PROV-9, PROV-13 hold.
Value: TP holds (AUC about 0.74-0.75, skill 0.50, >= 8,115 positives per window). MET-8 fallback roc_auc, reason incomplete (RaX-Crash); log_loss is issue 2.
Quality: CLEAN-21 fix the LIVERY regex and 'Utility'. CLEAN-3/CLEAN-14 off_street_name (issue 3). Notes: selection rule, borough drift, zero coordinates.
Weighed: size +, second city +, recording drift - (3 coding changes in 18 months), fit approximate -.
For the curator: issue 1 (USE-1 precedent), issue 2 (metric), issue 3 (off_street_name).
```

**Changes to make now (no decision needed)**
1. CLEAN-21 (a declared mapping whose own check fails): change the taxi pattern to `\bLIVERY\b`. Re-run the vehicle-mapping measurement (D2) and the windows. Today 1,259 delivery vehicles in 1,332 crashes are mapped to taxi after 2026-05-04.
2. CLEAN-21, force_2020 precedent ("masked, not converted"): map new-list 'Utility' (989 vehicles) to other/unknown, not car.
3. LEAK-6: keep the blank vehicle type as missing (option A). Rewrite the `Potential leak, kept on purpose:` note:
   - Cite LEAK-6 instead of LEAK-38, which covers only owner-run competitions.
   - State the mechanism: the blank marks a pedestrian or hit-and-run crash (13.7% of pedestrian-only injury crashes, 0.19% of motorist-only, 0.48% of uninjured).
   - Remove "this table cannot tell".
   - Give the cost of removing the signal: 0.0005 AUC.
   This also closes the precedent checker's Prompt B.
4. Claim honesty: correct D3 and the notes on the factor drop. The filled-slot count, which equals the party count, carries 78% of the gain; it is not "87% fill". Also, 13.4% of crashes have a factor but a blank type, so "blank slot = no further vehicle" is false. The drop still stands. A party count from the Vehicles table remains an option for a later rebuild.
5. SPLIT-10 (amended 2026-11-04/05): base `splits_comment` on the documented amendments ("subject to change when MV-104AN forms are amended") and on the measured arrival lags (median 3-5 d, 99th percentile 22-48 d), not on "follows chicago_traffic_crashes". Mention the 2026-11-06 backfill: 7,855 rows that lean uninjured, 2.7% of 2026.
6. MET-1/MET-11: the metric reason must name RaX-Crash (arXiv 2512.07848). It reports accuracy, kappa, macro F1 and fatal recall and names no single criterion, so MET-5 keeps the fallback.
7. Notes (CLEAN-1 wording, PROV):
   - The lat/lon = 0 rows are the post-reload backfill (7,313 rows), not "not geocoded".
   - Fix the PROV-7 cite.
   - State the selection rule: a report is required when someone is injured or damage is >= $1000, so the model learns P(injury | reported).
   - State the borough-missing drift (35% to 3%, a geocoding change in 2025).
   - Add a fit note: address-only rows are 30% injured against 53% at intersections.
   - Note that 13,908 e-scooter/e-bike injuries appear only in persons_injured, not in the per-role counts. The all-counts target already catches them.

**Issues for the curator (ranked)**

**Issue 1 (P3, Must, validity): the borrowed site-ranking actor against the Thailand rejection**
- **Problem:** the injury flag sits on the same police report as every input. The use case is the Chicago actor: an analyst estimates each crash's chance of injury to rank sites. On 2026-11-03 Andrej rejected thailand_road_accident_register_2019_2022 (`No`, No Good Target, "as glioma_grading") for the same mechanism, and he declined this same site-screening reading. Chicago shipped on 2026-11-05 without naming what sets it apart. NYC inherits the unaddressed pair.
- **Effect:** either NYC and Chicago ship on a reading another curator rejected, or the whole family of crash registers is decided one way.
- **Advocate's best evidence:**
  - Independent USE-9 support: the blind reviewer named a city-safety analyst, EMS and insurers without our notes.
  - The domain practitioner (DOT Vision Zero) would use it for HSM-style expected-severity smoothing.
  - USE-1 allows a "for example" actor.
- **Critic's best evidence:** the domain practitioner also says "no moment at which I hold these inputs and not the label". The Thailand case had the same mechanism and the same offered reading.
- **Rule:** USE-1/USE-2 (Must), and the precedent rule on treating like cases alike. Rank cannot settle a conflict between two curators' applications of the same Must.
- **What would settle it:** a stated fact that sets city registers apart. A candidate: they hold every reported crash at a site, so the per-site sum of probabilities smooths a rate, whereas Thailand was read as one count per crash. The weak point is that Thailand also has 87.6% zero-death rows, so the fact may not hold. Andrej's view is needed.
- **Decision:** choose one:
  - (a) exception with that fact;
  - (b) treat NYC like Thailand, which also reopens Chicago;
  - (c) reopen Thailand;
  - (d) amend USE-1/USE-2 with Andrej.
- **Precedent checker's recommendation:** (a) if the fact holds; otherwise (d).

**Issue 2 (P6, Should, value): metric, roc_auc fallback or log_loss**
- **Problem:** MET-8 gives roc_auc for binary tasks. The stated use case sums probabilities per site, which needs calibration that ROC AUC does not score.
- **For roc_auc:**
  - MET-8 names it.
  - churn_telco_south_asia kept the fallback.
  - Chicago's log_loss is the multiclass fallback, not a deliberate choice, so there is no precedent pair (precedent checker).
- **For log_loss:**
  - The domain practitioner, the claim auditor, the critic and the advocate all lean log_loss: it is strictly proper and rewards the per-site sums (MET-1).
  - It matches Chicago, the sibling with the same actor.
- **Rule:** MET-8 (Should). Choosing log_loss is an exception: the fact is that the actor sums probabilities per site, and it serves P3 (MET-1).
- **Decision:** roc_auc as the rule says, or log_loss recorded as an exception. My lean is log_loss. It depends on issue 1: if the actor goes, so does the reason.

**Issue 3 (P7, quality): off_street_name, drop or keep**
- **Problem:** the column is a house-number address. It has 120,191 distinct values and is 71% blank; 87% of sampled values occur once.
- **What it is not:** a leak or a row id (CLEAN-3 is about row ids). The gamer finds no exploit, and its format signal is deployed signal.
- **Score:** removing it changes almost nothing (0.7403 vs 0.7396, or 0.723 vs 0.727).
- **For drop:**
  - zillow_prize dropped near-identifier location parts (CLEAN-14 Cases, 55,601 levels).
  - The address-vs-intersection signal survives in on_street_name's missingness.
- **For keep:** CLEAN-22 says width is no reason to drop a column, and an address is information the analyst actually has.
- **Decision:** drop, keep, or replace it with a has-address flag. My lean is drop, following zillow. Keeping it needs a stated fact that sets it apart from zillow.

**Open across datasets (kept for the review page, as the curator asked)**
- Codes vs words: the 12-kind vehicle mapping (draft issue 2; A recommended, after fix 1).
- Late-filled values: the blank vehicle type and the backfill.

**Builder's draft issues that are now settled**
- Draft 4 (gap): one month, by measured lags (change 5).
- Draft 5 (3 windows): follows SPLIT-15; Chicago's 9 is that dataset's own departure.
- Draft 6 (recording changes): a weighing factor only.

**Agreed facts**
- 630,838 crashes from 2020-04-06. The era start follows NYPD release p0403b (weekly injured share 0.19 to 0.29).
- dataset check: 0 errors, 0 warnings. LightGBM AUC about 0.74-0.75 and beats the dummy in 3 of 3 windows.
- No leak can be exploited:
  - The gamer's best attack gains +0.0017 (address formats, deployed signal).
  - 0 exact test copies in training.
  - A classifier telling train from test reaches AUC 0.54-0.57, driven by places, not the label.
  - The hour floor leaves no residual timing signal.
- The LIVERY-in-DELIVERY bug: 1,259 vehicles, 1,332 crashes, +0.0014 AUC.
- Blank vehicle type: 9,378 crashes, 80.6% injured. It is a pedestrian-crash marker (13.7% vs 0.19% vs 0.48%). Removing its signal costs 0.0005 AUC.
- Of the factors' gain, 78% is the party count. 13.4% of crashes have a factor but a blank type.
- Gap: arrival lag median 3-5 d, 99th percentile 22-48 d. Gap 0 vs 1 month differs by 0.0005. 9 windows add nothing (the spread comes from season).
- off_street_name: removing it moves the score by at most 0.004.
- Borough missingness drifts from 35% to 3%. The zero coordinates are the 2026-11-06 backfill.
- RaX-Crash (arXiv 2512.07848) exists and fixes no single metric.
- Dropping the absolute time column helps an honest model (+0.0023). That is a modelling choice, not a flaw in the task.

**Task gamer exploits mapped to rules**
All are new. The definition's only `Potential leak, kept on purpose:` note covers the blank vehicle type, which the gamer did not attack. None of these is an issue:
- Address-format features, +0.0017: LEAK-13 (recording form), known at the report, so deployed signal.
- Counts over train and test together, 0: LEAK-30 (transductive), none.
- Exact copies across the split, 0: LEAK-18/19.
- Row order, none: LEAK-17 (order).
- Late labels at the end of training, none: SPLIT-9/10.
- The absolute time column hurts honest models: not a rule matter.
- The source lookup (a join on the public API recovers the label): the accepted public-source exposure common to every public dataset; not ranked.

**Consistency with precedent**
- **Follows:**
  - chicago_traffic_crashes: era break, reload treatment, PROV-9 year, copies rule, "same task, another source".
  - ZIP as a category: house_sales and others.
  - force_2020 mapping method, once 'Utility' is masked.
  - churn_telco_south_asia: roc_auc fallback.
- **Departs, resolved by the changes above:**
  - Blank-type keep under LEAK-38: moved to LEAK-6 with its mechanism (change 3).
  - Gap justified by Chicago: rebased on measurements (change 5).
- **Departs, unresolved:** the Thailand pair (issue 1). log_loss, if chosen, is an exception (issue 2). Keeping off_street_name departs from zillow_prize (issue 3).
- **Chicago's own departure:** its 9 windows depart from SPLIT-15. NYC needs no change; Chicago would need an issue of its own if the curator wants the two siblings alike.

Files: panel (the run folder) ; definition (the run folder)

</details>

<details><summary>Claim audit</summary>

CLAIM AUDITOR: nyc_motor_vehicle_collisions (df-large, 2026-11-09)

Verdict: ship after small fixes. No validity claim is refuted in a way that blocks the task. Refuted:
(a) one cleaning bug: "Delivery Truck" is mapped to taxi;
(b) the reading of the factor drop: 78% of the factors' gain is a count of parties, and the dataset says a blank vehicle slot means no further vehicle, which is false for 13.4% of crashes;
(c) the blank-vehicle-type mechanism: "this table cannot tell" is wrong, it can, and the answer is a pedestrian marker, not recording by outcome;
(d) the metric reason, which misses a paper.
Everything else holds or is minor.

Scripts and caches: the run folder  (a1-a7.py, a5.json, raw.parquet and era.parquet hold the raw rows).
Model: untuned LightGBM, as the builder's measure.py (400 trees, 63 leaves), on the three shipped windows with a 1-month gap.
My base reproduces the shipped 0.7361 (builder 0.7365).

TABLE (claim | source | test | result | evidence | rule)

C2/C3/C10 era from 2020-04-06 | task_summary.row, notes | NYPD press release p0403b; weekly injured share around the date | HOLDS | release: effective Mon 2020-04-06, PDO not reported; police still come for injury, feels-unsafe, owner not found. Weekly share 0.187-0.198 (3 weeks before) -> 0.291 (week of 04-06), 0.23-0.38 later | SPLIT-6, SPLIT-20
C9 19-23% before, 25-36% after | notes | monthly shares | HOLDS | pre-era months 0.191-0.232; Apr-Dec 2020 months 0.256-0.360
C11 COVID weeks 826-1,579 vs 3,000-3,800 | notes | weekly counts | HOLDS | 826 (wk 04-06) to 1,579 (wk 05-25); Feb-early Mar 2,995-3,778
C4/C13 33.7% (2020) vs 47.6% (newest window) | task_summary.predicted | shares | HOLDS | 0.337 / 0.4763
C14 counts disagree in 14,370 rows | notes | persons_injured != sum of parts | HOLDS (numbers), WEAK reasoning | 14,370 (+1 null row); persons_killed != parts in 132 rows. But "any of 8 > 0" and "persons injured or killed > 0" differ in only 1 row (the null one), so the disagreement never changes the binary target | USE-5
C15 one row without persons-injured | notes | null count | HOLDS | 1
C12 snapshot ends 2026-11-03 | notes | max crash_date | HOLDS | 2026-11-03
C25 hour floor (LEAK-13) | notes | minute :00 by class, per hour; 00:00 placeholder | HOLDS | :00 is 19.93% of uninjured vs 12.33% of injured. Injured share at minute 0 is lower in every hour 1-23 (e.g. 12h: 0.258 vs 0.403). The 00:00 placeholder is class-neutral (1.82% vs 1.66%; hour-0 share 0.378 vs 0.388), so the floor leaves no residual | LEAK-13
C16/C17/C43 factors dropped, unspecified 52.6% vs 29.9% in single-vehicle crashes | notes, D3 | recount by party; split by injury type | HOLDS in conclusion, table MISLEADING | D3 counts vehicles by typed slots. 72,767 "single-vehicle" crashes carry a factor 2 (an untyped second vehicle), and only 15.1% of them are injured. Counted by party (a slot with a type or a factor), single-party crashes show 69.1% vs 29.1%, so the gap grows. Within single vehicles: motorist-only injuries 34.4%, uninjured 52.6%, so the gap is not only crash type. Two parties: 29.9% vs 27.3% | LEAK-38 measured clause -> LEAK-10
C18 fill flags give 87% of the +0.068 gain | notes | decompose the flags | NUMBERS HOLD, READING REFUTED | base 0.7361; 3-level state 0.7957; blank/non-blank only 0.7836; named/not-named only 0.7799; number of factor slots filled alone 0.7831. So +0.047 of the +0.060 (78%) is how many parties the report lists, which is not the officer's judgement. "Named vs not" alone is +0.044 (overlapping) | LEAK-38, CLEAN-22
(implied) "A blank slot means no further vehicle" | notes, vehicle bullet | factor present while type blank | REFUTED | 84,807 crashes (13.4%) have a factor in a slot whose type is blank, 11.6% in slot 2. Typed-single crashes with a factor 2: 72,767, 15.1% injured; without one: 131,698, 46.9% injured. Typed-single crashes with factor 2 by year: 0.32-0.36 (2020-2025), 0.464 in 2026 (drift) | CLEAN-22, LEAK-13
C19 "Does Not Apply" from April 2025 | notes | not re-run (builder's factor_vocab_by_month.json) | UNTESTED (out of scope: factors dropped) | -
C20 vehicle codes switch in the week of 2026-05-04; 48/44 distinct vs 137-187 | notes | weekly Sedan vs "4 dr sedan" counts | HOLDS | "Sedan" 743 -> 134, "4 dr sedan" 24 -> 606 in the week 05-04. Distinct slot-1 values: 2026Q3 48, Q4 44; 2025Q1-2026Q1 137-163; 2026Q2 119 (the switch quarter)
C21 12 kinds, taxis, buses etc. kept apart | notes, VEHICLE_CATEGORIES | which raw codes land in each kind | REFUTED | the taxi regex "LIVERY" matches "DELIVERY". 1,350 delivery vehicles become "taxi or limousine": 1,259 "Delivery Truck" in the new list (1.7% of new-list vehicles, 505 in slot 1) and 91 old free-text codes | CLEAN-21
C42 D2: kinds keep their shares across the switch | Decision 2 | kind shares, May-Oct 2025 vs 2026 | REFUTED for taxi | taxi or limousine 2.64% -> 3.49% (+32%). Moving the delivery codes to truck or van gives AUC 0.7375 vs 0.7361 (+0.0014; windows +0.0023/+0.0018/+0.0001) | CLEAN-21
C22 truck-or-van 8.5% vs 8.1% | notes | shares | HOLDS | 0.0852 / 0.0808 (it would be about 9.8% with the delivery trucks)
C23 raw codes 0.656 vs 0.742 | notes | builder measure.py | HOLDS (taken from the builder's run; my harmonised base matches) | -
(untested) "Utility" = SUV | notes | - | UNTESTED | the new list also has "Station Wagon/Sport Utility Vehicle" (11,257 in slot 1), so "Utility" (544) may be a utility truck. Needs the code list | CLEAN-21
C26 blank vehicle type: 9,378 (1.5%), 80.6% injured; "this table cannot tell" whether it is recording or a pedestrian crash | notes, fit_reason | blank share by injury type | NUMBERS HOLD, MECHANISM CLAIM REFUTED | blank in all slots: 13.7% of pedestrian-only injury crashes, 0.00% cyclist-only, 0.19% motorist-only, 0.48% uninjured. If officers skipped the type on injury reports, motorist-only injuries would show more blanks than the uninjured; they show fewer. So the blank marks a pedestrian crash, a scene fact. Its rate drifts 0.84% (2020H1) -> 1.82% (2026). Replacing it with "unknown" in slot 1: AUC 0.7356 vs 0.7361 (-0.0005) | LEAK-6, LEAK-13
(rule scope) "Potential leak, kept on purpose" via LEAK-38 | notes, builder issue 1 | read LEAK-38 | REFUTED as cited | LEAK-38's keep clause covers data the owner released for its own competition; NYC Open Data is not one. With the test above, the rule that decides is LEAK-13/LEAK-6 (no class-specific recording found), not a LEAK-38 keep | LEAK-38
C27 coordinates 0: 7,286 rows, the only values outside the city | notes | count; range of non-zero values | HOLDS in substance, COUNT OFF | 7,274 in the era (7,273 after copies are dropped; 7,634 in all downloaded rows). Non-zero lat 40.499-40.913, lon -74.255 to -73.700; missing by class 7.41% vs 7.23%
C28 borough blank 30-35% to 2024Q3, about 3% from 2025Q2 | notes | by quarter | HOLDS | 0.30-0.36 to 2024Q3, 0.21-0.22 in 2024Q4-2025Q1, 0.067 in 2025Q2, 0.029-0.036 after. Class-neutral in 2026 (3.2% vs 2.9%)
C29 229 exact source copies; 434 reduced duplicates, 152 across labels | notes | recount on raw and on the container | 229 HOLDS; 434/152 WORDING | 229 copies, spread 6-31 per quarter. In the container, 586 rows repeat another row's 13 inputs, 152 input groups carry both labels, and 586 - 152 = 434. The note's "434 rows; 152 share their inputs with a row of the other label" suggests the 152 are among the 434. Exact input copies of newest-window test rows in train: 0.0% | LEAK-18, LEAK-19
C30/C32 reload of 2026-10-29: hash ids, update times reset | notes | :created_at/:updated_at dates; collision_id | HOLDS | 873,319 of 883,059 rows created and updated 2026-10-29; the rest 2026-10-30 to 11-06; collision_id is 32-char hex, unique | PROV-13
C35 / builder issue 4: one-month gap, delay unmeasurable | splits_comment | look for a missing-injury deficit in the newest weeks (late injuries would lower them) | PARTLY REFUTED ("unmeasurable") | weekly share Oct 2026 0.468-0.482 vs Aug-Sep 0.464-0.488; monthly Aug/Sep/Oct 2026 0.475/0.475/0.478, no dip at the snapshot edge. So no late injury flips are visible. The gap is harmless and follows the precedent, but the data does not call for it | SPLIT-10
C6/C34 split: 3 x 3 months, train 560,737-602,337 | splits_comment | container splits | HOLDS | train ends 2026-06-30 / 03-31 / 2025-12-31 (gap 1 month), test 21,559 / 21,849 / 19,923 rows with 10,268 / 10,208 / 8,115 positives | SPLIT-14
C37 drift, January-February dip (35.5% in Feb 2026) | splits_comment | monthly shares | HOLDS | Feb 2026 0.355; 2025-06..2026-10 0.355-0.478. Note: the oldest test window (Feb-Apr 2026) sits in the dip, 40.7% positive vs 47% | SPLIT-20
C33 PROV-7 against chicago_traffic_crashes | notes | read chicago's dataset.py | HOLDS in substance, WRONG RULE | Chicago: 5 KABCO levels, from 2017-09, a 1-month gap measured from :updated_at (99.4% within 30 d), factors/conditions dropped under the same LEAK-38 clause, hour floor in _clean. Distinct city and target, so not a duplicate. But PROV-7 is about records that share a source; two cities are "same task, another source" (principles.md Tensions) | PROV-7
C5 13 inputs | known | feature_columns(c) | HOLDS | 13: datetime, borough, zip, lat, lon, 3 streets, 5 vehicle slots
(implied) streets known at the report, filled the same way by class | - | null share by class | UNTESTED mechanism | on_street null 35.1% (uninjured) vs 18.4% (injured); off_street (address) null 64.9% vs 81.6%. Injury crashes are written at intersections, the others at addresses. This may be a scene fact (intersections are more dangerous) or a recording convention; the builder's missing-indicator probe gives at most 0.523 | LEAK-13
C38 metric fallback roc_auc; "no competition or paper defines one" | metric reason | look again (MET-1) | FALLBACK HOLDS, REASON REFUTED | RaX-Crash (arXiv 2512.07848, 2025) models NYC injury severity in 3 classes (none/injury/fatal) with a temporal holdout. It reports accuracy, Cohen's kappa, macro F1 and fatal recall and names no criterion, so MET-5 gives the fallback, but the reason must name it and list its metrics | MET-1, MET-5, MET-11
(MET-2) computable on every fold | - | scorer(c) on a constant 0.5 and on a ramp | HOLDS | constant 0.5 = 0.5 on all three folds; positives 8,115-10,268; no scoring columns needed
(MET-1/MET-8) the metric fits the use case | use_case | read | WEIGH | the analyst "estimates expected injury crashes at each site", a sum of probabilities, so calibration matters. ROC AUC ignores calibration; log_loss would score that decision more directly. MET-8 allows roc_auc as the binary fallback | MET-1, MET-8
C39/C40 metadata, sha256, 883,059 rows | download_description | row count | HOLDS (rows) | 883,059 rows, 95 files. sha256 not recomputed
C1/C7 use case borrowed from Chicago | task_summary | - | UNTESTED here (blind reviewer's question) | USE-1

REFUTED / UNTESTED, RANKED (validity first)

1. [P4/P7, Should; CLEAN-22, LEAK-38 reading] The factors' gain is mostly a count of parties, and "a blank slot means no further vehicle" is false.
   What: 78% of the factor gain (+0.047 of +0.060) comes back from the count of filled factor slots alone. 13.4% of crashes have a vehicle whose type is blank but whose factor slot is filled (72,767 "single-vehicle" crashes, 15.1% injured vs 46.9%). The shipped data presents them as single-vehicle crashes. These are likely parked or departed vehicles (the post-2020 "owner cannot be found" exception), a scene fact the drop throws away. Their share jumps to 46.4% in 2026.
   Changes: the D3 table's vehicle counts; the bullet "A blank slot means no further vehicle"; the claim that the factors' gain is officer fill.
   Mildest remedy: correct the two notes. Open a curator issue: A, keep as is (with the corrected note); B, add a "parties on the report" count (slots with a type or a factor) after checking against the Vehicles table that the untyped vehicles are parked; C, leave it to a Vehicles-table variant. The drop of the factor values stays justified: by party, single-party unspecified is 69.1% vs 29.1%.
2. [P7, Should; CLEAN-21] Delivery trucks are mapped to taxi.
   What: VEHICLE_CATEGORIES matches the taxi pattern "LIVERY" before the truck pattern, so "DELIVERY ..." becomes "taxi or limousine": 1,350 vehicles, of them 1,259 "Delivery Truck" in the new list. D2's "kinds keep their shares" fails for taxi (2.64% -> 3.49%). The fix gains +0.0014 AUC.
   Mildest remedy: write `\bLIVERY\b` (or move the truck pattern before taxi); re-run D2 and the 8.5%/8.1% numbers.
3. [P4, Must-adjacent; LEAK-13/LEAK-6; builder issue 1] Blank vehicle type: the mechanism is testable, and the test points to a pedestrian marker.
   What: blank is 13.7% of pedestrian-only injury crashes, 0.19% of motorist-only, 0.48% of uninjured, and neutralising it costs 0.0005 AUC. The "Potential leak, kept on purpose" note (LEAK-38 keep, which covers competition data only) is the wrong frame.
   Mildest remedy: keep it (option A), and rewrite the note and fit_reason as a tested scene fact with these numbers.
4. [P6, Must (MET-1/MET-11 reason)] The metric reason says no paper; RaX-Crash (arXiv 2512.07848) exists. The fallback stays under MET-5. Add it to the reason, with its metrics. Weigh log_loss for the expected-count use case (MET-8).
5. [P4, Should; SPLIT-10] "Delay unmeasurable" is too strong: the newest weeks show no injury deficit (Oct 2026 0.478 vs Aug/Sep 0.475). Keep the 1-month gap by precedent; add this check to splits_comment.
6. [P5; PROV-7] Wrong rule cited: Chicago is another source, not a shared one. Cite principles.md "same task, another source"; the conclusion is unchanged.
7. [Notes] Small number fixes: zero coordinates are 7,274 in the era (7,273 shipped), not 7,286. The 14,370 count disagreements change the target in 0 rows, so say "harmless", not "so the target reads all eight". 586 rows repeat inputs (434 with the same label, 152 groups with both).
8. UNTESTED: "Utility" as SUV (the new list has a separate SUV code). Street-name fill by class (intersection vs address, 18.4% vs 35.1% on_street blank) as scene vs recording. Factor vocabulary change (C19). The use case (blind reviewer).

Sources: NYPD press release https://www.nyc.gov/site/nypd/news/p0403b/nypd-expanding-successful-non-injury-collision-pilot-save-nypd-resources ; RaX-Crash https://arxiv.org/abs/2512.07848 ; data dictionary source/MVCollisionsDataDictionary_20190813_ERD.xlsx.

</details>

<details><summary>Column audit</summary>

COLUMN AUDITOR: nyc_motor_vehicle_collisions (2026-11-09)
Verdict: ship after one cleaning fix (Delivery Truck mapped to taxi). No column is a leak to drop. Two questions for the curator.
Scripts and cached frames: the run folder  (a1-a8.py; raw.pkl, clean.pkl built from the definition's _load_raw/_clean on the pinned snapshot).
Codebook: source/MVCollisionsDataDictionary_20190813_ERD.xlsx (Column Info sheet). Prediction point: report filed, before the injury counts are read.

COLUMN TABLE (column | meaning | known at prediction? | dtype and cleaning | verdict | rule)
crash_datetime | ACCIDENT_DATE + ACCIDENT_TIME, when the crash happened | yes | datetime, floored to the hour. Exact 0:00 (1.8% of rows, 37.8% injured vs 40.0%) and :30 heaping (11.8% uninjured vs 8.7% injured) fall inside the hour. Inside hour 0 the midnight flag scores AUC 0.492 on the test windows, so the floor removes it | fine | LEAK-13
borough | borough where the crash happened | yes (a place). The 2025Q2 fill only goes forward: 30-35% blank to 2024Q3, 21% in 2024Q4-2025Q1, 3% from 2025Q3. Old rows were not backfilled at the reload | categorical, 5 levels, upper-cased | fine, drift noted. Blank-borough AUC 0.497-0.4995 on the 3 test windows. Before 2025 a blank borough is 3-5 points more often injured (highway crashes, e.g. BELT PKWY, are not geocoded to a borough): a scene fact, not the outcome | LEAK-10 ok; CLEAN-21 optional
zip_code | postal code of the crash | yes | categorical, 230 codes; the dtype probe flags numeric_levels, answered: a code (CLEAN-14). Blank 19-27% from 2025, rising in 2026; blank-ZIP AUC 0.519-0.527 on test | fine | CLEAN-14
latitude, longitude | WGS84 position | yes | float. 0 made missing (7,273 era rows; 7,286 in the raw download) | fine, note to correct (below). Every in-era zero row was created after the reload (created_at 2026-10-30..11-06; 0 zeros among rows from the reload). Most came in one batch of 7,313 rows on 2026-11-06 spread over 2020-2026, 35.3% injured vs 40.0%. Coords-missing AUC 0.495-0.497 on test | LEAK-13 weak, CLEAN-10
on_street_name | street of the crash | yes | string, upper-cased, USPS words. No raw format signal is left: lower-case raw spelling AUC 0.5002, and no unabbreviated STREET/AVENUE remains | fine (location pattern: Q2 below) | CLEAN-21
cross_street_name | nearest cross street | yes | string, same cleaning | fine | CLEAN-21
off_street_name | street address if known (house number + street) | yes | string, 120,191 distinct. 21.7% of the raw values had padding spaces; the normalisation collapses them | fine | CLEAN-21
vehicle_type_code1..5 | type of each vehicle on the report (dictionary: ATV, bicycle, car/suv, ebike, escooter, truck/bus, motorcycle, other) | yes (a scene fact on the report) | categorical, 12 kinds. Bug: "Delivery Truck" goes to "taxi or limousine" (below). Only 3 rows have slot 1 blank with a later slot filled. No empty strings in the raw data | cleaning problem (slots), leak question (all blank) | CLEAN-21; LEAK-6/LEAK-10
anyone_injured_or_killed (target) | any of the 8 counts > 0 | outcome | "No"/"Yes", Yes = the event. 0 negatives, 1 NaN (persons injured). The counts disagree in 14,456 of the cleaned rows (the claim's 14,370 is for the raw download; my raw count is 14,493 because it counts the NaN row as a disagreement). In 13,908 rows persons injured > 0 while every part is 0, from 2021 on (none in 2020). Those crashes involve e-scooters (47.9%), e-bikes (40.8%) and mopeds (11.6%), against 1.5-2.1% overall: riders of those vehicles are counted in neither the cyclist nor the motorist count. Reading all eight counts is right; reading the parts alone would lose 2.2% of the positives | fine | USE-5, CLEAN-25
Dropped: the 8 counts (the target and its parts), the 5 contributing factors (fill measured by outcome: LEAK-38's measured clause sends them to LEAK-10), collision_id/:id/:created_at/:updated_at (ids and reload metadata; :created_at would have marked the late batch), location (not downloaded) | all outcome-side or ids | drops correct | LEAK-10, CLEAN-22

PROBLEMS, RANKED (principles.md order: P4 leaks before P7 cleaning; severity noted)

1. [P4, question] Blank vehicle type in every slot (9,378 rows, 1.5%, 80.6% injured). The keep cites LEAK-38, but LEAK-38 only covers fields whose timing cannot be tested, in data released for its owner's own competition. This is a city register, so the keep rests on LEAK-6 (a small optimism with a note: the blank alone scores AUC 0.513).
   Facts:
   - 77.2% of the blank crashes have an injured pedestrian, against 8.5% overall; 13.5% of all pedestrian-injury crashes have no vehicle type.
   - The UNKNOWN code is used in another way. In slot 2 it is 8.7% injured (705 rows); a lone UNKNOWN vehicle is 60% injured (35 rows).
   - Plausible scene mechanism: a hit-and-run vehicle whose type nobody saw.
   The builder says "this table cannot tell". The Person table can, though: it lists uninjured people too (VICTIM_INJURY includes "unspecified"). So test C is cheap: query Person (f55k-p6yu) for pedestrians present in the blank crashes without an injury. If they are there (pedestrian contact with no injury), the blank is a scene fact and stays. If the blank never occurs on uninjured pedestrian reports, it is recording by class: make it missing-equivalent to "unknown", or drop under LEAK-10.
   Mildest remedy now: fix the note's rule citation (LEAK-6, not LEAK-38) and add the Person-table test to the revisit line.
2. [P7, Should; a clear bug] CLEAN-21: the taxi pattern r"TAXI|^CAB$|LIMO|LIVERY" matches "DELIVERY". New list:
   - 1,259 "Delivery Truck" vehicles (1.7% of the vehicles after 2026-05-04) become "taxi or limousine". In 1,242 of the 2,487 crashes with a taxi-kind vehicle after the switch, that vehicle is a delivery truck.
   - The old list had "DELIVERY T"/"Delivery"/"DELIVERY" (44 codes) the same way. In all, 1,332 crashes are affected.
   - Decision D2's table shows it: taxi or limousine 2.36% (old) vs 3.49% (new).
   This touches both test windows after the switch.
   Remedy: anchor the pattern, e.g. r"TAXI|^CAB$|LIMO|\bLIVERY", so that "Delivery Truck" falls to the truck rule (DELIVERY is already in it). Then re-measure D2, and update the curation note's truck-or-van shares (8.5% vs 8.1%) and the AUCs.
3. [P7, question] "Utility" (989 vehicles, 1.3% of the new list) is mapped to car. The new list also has "Station Wagon/Sport Utility Vehicle" (18,725) and "Utility Task Vehicle" (269, mapped to other) as separate codes, so a separate "Utility" code more likely means a utility-body truck than an SUV. The builder listed this as not checked. Remedy: map new-list "Utility" to truck or van, or leave it with a note. "Police Vehicle" (1,016) as car is consistent: the old list coded police cars by body type. "Hearse (Ambulance)" (19 vehicles) lands in "ambulance or fire"; this is trivial, map it to car or other. The truck+van+pickup merge is justified by D2 and needs no change.
4. [P4, weak, note only] Coordinates of 0: the curation note says 0 "marks a crash that was not geocoded". In this snapshot it marks rows inserted after the reload: 100% of the in-era zero rows. In the test windows they are 2.3-2.5% of rows, injured less often, but the coords-missing AUC is 0.495-0.497. Keep them missing and amend the note: the batch of 2026-11-06 (7,313 rows, all years), 35.3% vs 40.0% injured. The batch also means a later download will differ beyond daily amendments (PROV / download_description).
5. [P3/P4, question, weak] Location form: address-only rows (off_street set, on/cross blank; 32% of test rows) are 30.2% injured, against 52.7% at an intersection. On test, on_street present alone scores AUC 0.598, the strongest single input. Either it is a scene fact (driveways, parking lots, low speed), or it is how the report was taken (reports taken at the precinct with an address, against an officer dispatched to an injury crash who writes the intersection). Both are known when the report is filed, so this is no leak at this prediction point. It is a fit point for USE-8: it is what the analyst sees.
6. [P7, optional] Borough means different things over time: blank 30-35% before 2024Q4 (mostly not geocoded or highways), 3% after. It could be filled from the coordinates for the old era (CLEAN-21, one scale). It does not predict on test; the drift note is enough.

No finding: hour floor (LEAK-13 fixed), street normalisation (no residual format signal), ZIP typing, target definition, dropped columns.

</details>

<details><summary>Split audit</summary>

SPLIT AUDITOR - nyc_motor_vehicle_collisions (full version), 2026-11-09

VERDICT: right with notes. Keep the shipped split: temporal, era from 2020-04-06, 3 windows of 3 months, gap of 1
month, expanding train side. None of the alternatives changes the score or the ranking beyond noise. The notes are
about how the gap is justified and about adding the measured numbers to splits_comment.

Method. Same frame as the definition (the column auditor's _clean output, 630,838 rows), LightGBM set up as
measure.py (400 trees, lr 0.05, 63 leaves), ROC AUC. I rebuilt the windows by hand and they match the shipped
ones exactly: train 602,337 / 580,759 / 560,737, test 21,559 / 21,849 / 19,923, and AUC 0.7479 / 0.7426 / 0.7188
against the builder's 0.7477 / 0.742 / 0.7197. Designs run: 9 quarterly windows back to Aug 2024 under gap 1
(shipped design, extended), gap 0, gap 0 at the gap-1 train size, train from 2020-07-01, LightGBM without the 7
place columns, and a one-hot logistic regression. Scripts and output:
windows.py, windows.json, windows.log.

AUC per window (newest first; window start date):
  window      gap1  gap0  gap0eq  from07  noloc  logit   pos   n_train (frac)
  2026-08     .7479 .7480 .7481   .7471   .6873  .7056   .476  602,337 (.955)  shipped
  2026-05     .7426 .7427 .7431   .7436   .6918  .7119   .467  580,759 (.921)  shipped
  2026-02     .7188 .7190 .7196   .7202   .6597  .6807   .407  560,737 (.889)  shipped
  2025-11     .7235 .7245 .7248   .7231   .6628  .6732   .420  538,679 (.854)
  2025-08     .7467 .7470 .7468   .7472   .6910  .7096   .461  516,742 (.819)
  2025-05     .7393 .7399 .7390   .7390   .6881  .7041   .444  494,703 (.784)
  2025-02     .7159 .7175 .7175   .7161   .6650  .6791   .417  475,205 (.753)
  2024-11     .7116 .7125 .7137   .7120   .6678  .6689   .437  452,440 (.717)
  2024-08     .7364 .7357 .7357   .7364   .6907  .7003   .458  429,470 (.681)
  mean of 3 shipped windows .7365; next 3 .7365; oldest 3 .7213; all 9 .7314 (sd .014)

FINDINGS (ranked by principles.md; all P4)

1. The gap's stated reason is borrowed and partly wrong; a measured reason exists (SPLIT-10, amended 2026-11-05:
   measurements decide). Note, not a fix.
   - splits_comment justifies the month by chicago_traffic_crashes' precedent and the 30-day death rule. A death
     never flips this target. A later injury report would flip it, but the reload (every row created 2026-10-29
     17:00-19:00 UTC) leaves no amendment history, so label flips cannot be sized. No earlier snapshot exists:
     the two trial monthly downloads (in the run folder) were downloaded 1.5 h before the main pull and add nothing.
   - What CAN be measured is when rows arrive. The source's :created_at for rows added after the reload (9,740
     rows, in daily batches 10-30, 11-03, 11-04, 11-05) puts new crashes a median 3-5 days after the crash, the 90th
     percentile at 7-13 days and the 99th at 22-48 days. A refit at a window's start therefore misses part of the
     last 1-2 weeks, and a one-month gap covers 99% of that.
   - A separate batch on 2026-11-06 added 7,855 crashes dating from 2019-01 to 2026-11 (median lag 695 days). None
     has a twin on date + time + coordinates + streets + vehicles, so these are late additions, not rewrites. They
     are 2.7% of 2026 rows and 2.2% of 2025 rows, and they lean uninjured: 0.358 injured in 2026 against 0.446 for
     all of 2026. Late-arriving crashes are therefore mildly selected by outcome, and they arrive months to years
     late, beyond any gap.
   - What the last month adds: gap 0 minus gap 1 is +0.0005 AUC on average over 9 windows (-0.0007 to +0.0016), and
     +0.0006 at equal train size. There is no shortcut (no crash recurs, so SPLIT-9 has no entity link) and no
     growth toward the release end (+0.0001 in the newest window).
   - Remedy (mildest): keep gap=1. Rewrite the reason in splits_comment: rows arrive a median 3-5 days after the
     crash (99% within 22-48 days, daily batches after the reload); gap 0 against 1 is +0.0005 AUC; late backfills
     (2.7% of 2026, 36% injured) are not covered by any gap; label amendments cannot be measured. Drop the
     death-within-30-days argument, or say it does not apply to this target. Gap 0 would also be defensible
     (SPLIT-10's "no measurable effect"), but the arrival delay is real and the month costs about 3.5% of the
     train side. Either is fine; the curator can choose.

2. Three windows against Chicago's nine, and whether the windows measure coding drift (SPLIT-14, SPLIT-15,
   SPLIT-20; builder issues 5-6). No change needed.
   - The three shipped windows, all after the April 2025 factor change and two after the May 2026 vehicle-code
     switch, score the same as the three before them: 0.7365 against 0.7365.
   - The spread follows the season, not the coding:
       Aug-Oct: .7479 (2026), .7467 (2025), .7364 (2024)
       May-Jul: .7426, .7393
       Feb-Apr: .7188, .7159
       Nov-Jan: .7235, .7116
     The low windows are the winter ones, where the injury share dips to 0.407-0.437.
   - Over 9 windows: sd 0.014 against a range of 0.029 over the 3 shipped windows. LightGBM beats the logistic
     model in all 9 windows (+0.031 to +0.050), and dropping the place columns costs 0.046-0.059 in every window.
     The ranking of designs and models is the same on 3 or 9 windows.
   - The vehicle-code switch is absorbed by the harmonisation (CLEAN-21). The builder's raw-code check, 0.656 in
     the May-Jul window, is the counterfactual and is no longer present.
   - Nine windows would all pass SPLIT-14 (oldest train side 68%) and are Chicago's choice. Here they add compute
     and no information. SPLIT-15 at 630k rows gives 3.
   - Remedy: none. Optionally state in splits_comment that the shipped windows score like the year before
     (0.7365 vs 0.7365) and that the spread is seasonal. The 3 windows cover Feb-Oct. The Nov-Jan season (the
     lowest scoring together with Feb-Apr) is untested, which is acceptable because SPLIT-20 asks that most windows
     not be atypical, and they are not.

3. Era start 2020-04-06 and the COVID weeks (SPLIT-20, SPLIT-6). Right as shipped.
   - The break is real: 19-23% injured before against 25-36% after, a change in which crashes get reported.
     2020-04-06 is the documented date.
   - The lockdown weeks of April-June 2020 hold 16,593 rows (2.6% of the frame). Their weekly volume is 826-1,987
     against about 1,700 now, and their injury share ramps from 0.23 to 0.38.
   - Training from 2020-07-01 instead changes AUC by +0.0002 on average over 9 windows (-0.0008 to +0.0014). The
     COVID weeks neither hurt nor help, and SPLIT-21 would not let a few windows decide this anyway.
   - Remedy: none. One line in splits_comment could record "training from 2020-07 changes AUC by +0.0002".

4. Recurring places (LEAK-18, SPLIT-29, SPLIT-13 / USE-10). Not a problem.
   - The use case ranks sites by expected injury crashes. A site is a known entity, and its history is exactly
     what the analyst has (USE-10 known entity), so places recurring across the cutoff are part of the task.
     SPLIT-29 is the IID rule and does not apply to a temporal split.
   - Size: the 7 place columns (borough, zip, coordinates, three street names) add +0.053 AUC (0.7314 against
     0.6782, 9 windows, steady at 0.046-0.059).
   - Probe facts: 92% of test rows have coordinates seen in train and 67% an on-street name seen in train. Near
     copies across the split cover 0.0% of test rows. Exact copies on coarse non-string inputs reach 28.5%, but 0.0%
     once street text and datetime are included.
   - splits_comment already says "this is not unseen-location evaluation". Remedy: none. Optionally add the +0.053
     so a reader knows how much of the score comes from site memory.

5. Release end and test completeness (SPLIT-10, selection at the release end). Note only.
   - The newest test window's last week (Oct 26 - Nov 1) holds 1,515 crashes, against 1,683-1,785 in the weeks
     before and 1,768 in the same week of 2025. About 200 crashes are still to arrive, under 1% of the window. Its
     injury share of 0.473 is in line with the weeks before (0.468-0.488).
   - Given finding 1, the missing late crashes lean uninjured, but at under 1% of the window the effect on AUC is
     negligible. DATA_END at 2026-11-01 is right.
   - Remedy: none.

Checked and fine:
   - The time column is crash time floored to the hour: an event time, available when the report is filed.
   - Expanding train side (SPLIT-11). Train fractions are 0.889-0.955 (SPLIT-14 holds).
   - Test windows of 19,923-21,849 rows with 8,115-10,268 positives (SPLIT-16, SPLIT-17).
   - No grouping is needed: a crash is the prediction unit, crashes do not recur, and collision_id is a hash since
     the reload, so it is not usable as a group anyway.

Not checked: label amendments (no history in the snapshot). The Person/Vehicles tables' own timing fields were not
downloaded.

</details>

<details><summary>Domain practitioner</summary>

DOMAIN PRACTITIONER REPORT: nyc_motor_vehicle_collisions (folder nyc_motor_vehicle_collisions, full version)
Actor played: a road-safety analyst at NYC DOT (Vision Zero) working from NYPD's MV-104AN crash register.
Date: 2026-11-09. Read-only; scratch: the run folder q.py (numbers below from the raw monthly CSVs,
era 2020-04-06 to 2026-10-31, 631,067 crashes before the copy drop).

VERDICT
Fit: approximate (agree with the definition). One sentence: the crash table lets me rank crashes by how likely someone
was hurt from time, place and vehicle kinds, but the injury count is written on the same report by the same officer,
so there is no moment at which I hold these inputs and not the label; the model is a severity smoother / risk-factor
tool for site ranking, and its target is "any injury" where I act on pedestrian KSI.
Metric: partly. roc_auc ranks crashes city-wide; my decision sums probabilities per site, so calibration matters.
I would choose binary log_loss (MET-1, MET-8), consistent with chicago_traffic_crashes' log_loss.
Ship: yes, as approximate; it is a real, widely studied framing (crash-severity modelling) with a real actor.

HOW THE DECISION IS MADE TODAY (sources below)
NYC DOT picks Vision Zero Priority Corridors, Intersections and Areas from pedestrian KSI (killed or severely
injured): corridors ranked by pedestrian KSI per mile until half of the borough's KSI is covered; intersections by
raw pedestrian KSI count (top 15%); areas by KSI kernel density; five years of data (2017-2021 in the 2023 update).
Severe injuries come from the NYPD FORMS crash database, deaths from the DOT/NYPD reconciled fatality database.
So today the ranking uses observed KSI counts, not predicted probabilities. A model enters as a smoother of noisy
counts (the HSM-style expected-severity idea: expected injury crashes = crashes x P(injury | crash facts)) or as a
risk-factor study (which vehicle kinds, hours, places raise severity). That is the use case the definition writes
("for example ... rank sites"), borrowed from chicago_traffic_crashes (use_case.md Cases, USE-9 row). I accept it.

1. INPUTS AT THE PREDICTION POINT (USE-3, USE-6)
Have, at filing: date and hour, borough, ZIP, coordinates, street names / address, up to five vehicle kinds. All
legitimate; the hour floor (LEAK-13) costs me nothing (I aggregate by hour or coarser anyway).
Correctly not given: the eight injury/death counts (the target, LEAK-10); the contributing factors (filled
differently on injury reports, LEAK-38 measured; I would not use them for severity either - officers' "unspecified"
is a paperwork artefact).
Missing that I would always have (ranked by what they carry):
 a. Whether a pedestrian was struck (crash type). The officer knows it at the scene and it is the single strongest
    severity fact: in single-vehicle crashes 22.2% have a pedestrian hurt, and pedestrian casualties are 21.6% of all
    positive crashes. The table only shows it through the injury counts (the target), so it cannot be added without
    the Person table; and since police no longer take property-damage-only reports, a reported pedestrian strike is
    almost always an injury, so adding it would make much of the task near-trivial. Its absence is what keeps the
    task non-trivial; I name it as a gap, not a fix.
 b. Pre-crash action and vehicle damage (Vehicles table, same report): known at filing, standard severity inputs.
 c. Road context DOT holds outside this table: speed limit, number of lanes, signal control, one-way, LION segment
    class, lighting and weather (the MV-104AN has weather/lighting; NYC Open Data does not publish them). Chicago's
    dataset had these (and dropped some for completeness bias). Here the street name and coordinates stand in.
 d. Number of persons involved (Person table) - known at filing.
None of these is a leak; their absence makes the task "severity from where, when and what vehicles", which is a
coarse but honest subset.

Issue 1 (blank vehicle type, 9,381 crashes in my count, 1.5%; 80.6% injured): from the analyst's chair this is a
pedestrian crash. 77.6% of the blank-type crashes have a pedestrian injured or killed (vs 21.6% of all positives);
the builder's Vehicles lookup found the vehicle row present with type blank but a pre-crash action - consistent with
a driver who left (hit-and-run) or an officer focused on the struck pedestrian. Either way it reflects a scene fact
(a pedestrian struck, possibly a fled vehicle) that I know at filing, not a field filled after the outcome. Recent
share is 1.8% (2025-2026) with 82.4% injured. I would keep it (option A) and word the note as "most are pedestrian
crashes"; option C (Person/Vehicles join) is worth doing only if a rebuild adds pedestrian involvement anyway.

2. TARGET (USE-5)
"Anyone injured or killed" is a proxy. What I act on is KSI, and for Vision Zero priorities pedestrian KSI. On these
rows deaths are 0.27% of crashes (0.67% of positives); "injured" is dominated by complaint-of-pain level injuries,
which police recording drives (the positive share climbs from 34% in 2020 to 48% in late 2026, partly composition:
property-damage crashes stopped being reported in April 2020 and attendance keeps changing). Any-injury still ranks
sites roughly like KSI (both scale with exposure and vulnerable-user conflicts) but it overweights rear-end
"complaint of pain" car crashes at high-volume arterials relative to the pedestrian KSI I act on.
KSI cannot come from the crash table. An expert would rebuild the target from the Person table (f55k-p6yu, from
2016): person_injury plus bodily_injury / complaint / emotional_status give an approximate severe-injury flag (e.g.
fracture, severe bleeding, amputation, unconscious), the same kind of reading DOT applies to NYPD FORMS. That would be
a second variant (KSI, 2-3% positive), not a fix of this one. I would want a probability, not a class.
Selection: since 2020-04-06 the no-injury crashes are those police still attended. My register has the same
selection, so by USE-8 this is not a gap for the analyst, only for anyone reading the probability as "chance a crash
injures someone" in the street. fit_reason says so; good.

3. ROW AND TEST DATA (USE-10)
One row = one reported crash; my decision unit is a site (intersection, corridor, area) over several years. A
crash-level probability is the building block I would sum, so the row is right for the model but not for the score
(see 5). Known places recur (on-street 67%, coordinates 92% of test rows seen: builder's hidden-groups probe); that
is my setting (I re-rank the same city), USE-10 known entity, temporal split right. Test = the next quarter after a
one-month gap, with quarterly refits on everything since April 2020: matches how I would refresh a model. All three
windows fall after the April 2025 factor change and two after the May 2026 vehicle-code change, which is the regime
I would deploy into - better than testing on a stable past.

4. WOULD I USE IT; TRUST (issues 2, 6)
I would use it as a smoother and a risk-factor screen, not to replace observed KSI counts. Trust would rest on:
 - calibration per window and per borough (expected injury crashes per site must sum right; the base rate drifts
   34% -> 48%, and AUC is blind to that);
 - stability of the vehicle-kind effects across the May 2026 code switch. The 12-kind mapping (issue 2, option A)
   keeps what drives severity: the two-wheelers (bicycle, e-bike, e-scooter, moped, motorcycle: 13.0% of crashes,
   80.6% injured), buses, emergency vehicles, taxis, trucks. Losses I would notice: SUV vs sedan merged into "car"
   (SUVs are worse for pedestrians, a live NYC policy topic) and heavy trucks merged with vans and pickups (matters
   for KSI more than for any-injury). For this target both are small; I would not ask for a change unless both code
   lists separate SUV cleanly (the builder's open "Utility" question says they may not). Option A is right; raw
   codes (option C) would break my model at the switch (0.656 vs 0.742 AUC).
 - Recording changes (issue 6): three in 18 months plus the reload. I would trust a model only refit quarterly and
   monitored; the dataset's test windows measure exactly that robustness, which I count as realism, not a defect.
   Borough blank for 30-35% until 2024Q3 then ~3%: a model must not read "borough missing" as a time signal; with
   coordinates present it barely matters.

5. METRIC (MET-1, MET-6 to MET-9)
Declared: Metric.fallback roc_auc (MET-8 fallback, MET-11 origin recorded, places looked named - fine under MET-1's
"look first"; no source metric exists).
Does it score my decision? Partly. roc_auc picks the model that best orders crashes city-wide by injury chance; that
supports a risk-factor screen. But my action sums each crash's probability into expected injury crashes per site and
ranks sites: that needs calibrated probabilities, and the base rate moves between train and test (40% overall vs
47.6% in the newest window), which roc_auc ignores and a site total does not. MET-6/MET-7: there is no threshold or
cost I act on per crash, so no threshold metric. MET-9: average precision is wrong here (positive share 40-48%,
near-majority, and the top-k I follow up is sites, not crashes).
I would choose binary log_loss: strictly proper (MET-8), rewards the calibration my per-site sums need, and matches
chicago_traffic_crashes (multiclass log_loss for the same actor). Brier would also do. The site-level score
(Spearman of predicted vs observed injury crashes per intersection) would be the ideal but is not a row metric;
not worth a custom spec. Not a blocker: roc_auc stays defensible under the MET-8 default; flag for the curator.

GAPS, RANKED BY HOW MUCH THEY CHANGE THE TASK
1. No prediction moment: the label is on the same report as the inputs; the model is a smoother / risk study
   (USE-3, USE-9; the reason the fit is approximate, same as chicago).
2. Target any-injury, not (pedestrian) KSI: positives mostly minor, recording-driven drift 34% -> 48% (USE-5).
3. Unit: I act on sites, the rows and the score are crashes; roc_auc ignores the calibration my sums need (MET-1).
4. Missing scene facts I always have: pedestrian struck, pre-crash action, persons involved, road context
   (USE-6) - the pedestrian fact would nearly decide the label.
5. Vehicle-kind coarsening (SUV in car, heavy trucks in vans) - small for this target (issue 2).
6. Recording changes (issue 6): a trust question handled by quarterly refits; realism, not a gap.
Not a gap: the blank vehicle type (issue 1) - a pedestrian/fled-vehicle scene fact, keep (A); the post-2020
selection of no-injury crashes, which my register shares (USE-8).

WHAT AN EXPERT WOULD CHANGE
- Metric: log_loss instead of roc_auc (MET-1, MET-8), as chicago_traffic_crashes.
- Issue 1 note: say "77.6% of these crashes have a pedestrian hurt; likely a struck pedestrian or a fled vehicle,
  both scene facts" rather than only "maybe a recording gap" (fit_reason currently says "maybe a recording gap").
- Later variant (not this one): a KSI target built from the Person table, with pre-crash action from Vehicles.
- Keep the 12 kinds; split SUV from car only if both code lists allow it.

ANSWERS TO THE PROMPT'S QUESTIONS IN BRIEF
Inputs at filing: yes, all; contributing factors rightly dropped. KSI: yes I would want it; this register cannot
give it, Person table could approximate it. Use: screening/risk factors and site ranking smoothing, not Vision Zero
evaluation (evaluation compares observed KSI before/after treatment; a severity model only adjusts for crash mix).
roc_auc: partly. Vehicle mapping: keeps what matters. Blank type: a pedestrian sign (77.6%), known at filing.
Trust across recording changes: with quarterly refits and calibration checks, yes; the test windows test exactly that.

SOURCES
- dataset.py and README of the folder; builder_report.md; use_case.md (USE-3, 5, 6, 8, 9, 10, Cases USE-9
  chicago_traffic_crashes); metrics.md (MET-1, 6, 7, 8, 9, 11); chicago_traffic_crashes/dataset.py (use case, metric).
- Own counts on the raw monthly CSVs (the run folder q.py).
- NYC DOT, Vision Zero Borough Pedestrian Safety Action Plans 2023 update, press release:
  https://www.nyc.gov/html/dot/html/pr2023/vision-zero-borough-pedestrian-safety-action-plan.shtml
- DOT VZV Priority Corridors (method note): https://catalog.data.gov/dataset/dot-vzv-priority-corridors-20241021
- NYC DOT equity and street safety: https://www.nyc.gov/html/dot/downloads/pdf/equity-and-street-safety.pdf
- Vision Zero View: https://vzv.nyc/
- Motor Vehicle Collisions - Person (fields person_injury, bodily_injury, complaint, emotional_status):
  https://catalog.data.gov/dataset/motor-vehicle-collisions-person (severity mapping from these fields is my domain
  reading, not verified against the dictionary).

</details>

<details><summary>Blind review</summary>

BLIND REVIEW: nyc_motor_vehicle_collisions (target anyone_injured_or_killed, binary, temporal split on crash_datetime)
Inputs used: clean_room/data.parquet (200,000-row sample), clean_room/task.md, NYC Open Data page/metadata API and SODA API for h9gi-nx95. No other local files were read.

VERDICT: Include with changes. It is real, large data with moderate, non-trivial signal (temporal LightGBM AUC about 0.73-0.74). But the prediction moment needs to be stated, the near-ID address column dropped, and the outcome-linked selection and missingness drift written down.

WHAT THE TASK IS
Each row is one police-reported NYC crash (MV-104AN form), from 2020-04-06 to 2026-10-31. The features are the hour of the crash, where it happened (borough, zip, lat/lon, street names) and the types of up to 5 vehicles. The target is whether anyone was injured or killed. Base rate in the sample: 40.0% Yes (80,005 / 200,000). The rate rises over time: 33.5% (2020), 35.1%, 38.0%, 41.9%, 44.0%, 43.7%, 45.0% (2026).
Plausible users: EMS/dispatch triage at report time, an insurer's first notice of loss, or a city safety analyst estimating injury risk from crash composition. Vehicle types and location are known early (a caller can say "car hit a cyclist"). So the use is real, but it is a weak, partly retrospective use. All features come from the completed police report.

CHECKS RUN
- Types: crash_datetime is datetime (rounded to the hour, minutes are always 0). borough, zip_code and vehicle_type_code1..5 are category. Street names are string. Lat/lon are float.
- Missing values: borough 26%, zip 30%, lat/lon 7.4%, on_street 29%, cross_street 50%, off_street 71%, vehicle1 1.5%, vehicle2 34%, vehicle3-5 91-99%.
- The data is sorted by time. 34 exact duplicate rows and 53 duplicate feature rows (0.03%).
- Source: 2,303,506 rows from 2012-07-01 to 2026-11-03. The source also has injury/death counts by person type, contributing factors and collision_id. All of these are correctly removed here, so there is no direct label leak.
- Temporal LightGBM, last 30% of rows as 3 test windows of 10%, AUC per window:
    vehicles only            0.660 / 0.675 / 0.677
    time+place only          0.566 / 0.569 / 0.573
    all, no street names     0.727 / 0.740 / 0.734
    all with street names    0.723 / 0.740 / 0.735
  Top gain: vehicle_type_code1, on_street_name, vehicle_type_code2, cross_street_name, zip_code, on_street_name missingness.

CONCERNS, MOST TO LEAST SERIOUS
1. The rows that exist depend on the outcome, and the prediction moment is not stated.
   Source: "The police report (MV104-AN) is required to be filled out for collisions where someone is injured or killed, or where there is at least $1000 worth of damage."
   So an injury makes a crash reportable by itself, while non-injury crashes enter only above a damage threshold and only if reported. The rising base rate (33.5% -> 45.0%) fits a drop in non-injury reports, or inflation lowering the real value of the $1000 threshold, more than a real change in severity. A model learns P(injury | reported), not P(injury | crash).
   A related reporting artifact: when vehicle_type_code1 is missing, 81% are Yes (2,950 rows in the sample). In the source, 7,523 of 9,381 crashes since 2020-04-06 with a null vehicle_type_code1 had persons_injured > 0. A missing vehicle on the form (e.g. a hit-and-run on a pedestrian) is a recording pattern linked to the outcome. It is legitimate at report time, but it is not crash physics.
   Change: in task.md, state the prediction moment ("at police report filing, before injury counts are entered") and the selection rule. Keep the missingness, because it is known at report time, but document it.

2. off_street_name is close to a row ID.
   The sample has 46,928 unique values, 40,841 of them singletons (87%). Examples: '889 SAINT NICHOLAS AVE', '1966 NEWBOLD AVE'. These are house-number addresses. The column is stored as free string, so a pipeline will either drop it or one-hot encode tens of thousands of levels. Street names add nothing measurable (AUC 0.7403 vs 0.7396 without them).
   Change: drop off_street_name or replace it with a has-address flag. Keep on_street/cross_street as high-cardinality categoricals (5,096 and 5,796 levels) or drop them as well.

3. Missingness drifts over time because of source processing.
   Borough missing by year: 35.1% (2020), 34.8, 33.5, 31.9, 28.8, 8.3 (2025), 3.0% (2026). Zip_code drifts the same way. 21% of rows have lat/lon but no borough. This looks like a geocoding change at the source in 2025. Under the temporal split, the test windows have far fewer missing boroughs than training, so models are judged partly on how they cope with this artifact.
   Change: fill borough/zip from lat/lon where coordinates exist, or document the shift.

4. Preparation choices that are not explained.
   (a) The window starts on 2020-04-06 although the source starts in 2012-07. This is probably to avoid the TAMS->FORMS change and the start of COVID, but it is not stated.
   (b) The raw vehicle-type free text (e.g. 'Sedan' 273,779, 'Station Wagon/Sport Utility Vehicle' 214,598, '4 dr sedan', 'Box Truck', 'Pick-up Truck', 'Van') is collapsed to 13 classes. Sedan and SUV both become 'car', which covers 81% of vehicle1. This is lossy, and the mapping table is not published.
   (c) Time is rounded to the hour, although the source has minutes. This is harmless.
   (d) Source records are "preliminary and subject to change when the MV-104AN forms are amended". Labels for recent months may still change.
   Change: publish the vehicle mapping and the start-date reason.

5. Small items.
   34 exact duplicates in 200k rows (possible double-filed reports, about 100 expected in the full table). Remove them or keep them; the effect is negligible. The target is stored as a category 'No'/'Yes'. Fine.

WORTH BENCHMARKING?
Yes. It is large (630k rows), the signal is moderate and not trivial, and the data is real, mixed-type, high-cardinality and drifting over time. Tabular models can be told apart on it. The ceiling is low because injury depends mostly on things that are not recorded.

COULD NOT CHECK
- The full 630,838-row table (only the 200k sample is here). Some SODA count queries failed with "Service unavailable", so I could not confirm that 630,838 equals all source rows in the window.
- The exact filters and vehicle-type mapping used in preparation.
- The exact boundaries of the 3 test windows (I used 70/80/90% row cuts).
- Whether labels for recent rows were later amended in the source.
Scratch files: the run folder  (lgb.py, meta.json).

</details>

<details><summary>Task gamer</summary>

nyc_motor_vehicle_collisions: task gamer report

Verdict: the task cannot be gamed. No attack beat the honest baseline by more than about 0.002 AUC, and the one that did uses information a deployed model also has.


Honest baseline (in the run folder)
Untuned LightGBM (400 trees, 63 leaves, lr 0.05) on all features plus hour, day of week, month and an absolute day count t.
AUC r0f0 / r1f0 / r2f0 = 0.7499 / 0.7511 / 0.7287, mean 0.7432.
Noise: a random column added moves the mean to 0.7427 (seed 0) and 0.7436 (seed 1), i.e. -0.0005 to +0.0004.

Exploits ranked by gain over the baseline
1. Format features.
   Features: off-street address starts with a number or "NN-NN", street-name lengths, bitmask of missing location fields, lat/lon decimal count.
   0.7516 / 0.7527 / 0.7308, mean 0.7450; gain +0.0017 / +0.0016 / +0.0021.
   Format-only features alone: 0.6302 / 0.6314 / 0.6308, mean 0.6308.
   A deployed model has these: they record how the crash location was written down at the report. Signal, not a leak. Fix: none needed.
   The missingness behind it: injury rate 0.26 at a street address against 0.455 at an intersection; 0.81 when vehicle_type_code1 is missing.

Task flaws
None found that a participant can exploit.
Opposite flaw (hurts an honest model): the absolute time column lets the trees fit the 2020-2026 rise in the injury rate (0.32 to 0.48), which they cannot carry past training.
  Dropping t: 0.7525 / 0.7520 / 0.7320, mean 0.7455 (+0.0023). This is a modelling choice, not a task flaw; no fix needed.
  Recent-only training is worse: last 1y 0.7252, last 2y 0.7326, last 3y 0.7379 (means). Old training rows do not hurt.

Attacks that found nothing
1. Row order: label against position within the hour, Spearman -0.002 (p = 0.19); next-row agreement within the hour 0.529 against 0.520 expected. Index is 0..n in time order; collision_id is dropped.
2. Counts over train and test together (same hour, same day): 0.7496 / 0.7517 / 0.7277, mean 0.7430 against 0.7432. On the model without t, counts plus same hour and place: mean 0.7438 against 0.7455.
3. Copies across the split: 0 test rows with an exact feature copy in training on every split; 32-34 duplicate rows inside each test window. Same hour and place plus exact-copy counts: 0.7498 / 0.7507 / 0.7279, mean 0.7428.
4. Number and string formats: label rate flat across lat/lon decimal counts (0.38-0.40); no zero or sentinel coordinates; street strings already upper-cased and trimmed; time rounded to the hour (minutes all 0).
5. Train-versus-test classifier (last 12 months of training against the test window, no calendar features): AUC 0.538 / 0.553 / 0.574, driven by street names and zip codes, not the label.
6. Format drift over time: borough missingness falls from about 0.21 to 0.03 in April-May 2025; zip and cross-street missingness rise from February 2026. Neither lines up with a label change. The source feed froze on 11 June 2026 (Streetsblog) and was backfilled; weekly counts, label rate and missingness are continuous across that date.
7. Columns from after the prediction point: injury counts and contributing factors are dropped. Best single feature is on_street_name at 0.6244, mostly through whether it is missing; vehicle_type_code1 0.5838; t alone 0.5000.
8. Whole-table transforms (standardised, min-max, ranks): none present.
9. Late labels in the newest training rows: no drop in the label rate at the end of training; each test window starts one month after training ends.
10. Past injury rate at the same place: 0.7280 / 0.7242 / 0.7053, mean 0.7192, worse; my leave-one-out encoding leaked training labels. It would be honest signal anyway.

Source lookup: works. The public Socrata API matches the kit's monthly counts within 1-6 rows and carries the injury counts, so a join on date, hour and place recovers the label. Not ranked.

Not checked
- Vehicle-type strings before they were mapped to the kit's 12 categories.
- Whether NYPD adds vehicle records after the first report. If so, the 0.81 missing-first-vehicle signal partly comes from after the prediction point.
- Tuning beyond the two LightGBM models above.

Sources
-------
https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95
https://nyc.streetsblog.org/2026/09/09/empty-quarter-citys-crash-database-hasnt-been-updated-in-three-months

</details>

<details><summary>Precedent check</summary>

PRECEDENT CHECKER: nyc_motor_vehicle_collisions (2026-11-09)

Verdict: 14 of 17 calls follow precedent. Two calls depart with no fact stated that sets them apart, and each gets a
reflection prompt below:
  (1) the blank vehicle type, kept under LEAK-38, although LEAK-38 does not cover this dataset;
  (2) the borrowed site-ranking actor, which has an unaddressed cross-curator pair: thailand_road_accident_register_2019_2022.
One real pair runs the other way: Chicago's 9 windows depart from SPLIT-15, and NYC's 3 windows follow it.
The vehicle mapping follows its method precedent (force_2020), but its own check fails on taxi because of the
DELIVERY bug (column auditor, finding 2).

Sources read: the dataset.py of nyc_motor_vehicle_collisions and chicago_traffic_crashes;
the records of chicago_traffic_crashes,thailand_road_accident_register_2019_2022,us_accidents,
noaa_storm_events_damage,nhtsa_crss_crash_severity,stats19_collision_severity;
the curation rule files; the panel's decision register (flags); builder_report.md;
the column auditor's report.

PER DECISION
1. Actor borrowed from Chicago ("For example, a city road-safety analyst ... rank sites") (USE-1, USE-9)
   Status: departs from a precedent, with no stated reason (the Thailand pair).
   - Follows: USE-1 Methods ("otherwise write the most plausible one and say 'for example'").
   - Follows: chicago_traffic_crashes (CC 2026-11-05, Lennart, issue 7 A). The blind reviewer named the same actor
     without our notes; the case was entered in the USE-9 Cases table.
   - Pair: thailand_road_accident_register_2019_2022 (CC 2026-11-03, Andrej): `No` + `No Good Target / Scientific
     Discovery`, "as glioma_grading": "once a crash is in the register its deaths are in the same record, so the model
     predicts a count already on file". The AI had offered the reading Chicago and NYC use now (the severity part of
     road-network site screening, the HSM relative severity index), and Andrej did not accept it ("We do C").
   - Same mechanism here: the builder's checklist says "the analyst already sees the injury count of a reported
     crash, so the decision is the smoothing of expected injuries per site".
   - Chicago's CC of 2026-11-05 came two days after Thailand's and does not mention it. No record, rule or Cases row
     names what sets Chicago apart from Thailand. NYC inherits the unaddressed pair.
   - The NYC blind reviewer's report is not in the panel folder yet, so USE-9's independent-actor test (the thing that
     carried Chicago) is not yet met for NYC.
   -> Prompt A below.

2. Target "any of the 8 counts > 0" (USE-5)
   Status: consistent, with a stated reason.
   - The crash table carries only injured/killed counts, so a binary target is the finest it offers.
   - Reading all eight counts is confirmed by the column auditor: 13,908 rows have persons_injured > 0 with every
     part 0 (e-scooter, e-bike and moped riders).
   - The pair with Chicago's 5 KABCO classes is set apart by the source: NYC's crash table has no severity scale.
     This is evident from the data, and fit_reason says the police count stands in.
   - Not checked: whether the Person table (f55k-p6yu) holds per-person injury descriptors from which a severity
     target could be built (a later variant, PROV-7 / USE-5). No precedent is broken now.

3. Five contributing factors dropped (LEAK-38 measured clause -> LEAK-10)
   Status: consistent.
   - chicago_traffic_crashes, five condition fields (CC 2026-11-04, Lennart): fill flags won back 72% of their gain.
   - chicago_traffic_crashes, `dooring_i` (CC 2026-11-05, Lennart): filled 4-8x as often for injured crashes within
     a crash type; dropped at a cost of 0.00011 log loss.
   - Chicago also dropped prim/sec contributory causes as investigation information.
   - kick `WheelType` and expresso REGION (2026-10-22, Lennart; the LEAK-10/LEAK-38 Cases row).
   - NYC's numbers are stronger: 87% of the gain from fill flags, conditioned on the number of vehicles.

4. Crash time floored to the hour in `_clean` (LEAK-13)
   Status: consistent.
   - Same mechanism and the same placement as chicago_traffic_crashes issue 9 B (CC 2026-11-05, Lennart): floored
     in `_clean`, before the framework sorts the rows.
   - Same rule as hepatitis_c_prediction and gallstone_disease.
   - Column auditor: the :00 and :30 heaping and the midnight flag (AUC 0.492) fall inside the floor.

5. Blank vehicle type in every slot, kept with a "Potential leak, kept on purpose" note (LEAK-38 / LEAK-13 / LEAK-6)
   Status: departs, with no fact stated that sets it apart. Under the ranking this is not a reasonable exception as
   written.
   - Scope: LEAK-38 (Should) covers fields "whose timing the source leaves undocumented and no test can establish,
     in data the data owner released for its own competition or challenge". A city register is outside that scope.
     Every LEAK-38 keep by a curator is challenge or host data:
       african_credit_scoring_challenge;
       medical_facility_operational_data (2026-11-04/05, Lennart);
       tunisian_fraud_detection_challenge (2026-11-05);
       sendy_logistics_challenge (2026-11-05).
     The register flags LEAK-38 with "3 keep / 1 exclude", all inside that scope.
   - A test exists: the column auditor's Person-table test. So "no test can establish" fails, and the measured
     clause sends a confirmed mechanism to LEAK-10 (Must).
   - LEAK-6 (Must) allows "a slight optimism with a known cause". Here the cause is not known: the note itself says
     "this table cannot tell".
   - The nearest keep of a blank, treehouse_pediatric_tumor_type, names its mechanism: age and sex missing by study,
     not by patient.
   - Closest precedents, all drops of fields whose fill differs by outcome:
       chicago_traffic_crashes `dooring_i` (2026-11-05) and the five condition fields (2026-11-04, Lennart);
       kick `WheelType` (kept 2026-10-01, dropped 2026-10-22).
   - Chicago's own treatment of the parallel codes: "Unknown/unreported categorical codes become missing", which
     merges unknown and blank. NYC keeps "unknown" as its own kind and the all-blank as missing, so the blank stays
     distinguishable. That is the opposite of Chicago, and no reason is given.
   - Drift: if accepted as written, this would be the first LEAK-38 keep outside the amended scope by Lennart, after
     he narrowed it twice (2026-10-22, 2026-11-05).
   - Third exception: none of this kind found (searched every "Potential leak, kept on purpose" note in the working
     copy). No amendment is due.
   -> Prompt B below.

6. Own 12-kind vehicle mapping over two code lists (CLEAN-21, CLEAN-12)
   Status: departs from CLEAN-21's wording ("the conversion the source or the measuring body publishes"), with a
   stated reason.
   - No published crosswalk between the two lists exists.
   - The dictionary's 8 categories are coarser and merge truck with bus.
   - The method follows force_2020_well... (CLEAN-21 Cases, 2026-10-21, Lennart): a conversion inferred from the
     data is accepted when checked against a second measure. Here the check is the shares in the same season a year
     apart (decision D2).
   - But the check fails where the bug sits: "taxi or limousine" is 2.36% (old list) vs 3.49% (new list), because
     LIVERY matches DELIVERY (1,259 vehicles, 1,332 crashes; column auditor).
   - force_2020's rule for unchecked conversions is "masked, not converted". By that rule, new-list "Utility" (989
     vehicles, no check, plausibly a utility-body truck) should go to "other" or "unknown" rather than be guessed as
     "car".
   - The bug is a fix, not a precedent question, so there is no prompt. Fix it and re-measure D2 before the curator
     answers draft issue 2.

7. Street names to USPS abbreviations (CLEAN-21)
   Status: consistent.
   - USPS Publication 28 is the published standard, so this is the measuring body's conversion. The column auditor
     finds no residual format signal.
   - Typing: `string` here vs Chicago's `street_name` as categorical. Cardinality sets them apart (off_street_name
     120,191 distinct). No departure.

8. ZIP code as a category (CLEAN-14)
   Status: consistent.
   - Follows house_sales `zipcode`, bemtpl97 `postcode` and france_dvf `code_postal` (all categorical).
   - The one numeric precedent, brazilian_ecommerce (CEP prefixes, whose order follows geography), is the exception
     with its reason written. No pair.

9. One-month gap, by precedent, not measured (SPLIT-10)
   Status: consistent with SPLIT-10 as amended 2026-11-04/05 ("a gap ... where late labels are documented and the
   collection does not cover them").
   - The portal documents amendments: "preliminary and subject to change when the MV-104AN forms are amended".
   - The reload removed the update times that Chicago used to measure the delay (99.4% within 30 days).
   - Probe 13 finds no fall at the release end (|z| < 1.5). That rules out selection at the end, but it does not show
     what a refit at a window's start would have known.
   - It does not match lt_vehicle_loan's no-gap application (one due date, labels final at release, measured).
   - Wording: `splits_comment` should rest the gap on the documented-amendment clause, not on "follows
     chicago_traffic_crashes". Chicago's gap stood on a measurement NYC lacks.
   - Cost: about 1.3% of a training side, the same order as Chicago's 1.0-1.4%.

10. Three windows vs Chicago's nine (SPLIT-14, SPLIT-15)
    Status: NYC is consistent; the pair runs the other way.
    - SPLIT-15: "as many windows as an IID or grouped task of that size would get folds". REPEATS_BY_TRAIN_SIZE gives
      1 x 3 folds above 250k train rows, so NYC's 3 follows the rule.
    - SPLIT-14 holds: train >= 89%.
    - chicago_traffic_crashes (998,117 rows, train sides > 250k) ships 9 quarterly windows with no reason stated. The
      9 comes from Myunghwan's `_1m` recipe of 2026-10-29 and was not revisited in Lennart's CCs of 2026-11-04/05.
    - The departure is Chicago's, so NYC needs no change. If the curator wants the two siblings alike, Chicago needs
      its own issue. No prompt for NYC.

11. Era start 2020-04-06 (SPLIT-6, SPLIT-20)
    Status: consistent.
    - Same kind as Chicago's start of 2017-09-01 at the citywide-coverage break (CC 2026-11-04, Lennart): the train
      side begins at a documented reporting break.
    - The break here changes the population (property-damage-only crashes no longer reported): 19-23% injured before
      vs 25-36% after, from the NYPD press release.

12. Fallback roc_auc (MET-1, MET-8, MET-11)
    Status: consistent.
    - MET-8 names roc_auc as the binary fallback.
    - churn_telco_south_asia kept fallback roc_auc (2026-10-21, Lennart).
    - Chicago's log_loss is the multiclass fallback, not a different choice for the same kind of task.
    - Observation, not a departure: the actor sums probabilities into expected injury crashes per site, which rewards
      calibration that ROC AUC does not score. A MET-11 `context` argument for log_loss could be made, but no
      precedent forces it.

13. Year 2026 as the pinned snapshot (PROV-9)
    Status: consistent.
    - PROV-9: "A source that grows over time (a public register ...) takes the year of the snapshot we pin."
    - Same as chicago_traffic_crashes (year 2026, PROV-9, panel of 2026-11-04).
    - The record's first publication (5/7/2014) is correctly not used.

14. The 2026-10-29 reload (PROV-13)
    Status: consistent.
    - The reload is not value damage: it hashed the ids, reset the update times and changed vocabularies that the
      definition harmonises. The origin keeps no pre-reload snapshot.
    - Same treatment as Chicago's bulk reload of 2026-05-21 and its 2026-11-03 batch rewrite: kept, with the limit
      stated.
    - Note the column auditor's finding: the 7,313-row batch of 2026-11-06 has zero coordinates. Its note should
      replace "not geocoded" (CLEAN-1 wording, no precedent issue).

15. Licence wording (EV-4, PROV-10)
    Status: consistent.
    - "See Terms of Use (NYC Open Data)" parallels Chicago's "See Terms of Use (City of Chicago Data Portal)". The
      licence decides nothing (EV-4).
    - @misc with author NYPD and the portal URL is the publishing work, as Chicago's City/CPD @misc (PROV-10).

16. Uniqueness next to Chicago (PROV-4, PROV-7)
    Status: consistent.
    - Tensions row "Same task, another source" names this very pair (Lennart, 2026-11-08): both enter.

17. Exact source copies (229) dropped; reduced duplicates kept (LEAK-19, LEAK-18)
    Status: consistent.
    - Chicago's rule word for word: drop on all original fields but the ids and metadata, and never deduplicate on
      the reduced vector.

REFLECTION PROMPTS (issue shape, review_file_format.md)

Prompt A (decision 1)

Consistency check: What sets the site-ranking actor of nyc_motor_vehicle_collisions (and
chicago_traffic_crashes) apart from thailand_road_accident_register_2019_2022, rejected because the outcome is
already on file?
   - **Problem:**
     - The NYC use case is Chicago's: an analyst estimates each reported crash's chance of injury to rank sites, though
       the report already carries the injury count.[use1]
     - Andrej retired the Thailand register on 2026-11-03 for that mechanism ("the model predicts a count already on
       file"), after the same site-screening reading was offered and declined.[thai]
     - Chicago shipped two days later with the site-ranking actor; no record names what sets it apart from Thailand.[chi]
   - **Background:**
     - In Chicago, the blind reviewer named the actor without our notes.[use9]
     - NYC's blind reviewer has not reported yet.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Exception, with its fact | Record that the city registers hold every reported crash of a site, injured or not, so a model smooths a rate per site over many crashes (empirical-Bayes site screening), whereas Thailand's register is a national highway list read for a count per crash | Keeps two shipped siblings; names the fact for later registers | Thailand also holds mostly non-fatal crashes (87.6% zero deaths), so the fact may not hold; it needs Andrej's view |
     | b | Treat NYC like Thailand | `No` with `No Good Target / Scientific Discovery` | Consistent with the earlier call | Also reopens Chicago, shipped 2026-11-05 |
     | c | Reopen Thailand to match Chicago and NYC (implemented here) | Thailand gets an issue of its own, with the site-screening actor offered again | One reading for all crash registers | Overrides another curator's call; needs Andrej |
     | d | Amend USE-1 / USE-2 | Write when predicting an outcome already on file serves a decision (site smoothing) and when it does not (glioma's cross-check) | Settles the family once | A rule change across curators, beyond one dataset |

   - **Recommendation:** a if the curator can name the fact (NYC's blind reviewer result is the test), else d with
     Andrej, since the split is between two curators on the same mechanism.
   - **Decision:** Which way out: a, b, c or d?

[use1]: USE-1 (Must): an actor, a moment and a decision; USE-2 (Must): a task no decision fits is out.
[thai]: thailand_road_accident_register_2019_2022, CC 2026-11-03, Andrej, issue 3 (C), as glioma_grading_clinical_and_mutation_features (USE-1 Cases).
[chi]: chicago_traffic_crashes, CC 2026-11-05, Lennart, issue 7 (A); USE-9 Cases row.
[use9]: USE-9 (Should): before settling on approximate, ask whether the data mirrors another well-defined use case.

Prompt B (decision 5)

Consistency check: What sets the blank vehicle type of nyc_motor_vehicle_collisions apart from
Chicago's `dooring_i` and condition fields, dropped because their fill differs by outcome?
   - **Problem:**
     - 9,378 crashes (1.5%) have no vehicle type, and 80.6% of them are injured against 40.0% overall; the keep cites a
       rule whose scope is host-released challenge data whose timing no test can establish.[l38]
     - A test exists (Person-table pedestrians without injury in the blank crashes), and the cause is not known, so the
       "slight optimism with a known cause" route does not apply either.[l6]
     - Chicago dropped `dooring_i` (filled 4-8x as often for injured crashes) and five condition fields on the same
       mechanism, and merged its unknown codes with blank.[chi2]
   - **Background:**
     - The blank alone scores ROC AUC 0.513.
     - 77.2% of the blank crashes have an injured pedestrian.
     - In a sample, the Vehicles table holds a row with type and make blank in 39 of 40.
   - **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Exception, with its fact (implemented, reason to be written) | Keep the blank as missing, with the fact that it marks a scene the officer could not type (a hit-and-run or unseen vehicle in a pedestrian crash), cited under the weak-optimism rule, not the challenge rule | Keeps a scene fact if that is what it is; small signal | The fact is a guess until tested; first keep of this kind outside the challenge scope |
     | b | Treat like Chicago: harmonise | Map an all-blank report to "unknown" in slot 1, as Chicago merged unknown and blank | One reading of "type not known"; cheap; follows the sibling | Loses the blank-vs-unknown difference if it is a real scene fact |
     | c | Test first | Query Person (f55k-p6yu) for uninjured pedestrians in the blank crashes; keep (a) if present, harmonise (b) or drop under LEAK-10 if absent | Decides on a measurement, as the rules ask | A second table to download and join; delays shipping |
     | d | Amend the scope rule | Extend the keep-with-note rule to untested blanks in public registers | Settles later registers | Undoes the narrowing of 2026-10-22 and 2026-11-05 |

   - **Recommendation:** c, with b as the default until the test runs. Writing a's fact without the test would be
     the first keep of this kind outside the challenge scope.
   - **Decision:** Which way out: a, b, c or d?

[l38]: LEAK-38 (Should; scope amended 2026-10-22 and 2026-11-05, Lennart): fields whose timing no test can establish, in data the owner released for its own competition; a measured mechanism goes to LEAK-10.
[l6]: LEAK-6 (Must): a slight optimism with a known cause can stay with a note; a confirmed leak goes even when small.
[chi2]: chicago_traffic_crashes, CC 2026-11-04 (five condition fields, LEAK-10) and 2026-11-05 (`dooring_i`, issue 10 B), Lennart; its `_clean` sets UNKNOWN / NOT REPORTED to missing. Also kick `WheelType` (2026-10-22, Lennart).

NOT FLAGGED (checked, no real pair)
- Kept-on-purpose notes in general: 50 definitions carry one (NYC included); the only blank-related ones with no named mechanism
  are NYC's (treehouse, sarcoma and homesite each name theirs).
- Register flags amendment_due SPLIT-10 / SPLIT-14 and exception_to_must USE-1: they concern other datasets'
  exceptions. NYC takes no exception to those rules.

</details>

<details><summary>Advocate</summary>

ADVOCATE OPENING BRIEF: nyc_motor_vehicle_collisions (2026-11-09)
Position: ship as defined, after fixes that need no decision.

1. No leak, no game (P4, LEAK-10/LEAK-13, Must). Counts, factors and collision_id dropped; hour floor leaves no residual
   (00:00 class-neutral, 1.82% vs 1.66%). Gamer: best attack +0.0017 AUC and it is deployed signal (address vs
   intersection); 0 exact test copies in train; train-vs-test AUC 0.54-0.57 from places, not label. Column auditor:
   "No column is a leak to drop." Outranks any fit worry: P4 is met, fit is weighed below it.
2. Blank vehicle type is a scene fact, not a leak (LEAK-6, LEAK-13). Claim auditor: blank in 13.7% of pedestrian-only
   injury crashes, 0.19% motorist-only, 0.48% uninjured; recording-by-outcome would raise motorist-only, it lowers it.
   Neutralising costs 0.0005 AUC. Keep option A; the mildest remedy is rewording the note (drop the LEAK-38 label,
   say "marks a pedestrian crash"). This resolves the precedent checker's departure without changing data.
3. Split is right (SPLIT-6/14/15/20). Era start confirmed by NYPD release p0403b (weekly share 0.19 -> 0.29). Split
   auditor reproduces windows exactly; gap 0 vs 1 differs by 0.0005; 9 windows add no information (sd .014, season).
   The gap reason is fixed by text: arrivals median 3-5 d, 99th pct 22-48 d (amended SPLIT-10, measured).
4. The DELIVERY->taxi bug is a P7 cleaning fix, not a block (CLEAN-21, Should). Remedy `\bLIVERY`, re-measure D2;
   effect +0.0014 AUC, 1,332 crashes. Remedy ladder: fix the line, keep the dataset. Likewise 'Utility' -> other.
5. Real use, independently named (USE-1, USE-9). Blind reviewer, without our notes, named EMS/insurer/city safety
   analyst; domain practitioner (DOT Vision Zero) says "Ship: yes, as approximate", HSM expected-severity smoothing.
   Thailand pair: there deaths were the target already on file; here a domain actor and an independent reviewer both
   carry the use, which is what USE-9 asks and what carried Chicago. Fit "approximate" is weighed, not a veto.
6. Unique and valuable (PROV-4, "same task, another source"). 630,838 rows, second city vs Chicago (binary, other
   inputs), published since 2014, moderate non-trivial signal (AUC ~0.74). Fix the PROV-7 cite only.
7. Remaining notes are text (no decision): metric reason names RaX-Crash (arXiv 2512.07848; MET-5 fallback holds);
   factor-drop reading corrected (78% of gain = party count) which strengthens the drop; selection rule ($1000 /
   injury) and borough-missing drift written in notes; coord-0 reason corrected. Metric choice roc_auc vs log_loss
   (domain prefers log_loss, Chicago uses it) is the one genuine curator choice; I lean log_loss for consistency (MET-8).

</details>

<details><summary>Critic</summary>

CRITIC OPENING BRIEF: nyc_motor_vehicle_collisions (2026-11-09)
Position: ship only after the changes below. No point asks for exclusion except that point 1 must be settled by the curator first.

1. Real task unresolved against a cross-curator precedent (validity, USE-1/USE-9, Must).
   Problem: the injury flag is written on the same police report as every input; there is no moment with inputs and no label. The actor (site-ranking smoother) is borrowed from chicago_traffic_crashes. thailand_road_accident_register_2019_2022 (CC 2026-11-03, Andrej) was rejected as "No Good Target" for this same mechanism, after the same reading was offered and declined (precedent checker, decision 1; domain practitioner: "no moment at which I hold these inputs and not the label").
   Remedy: the curator states the fact that sets NYC/Chicago apart from Thailand (e.g. the actor sums probabilities per site, a smoother of KSI counts) in the use case, or applies the Thailand call to all three. Not a defect of this folder alone; an unresolved precedent conflict.

2. Cleaning bug: taxi rule matches LIVERY inside DELIVERY (validity of an input, CLEAN-21, Must for a declared mapping).
   1,259 delivery trucks -> taxi after the 2026-05-04 code switch, 1,332 crashes, all in the test windows' era; the mapping's own check fails (column auditor finding 2, precedent checker, claim auditor +0.0014 AUC).
   Remedy: match \bLIVERY\b, re-measure the windows.

3. Blank vehicle type kept under the wrong rule and a wrong mechanism (LEAK-6 vs LEAK-38, Must on label-following inputs).
   9,378 crashes, 80.6% injured. LEAK-38 covers only owner-run competitions (precedent checker). The claim auditor shows the blank marks pedestrian crashes (13.7% vs 0.19%), so "cannot tell" is false.
   Remedy: keep (option A), but rewrite the note to LEAK-6 with the pedestrian mechanism; run the Person-table check for uninjured pedestrians to close it.

4. Factor-drop reasoning and the "blank slot = no further vehicle" claim are false (Should, claim honesty).
   78% of the factors' gain is the filled-slot count (party count); 13.4% of crashes have a factor but blank type (claim auditor). Remedy: correct D3 and notes; offer party count from the Vehicles table as an option.

5. Metric: roc_auc does not match the decision (MET-1, MET-8, Should).
   The actor sums probabilities per site, so calibration matters; Chicago uses log_loss (domain practitioner). The metric reason also misses RaX-Crash (arXiv 2512.07848). Remedy: log_loss, or state why AUC wins.

6. off_street_name is near a row id (Should, LEAK-16/CLEAN): 120,191 distinct values, 71% blank (blind reviewer, column auditor). Remedy: drop or flag; the score barely moves (0.723 vs 0.727).

7. Notes to correct (quality, notes only): gap reason should cite measured arrival lag (median 3-5 d, 99% within 22-48 d; SPLIT-10 amended) not Chicago; lat/lon 0 rows are post-reload backfill (7,313 rows on 2026-11-06, 35.3% injured); 'Utility' -> other/unknown; PROV-7 cite wrong; borough drift 35%->3%.

</details>
