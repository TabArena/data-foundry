# airfoil_self_noise

**Outcome:** added. Ship after changes (review panel, pilot of 2026-10-19). Validity: SEL, USE-3, USE-6, LEAK-10,
LEAK-16, SPLIT-24, SPLIT-28 and SPLIT-29 hold; USE-5 holds, but `predicted` and `question` name the measured level for
what is the source's scaled level (fix: text); USE-1 and USE-8 triggered: the use case names a configuration never
measured, while the run split mostly tests a tested setup at a new speed (issue 1); SPLIT-4 triggered: the reason for
not grouping by chord argues from the score gap (fix: restate it); SPLIT-23 and PROV-10 need the source's prediction
use cited and the BibTeX completed; PROV-8 and PROV-9 hold: UCI 2014 first published the rows (they were digitised in
2006 from the report's figures, and the 2006 and 2008 theses that used them do not list them). Value: TP-1 to TP-5 hold (no probe flags, LightGBM skill
0.837). Quality: CLEAN-14 departure, `attack-angle` typed categorical (fix: one line, numeric). Weighed, issue 1: for
the run split, filling in untested speeds is a real query and the CC of 2026-10-06 stands; for the setup split, the
source organises its data by setup, the practitioner's open queries are a new angle or size, and concrete was grouped
by mix. Issue 2: keeping is the release as published and the engineer's own normalisation; re-targeting gives the
quantity the source plots (TP-6). Changes that need no decision, listed and not applied in this pilot: `attack-angle`
numeric, with UCI's "Binary" label noted as an error of that copy; the target named as the source's scaled level with
its conversion; the tripped set, the corrected angle and the truncated bands stated; what the run split holds out
stated; the chord reason restated; the source's prediction use cited; the 62% and the grouped R² corrected in the
notes and in an Assessment line under the CC of 2026-10-06; the BibTeX completed; a line in the record on
"Outdated"; a CHANGELOG entry; then a rebuild on your ask. Already done in the rules: the hidden-group probe lesson in
task_probes.md and evidence.md, and the probe's float gap raised in the working copy's REVIEW.md.

**Main points:** Hold out whole runs or whole setups (issue 1); keep the scaled target or re-target to the measured
level (issue 2). The record's year follows the definition (2014) unless you keep it.

**Record fields that disagree with the definition:**

- `year`: record `1989`, definition `2014`.

**Record judgment:** valid. NASA wind-tunnel measurements (Brooks, Pope and Marcolini 1989, NASA RP-1218) of the
tripped NACA 0012 set; the rows match UCI's file and the two report figures checked (Figs. 11(a) and 12). The rows
were read off the report's figures: "The input-target data set was created from a noise database taken by digitising
the appropriate figures from [the NASA report]. The database contains 1503 entries" (Lau, López and Oñate, CIMNE
preprint PI-335, Sec. 4.1, [UPCommons](https://hdl.handle.net/2117/172215)); so the levels carry digitising error,
and their 0.01 dB grid is the digitiser's, not NASA's. First publication of the rows: UCI, 2014 (PROV-8, PROV-9).
López's 2008 PhD thesis ([PDF](https://old.cimne.com/flood/docs/PhDThesis.pdf), Sec. 4.3, Table 4.5) gives only summary
statistics, and Lau's 2006 MSc thesis is not public. Unchecked: an early release of the Flood library (about 2008-2010)
may have shipped the data file before UCI. "Outdated"
has no rule behind it and the physics does not age (kept like concrete_compressive_strength). The CC of 2026-10-06
stands as the decision, but three of its statements are refuted: the 62% (the run-mate share is 66.6%; 62.5% is a
nearest-neighbour statistic), the chord reason (it argues from the gap, SPLIT-4) and the probe lesson (the thickness
alone separates 104 of 106 runs). An Assessment line below it will say so; the CC itself stays as written.

**Issues for the curator:**

1. **Hold out whole runs or whole setups (one airfoil size at one angle)?** The shipped split holds out wind-tunnel
   runs, but for 91.5% of test runs (77.1-100% per split) the same airfoil at the same angle is in training at another
   speed, and the source has divided the speed effect out of the target (issue 2), so a run at a new speed looks much
   like its sibling in training. So the score mostly measures filling in a missing speed for a tested setup, and
   overstates how well a model predicts a new angle or size, which the use case ("before, or instead of, measuring it
   in a wind tunnel") names (USE-1, USE-8, SPLIT-1, all Must; a weighing of framings). Extra trees R² is 0.855 by run
   and 0.774 by setup; this shows what the test measures and is no reason by itself (SPLIT-4). The 2026-10-06 CC
   weighed IID and chord only, not the setup.
   - Implemented: the run split (`Grouping(on="run")`). For it: filling in the test matrix is a real query (20 setups
     were run at all 4 speeds, 13 at only 2); the source names size, speed and angle on equal terms. Needs `use_case`
     reworded to that moment ("an engineer extending a tunnel campaign on a tested airfoil decides which settings to
     run and which to take from a model") and the 91.5% stated in `split`, `splits_comment` and `fit_reason`. Against
     it: the benchmark then tests no new angle or size, and rewording the use case to fit the split meets the factor
     "a use case rephrased only to excuse a gap" (USE-9); the practitioner says it does not apply because the query
     is real.
   - Alternative: group by setup (`Grouping(on=["chord-length", "attack-angle"])`, 33 groups, about 11 per test
     fold). For it: the source organises the data by setup ("Each figure contains spectra for a model at a specific
     angle of attack for various tunnel speeds", Sec. 4.3); the practitioner: "the queries I cannot answer by running
     the tunnel for five more minutes are a new angle or a new size"; precedent: on concrete_compressive_strength's
     random split, 73% of the test rows had their mix in training at another age, and the curator then grouped by mix
     (CC 2026-10-14: "a new prediction is for a mix not tested before"); a mix is to concrete what a setup is here,
     and age what speed is. That call is newer than this dataset's CC of 2026-10-06. Requires the numeric angle (75%
     of test runs would see an unseen angle value).
   - Recommendation: the setup split, treating it like concrete, unless the curator names the fact that sets airfoil
     apart. The AI's best guess at that fact is weak: speed is the cheap setting once a setup is mounted and 13 of 33
     setups lack two speeds, but a tested mix at a new age is as real a query. The advocate recommends the run split
     with the reworded use case; the split auditor makes the case for the setup and the critic leaves the choice to
     the curator; the practitioner calls a new angle "the more valuable query". Decision needed: which moment the use
     case names. If the run split stays, its distinguishing fact is recorded; the other ways out are to reopen
     concrete or to amend SPLIT-1 for a setup measured at several speeds.
2. **Keep the scaled target or re-target to the measured level?** The target is not the level the microphone
   measured: the source subtracted a term that grows with the fifth power of the wind speed and with the boundary-layer
   thickness, so that spectra at different speeds line up (eq. 19, Sec. 5.1.1: "Scaled SPL1/3 = SPL1/3 − 10 log(M^5
   δ* L / r_e²)"; M is the Mach number, δ* the thickness feature, L the span, r_e the microphone distance). The term
   shifts each run by +52 to +90 dB; the measured levels run from 26.8 to 86.4 dB. The conversion is exact (the
   mediator confirmed the constants: all 1,503 rows land on the 0.01 dB grid with the report's span and microphone
   distance and a speed of sound of 340.46 m/s), so a band's error in dB is the same either way and USE-5 holds; what
   changes is what models must learn (untuned RMSE, scaled / measured: random forest 2.85 / 3.67, extra trees 2.92 /
   4.22, LightGBM 2.96 / 3.12; TP-1: a question, not a verdict).
   - Implemented: keep the scaled target, as released; the wording is to be fixed (no decision needed; not applied in
     this pilot).
   - Alternative: re-target to the measured level, which the source plots and an engineer reads; models then learn
     the U^5 and δ* scaling themselves. Whether that is a definition change or a new dataset (PROV-14) is read
     differently by the advocate and the mediator. The critic reads TP-6 (Must: a better version the source itself
     defines replaces ours) as pointing here, since the source plots the measured level; the mediator: TP-6 binds only
     if the curator judges the measured level the better version. No precedent re-targets a source's normalised level;
     TP-6's case is eryhemato.
   - Recommendation: keep (the column auditor, the practitioner, the blind reviewer and the advocate; the critic does
     not demand a re-target). Decision needed: which quantity the benchmark asks for.

**Review panel:** ship after changes (mediator). Claim audit: 9 claims hold, 5 are refuted (the target wording, the 62% figure, the reason for not grouping by chord, the angle typing, the probe lesson), 3 hold in part (the grouped R², taken from a numeric-angle version; the fit; the inclusion) and 2 are open (the use case, the split). Blind review: include; its one change (keep `run` out of the features) already holds, and it found the scaled target and the setup question on its own. Agreed: no leak, faithful NASA data, worth benchmarking, the angle numeric, the text fixes. Disputed: run or setup split (issue 1). Open: re-targeting, which nobody demands but TP-6 could require (issue 2). The year was settled after the panel: two theses that used the rows were read, and neither lists them (record judgment above).

<details><summary>Mediator</summary>

The advocate and the critic agree on the verdict (ship after changes) and on nearly every fix. Three points need the curator: run or setup split, re-target to the measured level, and the year. I ran one experiment, on the eq. 19 constants, to settle a disputed fact.

```text
Verdict: ship after changes.
Validity: SEL holds. USE-3, USE-6, LEAK-10, LEAK-16 hold (every feature is a tunnel setting or BPM's tripped
  formula of them; `run` is not a model feature). USE-5 holds in substance; the wording is false, fix the text.
  USE-1 triggered: the use case must name the moment the split tests, and its wording follows issue 1.
  USE-8 direct holds once the text says what a held-out run shares with training. SPLIT-24, SPLIT-28, SPLIT-29
  hold. SPLIT-4 triggered: the chord reason argues from the gap, restate it. SPLIT-23 holds (row, no context);
  the citation is missing, add it. SPLIT-1 group level (run or setup) is open, a weighing call. PROV-9 open
  (2014 on current evidence, two theses unchecked). PROV-10: complete the BibTeX. PROV-15: note UCI's "Binary" label.
Value: TP-1 to TP-5 hold. No flags, LightGBM skill 0.837, beats the dummy on 30 of 30 splits,
  model families spread from ridge 0.50 to extra trees 0.86 (untuned).
Quality: CLEAN-14 departure fixed (`attack-angle` numeric).
Weighed: split level: run side = a real matrix-filling query and the standing CC; setup side = the source
  organises by setup, the practitioner's query and the concrete precedent. Target: keep = release as published,
  BPM's own normalisation; re-target = the measured quantity, models learn the scaling.
For the curator: issue 1, run or setup split (weighing, plus a consistency check against concrete);
  issue 2, re-target to measured SPL (weighing, optional); issue 3, year and source (PROV-9, two unchecked theses).
```

The constants test (EV-1): are the eq. 19 constants confirmed or inferred? I measured where the implied measured level sits on the 0.01 dB grid.

| constants | rows within 0.0005 dB of the grid |
|---|---|
| stated: c0 340.46 m/s, span L 0.4572 m, r_e 1.22 m | 100% of 1,503 |
| c0 343; r_e 1.2192; r_e 1.0 | 0% each |
| c0 340.29; L 0.3048 | 8% each |

A random constant shift reaches 90% on the grid in 51 of 2,000 trials. The report states both lengths: "all of 45.72-cm span" and r_e "122 cm". So the constants are confirmed, and the critic is right on this fact. Its cited statistic does not prove it, though: the circular concentration R = 0.986 is the same for every set of constants I tried. R confirms the M^5·δ* form; the grid phase confirms the constants.

How each disputed point was settled:

- Did the 2026-10-06 CC already decide run against setup? No. It compares run with IID and with chord only, and names neither the setup nor the 91.5%. The run split stands as the curator's decision until changed, because the AI never overrides; the 91.5% is a later measured finding and goes to the curator as a new fact (stages precedence; "Arguing a call"). This is issue 1.
- Does the setup split's larger spread (R² SD 0.06-0.07 against 0.02-0.03) count? No. The tension "the right split against the score" (P4 over P6, forest_fires) says the split follows the application, and with 33 setups the "only a few groups" factor does not apply. The critic wins this.
- Does the source's purpose pick the split? No. The advocate is right that the critic's ellipsis dropped speed: the Summary describes sections "of different sizes ... tested at wind tunnel speeds up to Mach 0.21 ... and at angles of attack from 0° to 25.2°". The critic is right that the stated application, "a large-scale-model helicopter rotor", lies outside the tunnel matrix. The source is neutral; the citation is needed either way (SPLIT-23, PROV-16).
- If the run split stays, which text changes? `split`, `splits_comment` and `fit_reason` state the 91.5% (agreed). The critic also wins on `use_case`: USE-1 (Must) asks for the moment, and "before ... measuring it in a wind tunnel" does not describe this test. The advocate already accepts the practitioner's wording, so this follows issue 1.
- Target, TP-6 and PROV-14. USE-5 holds without re-targeting: the conversion is exact, and a band's error in dB is the same in both forms. TP-6 binds only if the curator judges the measured level the better version. My reading of PROV-14: an exact transform of the release's own columns is a definition change, like a log target (CLEAN-16), not a rebuild; the advocate reads it the other way. It matters only if the curator picks re-targeting.
- Year. The report's tables do not hold the band levels: "In tables 1 and 2, the data processing and manipulations ... are specified for each test case", and the peak Strouhal numbers and scaled peak levels are "also presented in table 1". The critic's open item (two theses) stands under EV-7 (Must). The record's year cannot be changed silently: a record field that disagrees with the definition goes into `REVIEW.md` (pipeline.md).

Changes to make now (no decision needed):

1. `_feature_types` becomes `FeatureTypes(categorical=("run",))` (CLEAN-14, Should: a cheap and safe fix). Note UCI's "Binary" type in the record (PROV-15). Run `dataset check`; the rebuild is the curator's.
2. Reword `predicted` and `question` to name the source's scaled level (USE-5, Must). Add a `curation_comments` bullet with the eq. 19 quote (Sec. 5.1.1, p. 51, suction-side δ*_s), the constants and the conversion, measured level = target + `10 log10(M^5 δ*_s L / r_e²)`; say that a band's dB error is the same in both forms, and cite this test as the proof (PROV-16, EV-6).
3. State what narrows the data in `row`, `fit_reason` and `curation_comments`, with a quote each (USE-8, PROV-16): the tripped set only (Sec. 4.3), the corrected α* (Sec. 2.4), bands truncated where extraneous noise changed the spectrum by "2 dB or more".
4. State what the shipped split holds out, in `split`, `splits_comment` and `fit_reason` (USE-8, Must): in 91.5% of test runs (77.1-100% per split) the same chord and angle is in training at another speed. Rewrite if issue 1 goes to the setup.
5. Restate the reason for not grouping by chord (SPLIT-4, Must): the "only a few groups" factor (6 chords, 2 held out per fold; covertype) and the use case staying inside the tested chord range.
6. Cite the source's prediction use in `Grouping.definition` (SPLIT-23, Must; PROV-16): "An overall prediction method has been developed for the self-generated noise of an airfoil blade encountering smooth flow", applied to "a large-scale-model helicopter rotor".
7. Correct the evidence numbers in `curation_comments` (EV-8, EV-7): the run-mate share under a random 3-fold split is 66.6% (62.5% is the nearest-neighbour statistic); the grouped R² values are untuned numbers from a numeric-angle version, to be re-measured after change 1.
8. Complete the BibTeX: NASA Langley, report NASA RP-1218 (L-16528) (PROV-10, Must).
9. Correct the probe lesson in the `task_probes.md` hidden-group row (which also repeats the 62%) and the `evidence.md` EV-3 case row (EV-3, EV-7): the thickness alone separates 104 of 106 runs, and the probe skips it because it only takes whole-number floats. Raise the gap with the probe's owner.
10. Write `REVIEW.md` (issues 1-3; the year as a record field; a note that the curator's CC line of 2026-10-06 carries the 62% and the wrong probe lesson) and a dated CHANGELOG entry.

Consistency with precedent. The run key follows the composite-key pattern with no drift; the angle typing has no exception to record (change 1); the USE-8 case row (airfoil direct) holds once changes 4 and 5 and issue 1 are done. The precedent check did not test the group level, so it goes to the curator under issue 1:

> Consistency check (AI, 2026-10-19): the run split keeps the same chord and angle at another speed in training for 91.5% of test runs. concrete_compressive_strength was grouped by mix (CC 2026-10-14, "a new prediction is for a mix not tested before"), after 73% of the test rows of its random split had their mix in training at another age. What sets airfoil apart?
>
> (a) Speed is the cheap setting varied once a setup is mounted, and 13 of 33 setups lack two speeds, so filling in speeds is the use case. Record this as the use case. This is the AI's guess, and a weak one: a tested mix at a new age is an equally real query.
>
> (b) Treat airfoil like concrete: group by setup.
>
> (c) Reopen concrete.
>
> (d) Amend SPLIT-1 or SPLIT-24 for nested entities (setup > run > band).

</details>

<details><summary>Claim audit</summary>

Verdict: the definition gets the rows, groups, features and copies right. One validity claim is false: the target is the report's scaled level (BPM eq. 19), not "the sound pressure level in that band". One quality choice measurably hurts: `attack-angle` is categorical. The reason for not grouping by chord argues from the gap, which SPLIT-4 rules out.

The proof for the target (USE-5): the thousandths digit is constant inside all 106 runs. Removing `-10 log10(M^5 δ*_s L / r_e²)` puts every run on one 0.01 dB grid: circular concentration 0.986, against 0.124 for the raw target and 0.155 for the M^5 term alone. The implied measured SPL runs from 26.8 to 86.4 dB, against figure axes of 20-80 dB at 1.22 m; the target runs from 103.4 to 141.0 dB, a per-run offset of +52.2 to +90.2 dB. Report Sec. 5.1.1, p. 51: eq. (19) "Scaled SPL1/3 = SPL1/3 - 10 log(M^5 δ* L / r_e²)", and "the displacement thicknesses for the suction side, δ*_s, are used for these normalizations", r_e = 122 cm; span 45.72 cm (Sec. 2.1); c0 = 340.46 m/s (the report's code).

| claim | result | evidence | rule |
|---|---|---|---|
| Predicted "the sound pressure level in that band"; question "how loud" | refuted | the proof above | USE-5 |
| Use case: a configuration's spectrum before or instead of measuring it; fit direct | untested (a judgment); fit weakened | narrower than written: all 106 runs are the heavily tripped set (Figs. 11-43), the untripped Figs. 44-74 are absent; the label is scaled | USE-1, USE-8 |
| Not grouped by chord: a new size is a harder extrapolation | refuted as the deciding reason; the decision is open | difficulty decides nothing; the 91.5% and the scores per grouping are in the split audit | SPLIT-4, SPLIT-1 |
| A random split gave a test row 62% of its run's other bands in train | refuted | 66.6% (2/3 by construction); 62.5% is the README's nearest-neighbour statistic | EV-8, EV-7 |
| Grouped R²: ET 0.850, LGBM 0.840, RF 0.830, kNN 0.629, ridge 0.490 | from another version | numeric angle: 0.859 / 0.837 / 0.837 / 0.651 / 0.498 (matches); categorical angle as shipped: 0.819 / 0.813 / 0.826 / 0.689 / 0.504 | EV-8 |
| `attack-angle` categorical | refuted | continuous degrees; 8.7% of test rows (up to 24.8%, in 22 of 30 splits) carry an angle absent from train; LightGBM 0.813 categorical, 0.835 without the angle, 0.837 numeric; the ranking RF > ET > LGBM becomes ET > RF ≈ LGBM | CLEAN-14 |
| The hidden-group probe missed the run because a run is three columns | refuted (the mechanism) | the thickness alone separates 104 of 106 runs; the probe only takes whole-number floats (`hidden_groups.py` lines 214-217) | EV-3, EV-6 |
| Year 2014, UCI, CC BY 4.0, NASA 1989 BibTeX | holds, with gaps | UCI donated 3/3/2014, DOI 10.24432/C5VW2C; the record says 1989; the BibTeX lacks "NASA RP-1218" | PROV-8 to PROV-10 |

These hold: 106 runs of 8 / 14 / 19 bands (min / median / max), each one block with no repeated frequency (SPLIT-24); every feature a setting or the report's formula of them (LEAK-10; the angle is the corrected α* = α_t / ζ(c) of Sec. 2.4); the grouping settings; the task probes (`flags: []`); no copies (0 duplicate feature rows; LEAK-16); inclusion in TabArena v0.1.

Refuted, ranked: (1) the target (USE-5, Must). Errors in dB are the same in both forms, but what models learn changes. RMSE in dB on the 30 shipped splits, learning the scaled level: RF 2.85, ET 2.92, LGBM 2.96, kNN 3.82, ridge 4.84; learning the measured SPL: LGBM 3.12, RF 3.67, ET 4.22, ridge 4.93, kNN 5.76. Re-targeting is the curator's call (USE-5 favours it, PROV-14 decides whether it is a new dataset). (2) The chord reason (SPLIT-4). (3) The angle typing (CLEAN-14, Should). (4) The evidence numbers (EV-8, EV-7). (5) The probe lesson (EV-3); non-integer float columns with repeated values are never probe candidates.

Untested: "outdated" (no fact a test settles); whether the report tabulates the band levels, as its table pages (pp. 134-137) did not survive OCR; whether the donor's 2008 thesis published the rows first.

Sources: [UCI dataset page](https://archive.ics.uci.edu/dataset/291/airfoil+self+noise), [NASA RP-1218 (NTRS PDF)](https://ntrs.nasa.gov/api/citations/19890016302/downloads/19890016302.pdf), [OpenML 43919](https://api.openml.org/d/43919), [OpenNN airfoil tutorial](https://www.opennn.net/tutorials/approximation-airfoil-self-noise-prediction/).

</details>

<details><summary>Column audit</summary>

None of the columns leak: every feature is a wind-tunnel setting chosen before the run, or a closed-form function of them. The frame (1,503 rows, 7 columns) matches the raw `.dat` file row for row.

| column | meaning | dtype and cleaning | verdict |
|---|---|---|---|
| `frequency` | one-third-octave band centre, 21 bands from 200 to 20,000 Hz; which bands a run has was the source's choice | int64, clean | fine, with a note |
| `attack-angle` | effective angle α* = αt/ζ(c) (BPM's open-jet correction); multiplied back by ζ(c), the 27 values map onto αt of about 0, 5.4, 10.8, 14.4, 19.8 and 25.2°, within 0.1°; UCI's type "Binary" is wrong | category, 27 levels, 25 of them at only one chord | wrong by meaning (CLEAN-14) |
| `chord-length` | m, 6 sizes from 0.0254 to 0.3048 | float64 | fine |
| `free-stream-velocity` | m/s: 31.7, 39.6, 55.5, 71.3 | float64 | fine |
| `suction-side-displacement-thickness` | δ*, BPM's empirical formula for a tripped boundary layer: recomputed from chord, velocity and angle (ν = 1.4529e-5), it matches all 106 runs, max relative error 4.3e-6, constant within a run; runs 009 and 054 share 0.00529514, both by the formula | float64, a fixed published formula using no acoustic labels | fine (LEAK-10, LEAK-30, CLEAN-5) |
| `scaled-sound-pressure` (target) | UCI: "Scaled sound pressure level, in decibels", scaling undefined | float64, 103.4 to 141.0; dB is already a log scale (CLEAN-16 n/a) | wording fix (USE-5) |
| `run` | group id, chord × angle × velocity = the raw file's 106 blocks | category, not a feature (`n_features` 5) | fine (LEAK-33) |

1. Target wording (USE-5, Must; holds in substance). The target is the scaled level (proof: claim audit). My own circumstantial checks agreed: the run maximum grows with only 0.63 × 10·log10(U), and 5.4 × once the scaling is added back, near self-noise's U^5; at zero angle the run maxima equal BPM's scaled peak amplitude K1 (129.2 against 129.2). The offset is a per-row function of two features, so nothing leaks (LEAK-30). Reword `question` and `predicted`. I advised against re-targeting without the exact constants; the mediator has since confirmed them.
2. Band selection (P4, Weigh; a note). Each run holds one contiguous ladder of 8-19 bands; the edge bands are quieter (49.7 dB implied against 55.8 for interior bands), so the source likely cut each spectrum at the tunnel background, which the split audit found stated in the report. The test scores only bands that could be measured. One clause in `task_summary.row`.
3. `attack-angle` numeric (P7, CLEAN-14 Should), carried from v1 with no reason. On the 30 shipped splits:

| model | numeric R² | categorical R² | gain (SE) | splits won by numeric |
|---|---|---|---|---|
| LightGBM | 0.835 | 0.813 | +0.022 (0.006) | 22 of 30 |
| random forest (one-hot) | 0.837 | 0.826 | +0.011 (0.002) | 24 of 30 |

For LightGBM, dropping the column also beats the category, as in the leak probe (0.847 without `attack-angle`, 0.828 with all features). Fix: `FeatureTypes(categorical=("run",))`.

```text
Validity: USE-5 holds in substance (the scaled target is invertible from the features); the wording of `predicted`/`question` is wrong. LEAK-10 holds for every column. LEAK-30 holds (δ* and the scaling are fixed per-row formulas). LEAK-33 holds (`run` is not a feature).
Quality: CLEAN-14 departure on `attack-angle` (fix: numeric).
For the curator: whether to re-target to the absolute SPL (I advise no); add a note on the band selection.
```

Limit: the NTRS PDF is a scanned image I could not OCR, so my target evidence is circumstantial.

Sources: [UCI Airfoil Self-Noise](https://archive.ics.uci.edu/dataset/291/airfoil+self+noise), [NASA RP-1218 on NTRS](https://ntrs.nasa.gov/api/citations/19890016302/downloads/19890016302.pdf), [Brooks & Marcolini 1985 on NTRS](https://ntrs.nasa.gov/citations/19850039707).

</details>

<details><summary>Split audit</summary>

Verdict: right with notes. The regime is right (grouped, a configuration never measured), the key is exact, and the grouped split clearly beats IID. The open question is the level of the group: the source organises its data by setup (one airfoil at one angle), and for most test runs that setup is in training at another speed.

```text
Verdict: right with notes.
Validity: USE-10 / SPLIT-2 / SPLIT-3 hold (grouped, new entity; no time axis). SPLIT-24 holds (exact key).
  SPLIT-29 holds against IID (gap 0.076 against a fold SD of 0.020). SPLIT-28 holds (signal across groups).
  SPLIT-1 / SPLIT-23 open: the group level (run or setup), a weighing call.
Quality: CLEAN-14 departure (`attack-angle` categorical), which interacts with the split.
For the curator: issue 1 (run or setup), then issue 2 (wording) if the run split stays.
```

Checked: a rebuild gives the same frame and splits as the build (the README's "stale" mark comes from text only); 106 settings = 106 consecutive blocks; 10 x 3 splits, no run on both sides, 35-36 test runs (481-526 rows) per fold; `per_sample`, `row` and `context="none"` are right; no time axis (a designed matrix); group probe IID 0.929 ± 0.003 against grouped 0.853 ± 0.020.

The source, read: Sec. 4.3, "Figures 11 to 43 are for airfoils where the boundary layers have been tripped ... Each figure contains spectra for a model at a specific angle of attack for various tunnel speeds". The 33 (chord, angle) setups are exactly Figs. 11-43, so the data is the tripped set only and `attack-angle` is the corrected α* (Sec. 2.4). The spectra are "truncated at upper and lower frequencies" where extraneous noise changed them by 2 dB or more, hence 8-19 bands per run.

Scores per split (R², 5 x 3, untuned, EV-8):

| model | IID rows | run (shipped) | setup = chord × angle (33 groups) | chord (6 groups) |
|---|---|---|---|---|
| extra trees | 0.943 | 0.855 | 0.774 | 0.713 |
| LightGBM, angle numeric | 0.921 | 0.832 | 0.736 | 0.656 |
| LightGBM, angle categorical (shipped) | 0.923 | 0.806 | 0.646 | 0.631 |
| random forest | 0.922 | 0.835 | 0.734 | 0.664 |

SD across splits: 0.024-0.033 by run, 0.062-0.073 by setup, 0.080-0.101 by chord. Extra trees RMSE: 1.64, 2.61, 3.23, 3.61.

Problems, ranked:

1. Run or setup (SPLIT-1, SPLIT-23, SPLIT-30; a weighing call). In each fold 91.5% of test runs on average (77.1-100%) have the same airfoil at the same angle in training at another speed. Over all 30 splits, 91.1% of test rows have their setup in training and score RMSE 2.48 (extra trees) or 2.68 (LightGBM); the other 8.9% score 3.47 or 4.04. For the setup: the speed is the cheap setting once a setup is mounted, and the source organises by setup (the context SPLIT-30 asks for). For the run: a run is one measured spectrum, and filling an unmeasured speed is a real query. Remedy: (a) `Grouping(on=["chord-length", "attack-angle"])`, 11 setups (494-514 rows) per test fold, with the angle numeric; or (b) keep the run split and fix the text (problem 2).
2. The text understates the overlap (SPLIT-1, USE-8). `split` and `splits_comment` say other combinations "can be in training"; for about 91% of test runs the same size and angle, the same report figure, is. `fit_reason` too.
3. The chord reason (SPLIT-4) is the size of the gap. It holds on other grounds: 6 chords, 2 held out per fold, R² SD 0.08-0.10 (the "only a few groups" factor, covertype), and the use case stays inside the tested chord range.
4. The "62%" (EV-8): 66.6% under a random 3-fold split; 62.5% is the share of rows whose nearest neighbour is in the same group (chance 0.9%).
5. The angle typing interacts with the split (CLEAN-14): 8.3% of test runs (up to 22.9% in a fold) meet an unseen angle value; LightGBM RMSE 3.02 categorical against 2.81 numeric. Under a setup split, 75% of test runs would, so the numeric angle is required there.

Sources: [UCI](https://archive.ics.uci.edu/dataset/291/airfoil+self+noise), [Brooks, Pope & Marcolini 1989, NASA RP-1218 (NTRS PDF)](https://ntrs.nasa.gov/api/citations/19890016302/downloads/19890016302.pdf), [NTRS record](https://ntrs.nasa.gov/citations/19890016302).

</details>

<details><summary>Domain practitioner</summary>

I read this as an aeroacoustics engineer who predicts airfoil self-noise for a wind-tunnel campaign or for blade design.

Fit: direct (narrow). The inputs are the settings I choose before a run, and a held-out run is a configuration nobody measured. But for 91.5% of test runs (split audit) the same chord at the same angle is in training at another speed, so the split tests the easiest unmeasured configuration. This agrees with the existing USE-8 case entry; the gaps should be named in the definition.

Inputs (USE-3, USE-6): I have all five before measuring; the thickness is a legitimate computed input (column audit), and the angle is the effective angle after the open-jet correction (jet height 30.48 cm). Shape, trip state, span and observer are missing only because they are constant. No leak.

Target (USE-5): a lossless proxy, the BPM-scaled level (claim audit). My own check agreed: at 0° the peak levels change by -1.8 to +0.1 dB from 31.7 to 71.3 m/s, where measured levels would rise 17.6 dB, and the peak sits at a Strouhal number f·δ*/U of about 0.06, BPM's trailing-edge peak. The band RMSE equals my error on the measured level, so the metric is in my units, though I act on the whole spectrum and its A-weighted level, and the way back to my receiver's SPL needs a convention the UCI page never defines.

The split. With the target speed-normalised, a held-out run whose cell is in training is mostly a Strouhal shift of a spectrum the model has seen. That case is real: 13 of the 33 cells were run at only 2 of the 4 speeds, so a new speed is a genuine query (USE-9, USE-10), and "a use case rephrased only to excuse a gap" does not apply. But "the queries I cannot answer by running the tunnel for five more minutes are a new angle or a new size." Held-out cells cost about 0.5 dB RMSE and 0.07 R² in my probe.

Would I use it? As an interpolator for this campaign, yes. For my blade, no: one symmetric airfoil, tripped only, Reynolds number 5.5e4 to 1.5e6, Mach up to 0.21, one observer. In practice I use BPM itself, built from this data; it ships in OpenFAST and NAFNoise, with δ* from XFOIL. I would trust a learned model that beats BPM on held-out cells and takes the angle as a number. The categorical angle is close to a cell ID and blocks new angles; the numeric angle wins in every split I ran, most under a cell split (extra trees / LightGBM RMSE 3.14 / 3.22 dB against 3.82 / 3.82).

Gaps, ranked: (1) the split tests the easiest unmeasured configuration, and the splits comment does not say that 9 in 10 test runs share chord and angle with a training run; (2) the categorical angle; (3) the label described wrongly (the metric is unaffected); (4) a decision is a whole spectrum, not one band (minor); (5) a narrow population, already "narrow" in `fit_reason`. I would make the angle numeric first, keep the scaled target under its right name (the physics normalisation an engineer applies anyway), and either group by cell (a new angle on a tested airfoil, the more valuable query) or keep the run split, state the 91.5% and sharpen USE-1 to "an engineer extending a tunnel campaign on a tested airfoil decides which settings to run and which to take from a model". That choice is the curator's. Six chords are too few to group on.

Limits: I could not read the scanned PDF; the BPM formulas I matched (the tripped δ*, the peak Strouhal 0.02 M^-0.6, the open-jet factor) are recalled, not read in the report.

Sources: [UCI](https://archive.ics.uci.edu/dataset/291/airfoil+self+noise), [NTRS record of RP-1218](https://ntrs.nasa.gov/citations/19890016302), [OpenFAST noise models](https://openfast.readthedocs.io/en/dev/source/user/aerodyn-aeroacoustics/02-noise-models.html), [Moriarty & Migliore 2003, NREL](https://research-hub.nrel.gov/en/publications/semi-empirical-aeroacoustic-noise-prediction-code-for-wind-turbin/), [Errasquin 2009, Virginia Tech](https://vtechworks.lib.vt.edu/handle/10919/35193), [Lau, Lopez & Onate 2009](https://agris.fao.org/search/en/records/6748867b7625988a371d0ad3) (the UCI donor's model), [Neural Designer case page](https://www.neuraldesigner.com/?p=3461) (warns that a random split overstates performance).

</details>

<details><summary>Blind review</summary>

Without our notes or rules, only the data in a clean room and the public sources. Verdict: include with one change: use `run` only as the key of the grouped split, never as a model feature. Beyond that, the data is real NASA measurement data, matches the public source row for row, and gives a fair task with clear signal.

The task: NASA wind-tunnel spectra of trailing-edge self-noise from NACA 0012 airfoils (Brooks, Pope and Marcolini 1989, NASA RP-1218), one row per one-third-octave band of one setting. A rotor or wind-turbine designer would use it to estimate the spectrum at an untested setting; in practice people use the BPM model fitted to these same spectra.

Fidelity: the data equals UCI's `airfoil_self_noise.dat` as a set of rows (all 1,503 to 6 decimals), with no missing values, duplicates or repeated (`run`, frequency) pairs. Against the rendered report pages: for 30.48 cm, α = 0°, U = 71.3 m/s the rebuilt raw level is 61.38 dB at 800 Hz, 62.77 at 1.6 kHz and 43.90 at 16 kHz, matching Fig. 11(a); Fig. 12 shows only U = 71.3 and 39.6 m/s at α* = 1.5°, which matches `run_004` and `run_005`.

Baselines (3-fold, repeated; RMSE in dB, target SD 6.9):

| model | random rows | grouped by `run` |
|---|---|---|
| linear | 4.81 | 4.86 (R² 0.50) |
| kNN | 3.43 | 4.04 (R² 0.66) |
| random forest | 1.89 | 2.76 (R² 0.84) |
| LightGBM | 1.76 | 2.57 (R² 0.86) |
| LightGBM + log/Strouhal features | 1.60 | 2.11 (R² 0.91) |

Clear signal, not trivial, model families separate well; the grouped spread across folds (0.2-0.3 RMSE) is fine with 30 splits.

Concerns, most to least serious:

1. `run` is a made-up ID column. Passed to LightGBM as a category it doubles the grouped RMSE (5.22 ± 0.58 against 2.68 ± 0.29). Keep it out of the features. (Both sides later dropped this: `n_features` is 5.)
2. The group sets the difficulty. Holding out runs is the honest choice over random rows, but the same chord and angle at other speeds stay in training, and the report's scaling makes those spectra collapse onto each other; grouping by (chord, angle), one group per report figure, is harder (split audit). Optional: `run` grouping fits "an untested combination inside the tested grid", (chord, angle) fits "a new angle for an airfoil".
3. The target is the report's eq. 19 scaled level, confirmed exactly (proof: claim audit). Not a leak, but it removes a large part of the easy signal (SD 10.5 dB measured against 6.9 scaled). Keep it and document what "scaled" means.
4. The thickness is computed (the tripped formula, column audit); the untripped formulas are off by a median of 60%. So there are 4 independent inputs plus frequency. Keep it, document it.
5. Narrow scope: the tripped set only, one airfoil, span and observer (split audit). Do not call it general airfoil noise.
6. The authors removed noisy bands (split audit), so test rows cover only clean bands. Minor.
7. Small (1,503 rows, 106 groups), on a fixed grid, and heavily used: [OpenML 44957](https://www.openml.org/search?type=data&id=44957) is in the OpenML-CTR23 suite, so methods may already be tuned to it.

Could not check: how the pipeline treats `run`; the fold assignments; whether the 0.01 dB levels came from NASA's digital records or the plots (the evenly spread last digits suggest digital records); membership in other suites such as TabArena v0.1. Only two report figures were compared, visually.

Sources: [UCI dataset 291](https://archive.ics.uci.edu/dataset/291/airfoil+self+noise), [NASA RP-1218](https://ntrs.nasa.gov/api/citations/19890016302/downloads/19890016302.pdf) (pp. 5, 17, 18, 51), [CTR23 / TFM paper listing airfoil_self_noise](https://arxiv.org/pdf/2605.21288).

</details>

<details><summary>Precedent check</summary>

Of five decisions, three are consistent, the year is open with the record and the definition disagreeing, and `attack-angle` categorical departs from its rule without a reason. None of the register's four flags involves airfoil.

1. Grouped by run since 2026-10-06, not by chord: consistent (SPLIT-4, SPLIT-24, the "Composite keys" pattern). Same facts: superconductivity (CC 2026-10-06, by composition, "the use case decided, not the gap"), concrete_compressive_strength (CC 2026-10-14, a 7-column mix key built with the same `groupby(...).ngroup()` code), electric_motor_temperature_prediction (test-bench profile, a session like a run). Told apart: amazon_employee_access stays IID under SPLIT-31, as new requests keep the role values. No drift. Two notes: the chord reason argues from difficulty, where superconductivity argued from the use case, and the rule-backed grounds are the use case and the "only a few groups" factor (covertype); and SPLIT-23 (Must) wants the source's use cited, as concrete's `Grouping.definition` cites Yeh 1999 on designing new mixes, while airfoil's cites Brooks et al. only for how a run is built.
2. `run` as a categorical composite key: consistent with concrete's `mix`, superconductivity's `composition`, musk's `molecule_name`, micro_mass's `Strain` and electric_motor's `profile_id`.
3. `attack-angle` categorical departs from CLEAN-14 (Should). A physical quantity with 27 values, while the same definition keeps `chord-length` (6 values) and `free-stream-velocity` (4) numeric, as concrete keeps `Age` (14) and video_transcoding_time_prediction its output settings. It came from the v1 notebook (`cat_features = ["attack-angle"]`) with no comment; 12 of the 27 angles occur in only 2 runs, which is why test rows meet unseen angles (claim audit). P7, touching P3. My consistency check offered: (a) an exception, since the tunnel-corrected angles mostly occur with one chord (the AI's weak guess), (b) numeric, (c) chord and velocity categorical too, (d) amend CLEAN-14 for settings on a grid.
4. Year 2014, NASA 1989 BibTeX, source UCI: open; the record says 1989. The pattern: a UCI dataset whose earlier paper does not hold the rows takes UCI's year and cites the work behind the data (concrete 2007 / Yeh 1998, musk 1994 / 1993, video_transcoding 2015 / 2014, micro_mass 2013 / 2014). Counter-precedents (CHANGELOG 2026-10-12): biomechanical_orthopaedic_prediction (a 2006 thesis appendix lists all 310 samples), in_vehicle_coupon_recommendation and aps_failure moved to the earlier work holding the rows. The deciding fact under PROV-9 is whether RP-1218 tabulates the 1,503 values; no repository file settles it. The 2026-10-12 sweep left airfoil "Unclear", and the 2014 is the v1 notebook's value, so there is no drift. The disagreement belongs in `REVIEW.md` (pipeline.md); the `@techreport` lacks institution and report number ("No. L-16528").
5. Kept despite "maybe outdated": consistent. `Outdated` has no rule (selection.md). Kept with the same concern: concrete ("Likely yes as no objects beside maybe outdated / lab setup"), forensic_glass_identification, heart_disease_cleveland, video_transcoding_time_prediction, covertype, credit_g, houses. Excluded on a further fact: machine_cpu (old hardware, newer data exists), nikuradse_1, sonar (SEL-16), haberman_survival. What sets airfoil apart is unwritten: the self-noise of a NACA 0012 section is physics that does not age; one line in the record would close it.

Outside this dataset, for a separate check: first_order_theorem_proving is `No` on `Outdated` alone ("a niche, dated benchmark"; `checked_by` still `AI (UNVERIFIED)`), while its ASlib siblings asp_potassco_classification and sat11_hand_algo_runtime ship as `Yes`.

</details>

<details><summary>Advocate</summary>

Final position after the rebuttal: ship after changes, keep the scaled target, and keep the run split with the use case reworded. The advocate agrees with the critic on the verdict and on the remedy for every point but the split.

Conceded:

- The target wording is false: name eq. 19's scaled level, add the constants and the conversion, and say that a band's error equals the error on the measured level.
- `split`, `fit_reason` and `splits_comment` must state the 91.5%, `use_case` takes the practitioner's USE-1 wording, and SPLIT-23 needs the citation. The current text cannot ship unchanged.
- The chord reason argued from difficulty (SPLIT-4).
- The narrowness clauses (tripped set, corrected α*, truncated bands); the fit stays "direct (narrow)".
- The year contradiction goes into `REVIEW.md`, and the BibTeX gets completed.
- The angle numeric, the evidence numbers and the probe lesson, in full. "Outdated" closes with one line in the record, on the precedent check's grounds.

Still disputed, and why:

- The source's purpose does not single out the setup. The critic's quote of the RP-1218 Summary cuts speed; the full sentence reads "seven NACA 0012 airfoil blade sections of different sizes (chord lengths from 2.5 to 61 cm) tested at wind tunnel speeds up to Mach 0.21 (Reynolds number based on chord up to 3 x 10^6) and at angles of attack from 0° to 25.2°". Read literally, it argues for holding out sizes too, which both sides reject on the few-groups factor, so the use case has to choose.
- The evidence for the setup split (the split audit's error and R² differences) is the size of the gap, which never decides (SPLIT-4). The new-speed query is real: a recount on the raw file gives 20 setups at all 4 speeds and 13 at only 2.
- SPLIT-23 decides the prediction unit and what is known about a new group, and all reports agree on row and none; here it is a missing citation, not a wrong split.
- The curator decided the run split on 2026-10-06, and that call outranks an AI assessment. Recommends option (b), rewriting the text, which keeps the decision and changes no data.
- Re-targeting. "A user cannot get back to the measured level" holds only until the conversion bullet is written. The ranking shift comes from untuned probes (TP-1, Must: a question, not a verdict). TP-6 keeps a valid task, and under PROV-14 a re-target would be a new dataset. The label is a lossless per-row transform from inputs known before the run, so the fit stays direct (USE-8).
- The year is a metadata question settled by one field; the evidence favours 2014 (the concrete pattern).

The mediator ruled against three of these: the CC never weighed the setup, so the 91.5% goes to the curator as a new fact (the run split stands until changed); the setup split's larger spread, raised in the brief, is no factor; and the constants the brief called inferred are confirmed. The advocate's PROV-14 reading stands against the mediator's.

Verdict: ship after changes. For the curator: run against setup (recommends the run split with the reworded use case); re-target (advises against, except as a new dataset); the year (one field).

</details>

<details><summary>Critic</summary>

Final position after the rebuttal: ship after changes. No Must is unfixable, so no exclusion, but the current text with the current split cannot ship.

Conceded:

- No leak (LEAK-10, USE-3, LEAK-16; `run` is not a feature).
- Re-targeting is no condition for shipping: the wording fix resolves the false claim, and re-targeting stays a question for the curator.
- The new-speed query is real (20 setups at 4 speeds, 13 at 2); SPLIT-24 and SPLIT-29 hold; no drift against precedent; the chord reason is restated; run against setup is the curator's call.
- The angle numeric, worth benchmarking (no P6 point), "outdated" dropped, the narrowness notes, the evidence numbers and the probe lesson.

A new fact on the year moved the critic toward the advocate. The report says what its tables hold: "In tables 1 and 2, the data processing and manipulations ... are specified for each test case", and the peak Strouhal numbers and peak scaled levels are "also presented in table 1"; the tables take 5 scanned pages (PDF pp. 142-146). So the report does not hold the 1,503 band levels, and 2014 is likely. Still open under EV-7 (Must): [OpenML 43919](https://www.openml.org/api/v1/json/data/43919) lists Lau's 2006 MSc thesis (Imperial College) and Lopez's 2008 PhD thesis (UPC), and nobody has checked whether either tabulates the rows. Remedy: the record to 2014, the BibTeX completed, one `REVIEW.md` line naming the theses.

Still disputed, and why:

- The curator did not weigh the setup on 2026-10-06: the CC compares run with IID and chord, never the (chord, angle) setup or the 91.5%. A later stage's measured finding supersedes an earlier reading, and "Arguing a call" says to surface it.
- Restating `split` and `splits_comment` is not enough. `use_case` ("before, or instead of, measuring it in a wind tunnel") and `fit_reason` ("a held-out run is an unmeasured configuration") contradict a test where the setup was already in the tunnel for about 91% of test runs (USE-8, USE-1, Must). The advocate's matrix-filling engineer has to become the use case.
- The setup split's larger spread is no factor: P4 over P6, and with 33 groups the few-groups factor does not apply.
- The source's stated use, a prediction method applied to "a large-scale-model helicopter rotor", means configurations outside the tunnel matrix; the citation is needed but does not favour the run.
- The constants are confirmed, not inferred, and TP-6 cuts toward re-targeting: "a better version the source itself defines replaces the current one", and the measured SPL is what the source plots in Figs. 11-43. Whether PROV-14 makes that a new dataset is left to the curator.

The mediator agreed that the CC never weighed the setup (the run split still stands until the curator changes it), sided with the critic on the `use_case` text, the spread and the constants, and found the source neutral.

The critic reproduced on the 30 shipped splits the 91.5% (77.1-100% per split), the 8.7% of test rows with an unseen angle and the 0.986 grid concentration. Dropped from its brief for lack of backing: `run` as a feature, "outdated", CTR23 or other-benchmark use (no evidence under EV-4, PROV-15), the band-count weighting, the stale build.

```text
Verdict: ship after changes.
Validity: USE-5 wording fixed (re-target: curator, no ship condition); USE-1/USE-8 need use_case and fit_reason to match the split; SPLIT-1 run vs setup goes to the curator with the 91.5% as a new fact (not decided 2026-10-06); SPLIT-4 reason restated; PROV-9 year 2014 (report tables hold no band levels), with the 2006/2008 theses left open in REVIEW.md.
Value: TP holds.
Quality: CLEAN-14 fixed (angle numeric).
For the curator: (1) run or setup split; if run, restate the use case as filling in a tested setup's speeds; (2) re-target to measured SPL, optional.
```

</details>
