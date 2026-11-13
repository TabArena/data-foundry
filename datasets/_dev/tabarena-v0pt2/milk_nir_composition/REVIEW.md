# milk_nir_composition

**Outcome:** added; the AI recommends shipping it. Milk fat (% w/w) of one milking from an on-farm near-infrared transmittance sensor on a milking robot,
41 Holstein cows on one Belgian farm over eight weeks in 2017 (1,224 milkings), from the authors' Zenodo deposit with a
data paper; four weekly test windows with an expanding calibration, RMSE as the source's RMSEP. The panel found that
the deposit's normalised spectrum was referenced with the mean dark and white readings of the whole trial week, later
milkings and other test rows included; a test milking's spectrum therefore drew on readings up to 45 hours later (85 in
week 1). We rebuilt it from the deposit's raw counts with each milking's own dark and white readings, the preprint's
default. This change is made and needs no decision. It costs ridge 0.0983 to 0.0996 RMSE on the four windows. If you
prefer the data paper's procedure (one pair held per half hour, 0.0982), switching to it is a one-line change. The
columns now sit on the source's nominal 960-1690 nm axis instead of numbered pixels.
Verdict: ship after changes (made).
Validity: SEL-1, SEL-15 hold; USE-1, USE-5, USE-8 hold (fit direct); LEAK-10 triggered, fixed (`Prot`, `Lact`, `SCC`,
`Urea` dropped); LEAK-30 / PROV-13 triggered (the deposit's `Trans_Tot` uses the week's mean references), fixed by the
rebuild from each row's own pair (PROV-14: same units, same 256 positions); EV-2 triggered (false notes on the
referencing, the "%" and the axis), fixed; SPLIT-3, -9, -10, -11, -13, -14, -17 hold; SPLIT-19 yields to SPLIT-14 (a
Must); USE-10 holds (a known herd).
Value: the task probes flag nothing (on the rebuilt spectrum, ridge 0.0996 against the train mean's 0.798, better on
4 of 4 windows); MET-5 holds (RMSEP). A window's level hinges on one or a few milkings (noted, kept).
Quality: CLEAN-26 axis declared as the source's nominal nm; CLEAN-11 fresh cows kept (issue 3); CLEAN-22 reason for
the sensor-timestamp drop corrected.
Weighed: gap 0, use case +, source +, shape +, risk 0.
For the curator: issue 1 (the raw instrument readings), issue 2 (`cow_id`), issue 3 (the fresh cows); the two lines for
the spectrum guide are an across-datasets item; three record fields (`required_split`, `domain`, `tag`).

**Main points:** Three calls: leave the sensor's 768 raw readings out, as the definition does now, or ship them as three
more spectra (issue 1, a weighing call; leaving them out is recommended); keep `cow_id` (issue 2, recommended); keep the
59 samples of the five fresh cows (issue 3, recommended).

**Record fields that disagree with the definition:**

- `required_split`: record `(none)`, definition `Temporal (NON-IID)`.
- `domain`: record `(none)`, definition `chemistry & material science`.
- `tag`: record `(none)`, definition `Non-IID (Temporal)`.

**Record judgment:** valid. The authors' own CC BY 4.0 deposit (Zenodo 8263430) with a data paper (Data in Brief 2023)
and a research article (Comput. Electron. Agric. 2020, read as its preprint) that name the actor, the moment and the
metric; the article's Table 3 is reproduced exactly from the deposit. The screening's "`Trans_Tot` in %" is the source's
percent-transmittance convention, and its "fat may have missing values" does not hold for the deposit (fat on all 1,224
rows). The priority moves from 3 to 4 (gap 0, use case +, source +, shape +, risk 0).

**Issues for Lennart:**

1. **Ship the sensor's 768 raw readings (sample, dark and white counts) as three more spectra?**

   * **Problem:**
     - The deposit holds each milking's raw sample counts and its own dark and white reference readings (256 pixels each), all known when the sensor's cycle ends, and the definition now builds the shipped spectrum from them but leaves the three blocks themselves out.
     - The rules count anything known at the prediction point as a legitimate input whose removal changes the task[^use6], and ship a spectrum as the source publishes it so that a method that processes spectra itself keeps the signal[^c26].
     - Against them, the source's on-farm models read the normalised spectrum only, and the blocks alone carry no measured signal on fat.
   * **Background:**
     - Referencing turns raw counts into transmittance: (sample - dark) / (white - dark), where the dark is the detector's reading with no light and the white its reading through a reference material (Spectralon).
     - How often to take the references and whether to average them is a choice; the data paper names the reference frequency as a research use of the deposit.
     - The deposit's own normalised spectrum used the mean references of the whole week, later milkings included, which is why the definition rebuilds it from each milking's own pair (the outcome above).
   * **Effect on the task:**
     - With the blocks, a method may pick its own referencing (another frequency, an average over past milkings, a learnt correction); without them every method reads the one referencing the definition ships.
     - The rebuilt spectrum is computed from the blocks, so each milking's own references reach the model; the absolute count levels do not, and their worth was not measured.
   * **Experiments:**
     - Ridge on a milking's dark, white or white - dark alone scores as the train mean (RMSE 0.719-0.867 against 0.720-0.872 on the four windows).
     - Three causal referencings as spectra, mean RMSE over the four windows (ridge / PLS with 15 components / PLS with 30 on the first derivative): own pair 0.0996 / 0.1125 / 0.1017, mean of the past 30 minutes 0.0997 / 0.1097 / 0.1028, one pair held per 0.5 h 0.0982 / 0.1123 / 0.1001; the differences are 1 to 2.5 standard errors of a bootstrap over cows and change sign by model, so on these windows a different referencing, the freedom that shipping the blocks would give, gains nothing measurable.
     - No model reading the blocks beside the rebuilt spectrum was run.
   * **Consistency:**
     - open_soil_spectral_library left out the depths and preparation code a laboratory knows, because the source's scan service accepts none of them[^os]; here the robot holds the readings itself, so that precedent does not carry over.
     - No precedent has these facts, so your call sets one for the next near-infrared or Raman source that publishes reference blocks beside a normalised spectrum.
   * **Panel:**
     - For shipping (no agent asked for it; the critic and the precedent checker asked that these rules stand beside option A): the robot holds the readings, and leaving a known input out changes the task.
     - Leave out (the builder, the domain practitioner, the advocate): the farm's model reads the normalised spectrum, and the blocks add no measured signal.
     - The mediator leaves it to you as a weighing call; the width of the table is no argument either way.
   * **Unknown:** whether a model reading the blocks beats the rebuilt spectrum; ridge on the rebuilt spectrum plus the blocks, or a learnt referencing, on the four windows would settle it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Leave the blocks out (implemented) | the rebuilt spectrum (256 columns) and the five robot fields: 261 features | what the source's on-farm models and the practitioner read; every milking's own references reach the model through the spectrum; the blocks alone predict nothing | a known input left out; no method can choose its own referencing |
     | B | Ship them as three more spectra | `Trans_Sample`, `Trans_Dark`, `Trans_White` declared as three spectra in counts on the same nominal axis, beside the rebuilt spectrum: 1,029 features | every reading the robot holds; the data paper's research question open to methods | no measured gain; the source's models never read them |

   * **Recommendation:** A: the rebuilt spectrum already carries each milking's own references, the blocks alone predict nothing, and the source and the practitioner deploy the normalised spectrum; B if you hold that the choice of referencing belongs to the methods. **Decision:** A or B?

   **Notes for the AI:** on B, in `_clean` keep `SAMPLE`, `DARK` and `WHITE` renamed to `counts_sample_<nm>`, `counts_dark_<nm>`, `counts_white_<nm>` on the nominal axis (a prefix that does not start with `nir_`, which the main spectrum takes), and declare three more `Spectrum(..., unit="nm", technique="near_infrared", state="raw")` in `special_features`; rewrite the blocks bullet of the notes, `task_summary.known` and `changes`; re-run `dataset check`, the leak, task and hidden-group probes. On A, a CC line in the record naming the call as the precedent for reference blocks.

   [^use6]: **USE-6** (Must): anything known at the prediction point is a legitimate input; "dropping it changes the task into predict without ...".
   [^c26]: **CLEAN-26** (Should): a spectrum ships as the source publishes it, one numeric column per position; processing is left to the benchmark's encodings, so "a method that processes spectra itself" keeps the signal. CLEAN-22 (Should) allows dropping columns that add nothing a method needs.
   [^os]: open_soil_spectral_library (Lennart, 2026-11-05, issue 6): the depths and preparation code left out as "a choice of actor", the source's scan-upload service accepting none of them.

2. **Keep the cow's id as a feature?**

   * **Problem:**
     - The robot identifies every cow, and 98.1% of a window's test milkings on average (98.8% pooled) are of a cow seen in training, so the definition keeps `cow_id` as a category[^u10].
     - A model that leans on the cow could predict close to her usual fat and under-report the deviations a farmer acts on.
   * **Effect on the task:** with the id a tree can learn each cow's level, while the linear spectral models gain nothing; without it the task becomes a calibration that ignores which cow is milked, another product (one calibration for any herd).
   * **Experiments:** on the rebuilt spectrum and the four windows, untuned LightGBM scores 0.274 without the cow and 0.215 with it; PLS with the source's per-cow bias correction 0.1047 against 0.1052 without; the cow's training mean alone 0.575 against the dummy's 0.798; the cow's last training-side fat adds nothing to ridge (0.0984 against 0.0986, on the deposit's spectrum; the panel's 0.267 and 0.213 for LightGBM were on the deposit's spectrum too).
   * **Consistency:** wisconsin_local_government_property_insurance_fund (`PolicyNum`), sendy_logistics_challenge (`Rider Id`) keep the id of an entity the actor knows under a temporal split, as does uniform_soybean_tests_yield (`genotype`) of this batch, not yet decided[^prec2]; this follows them.
   * **Panel:** No agent disagreed; the domain practitioner names the shrinkage toward the cow's level as the one reason to distrust such a model.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep `cow_id` (implemented) | the cow as a categorical feature, 41 levels | the robot knows the cow; the source's real-time evaluation kept every cow on both sides and tried a per-cow correction; follows wisconsin and sendy | a tree can lean on the cow's level |
     | B | Drop `cow_id` | 260 features | tests a calibration that holds for any cow | leaves out a known input; not the product the source evaluates |

   * **Recommendation:** A, a known input of the robot's own herd. **Decision:** A or B?

   **Notes for the AI:** on B, add `"Cow_ID"` to the dropped columns in `_clean` (remove it from `RENAME` and `_feature_types`), rewrite the kept-features bullet and `task_summary.known`; re-run `dataset check` and the task and hidden-group probes.

   [^u10]: **USE-10** (Should): for a known entity the split is temporal and the entity's id and history are legitimate inputs; **SPLIT-13** (Should): entities that recur in deployment may recur across the split.
   [^prec2]: wisconsin_local_government_property_insurance_fund (Andrej, 2026-11-02; definition reviewed by Lennart): `PolicyNum` an input, 97.6-98.8% of test members seen. sendy_logistics_challenge (Myunghwan, 2026-10-29; shipped with PR #33): `Rider Id` and `User Id` inputs, 99.1-99.4% seen. uniform_soybean_tests_yield (this batch, not yet decided by a curator): `genotype` kept as a category, "a breeder knows which line a plot is".

3. **Keep the 59 samples of the five fresh cows?**

   * **Problem:**
     - The research article of 2020 removed 59 samples of four cows that calved during the trial and one under five days in milk "to avoid the inclusion of colostrum samples", while the data paper, the data's first publication, releases them; the definition keeps them[^c11].
     - Their milk is not colostrum (protein at most 3.88%, colostrum's far above 10%), and they are early-lactation milkings, the cases health monitoring is for.
   * **Background:** the deposit has no days in milk; without these five cows it gives the article's Table 3 exactly (week 1: 308 samples, weeks 2 to 8: 857), which identifies them.
   * **Effect on the task:** kept, the test windows hold the hardest milkings a robot meets after calving (the largest fat value, 7.6%, cow 55394 in week 8, against the article's maximum of 6.25%); dropped, the task is the article's population of established cows.
   * **Experiments:**
     - As training rows they change nothing: PLS 0.1053 trained with them against 0.1055 without, on the same test milkings of the other cows (four windows).
     - As test rows they hold 30% of week 8's squared error under ridge on the rebuilt spectrum (39.5% on the deposit's, in the panel's reports; four-window mean 0.0996 with them, 0.0985 without).
     - A fat-to-protein ratio above 1.4, a sign of ketosis, occurs in 11.9% of their samples against 2.0% of the others.
   * **Consistency:** ames_housing dropped De Cock's partial sales because the data's own publication recommends it[^prec3]; here the first publication releases the samples and the use case meets fresh cows, so keeping them follows the default.
   * **Panel:** No agent disagreed; the domain practitioner gave the composition and ratio evidence, the claim auditor reproduced Table 3.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep them (implemented) | 1,224 milkings of 41 cows | the data as first published; normal milk; the early-lactation cases monitoring is for | departs from the article's population |
     | B | Drop them | 1,165 milkings of 36 cows, the article's population | matches the article's results | removes real milkings the robot meets; the article's reason (colostrum) does not hold for this milk |

   * **Recommendation:** A, the data paper's release and the robot's real herd. **Decision:** A or B?

   **Notes for the AI:** on B, drop the rows of `FRESH_COWS` in `_clean`, turn the `_decisions` entry into a drop with the same table, rewrite the fresh-cow bullet and the split sizes in `splits_comment` (the windows lose 20, 18, 6 and 0 test milkings); re-run `dataset check` and every probe.

   [^c11]: **CLEAN-11** (Should): an unusual row stays; a row whose target the source names as not the task's quantity "may leave, with the source's words".
   [^prec3]: ames_housing (Lennart, 2026-10-21): the partial sales dropped on De Cock's own recommendation in the data's publication. open_soil_spectral_library (Lennart, 2026-11-05): three layers above 70% organic carbon kept, unusual but not impossible.

**Review panel:** ship after changes (mediator). Full tier: the claim, column and split auditors, the domain
practitioner, the blind reviewer, the task gamer and the precedent checker, then the advocate and the critic with one
rebuttal each, and the mediator, who ran the decisive experiment on six referencings of the spectrum with four models.
Claims: 43 audited; no validity claim refuted; refuted or overstated and now fixed: Table 1's "%" as a slip (it is the
source's percent-transmittance convention), the reason for numbered bins (the nominal axis matches the source within a
pixel), "cannot" for week 4 and the week-spacing wording; the fresh-cow identification is now measured (Table 3
reproduced). The column auditor found that the deposit's spectrum is referenced with the week's mean readings (exact to
5e-15 in four weeks), against the notes' "per session and every 0.5 h, cannot be rebuilt": the spectrum is now rebuilt
with each milking's own pair. Blind review: include with changes; its concerns were the datetimes as raw features
(left to the pipeline, as for nyc_taxi) and declaring the spectrum (done). Task gamer: no exploit beyond noise (about
0.001 RMSE). Agreed: ship, the rebuild from the raw counts, the false notes rewritten, the nominal nm axis, the notes on
the single 2.59% milking and on the fresh cows. Disputed: which causal rebuild (settled: the milking's own pair, the
source's definition, over a 30-minute mean of our own), the source's 0.0826 as headroom (settled: it is another
protocol, ridge 0.101 on it), a note on another benchmark's results (settled: none); the raw readings (issue 1).

<details><summary>Mediator</summary>

```text
MEDIATOR REPORT: milk_nir_composition (2026-11-09)
Panel: full tier (claim, column and split auditors, domain practitioner, blind reviewer, task gamer, precedent
checker; advocate and critic with one rebuttal each). Decisive experiment: the run folder, output
rebuild.log / rebuild.json (threads capped at 4).

1. RECOMMENDATION (judgment record)

  Verdict: ship after changes.
  Validity: SEL-1, SEL-15 hold; USE-1, USE-5, USE-8 hold (direct fit); LEAK-10 triggered, fixed (Prot, Lact, SCC,
    Urea dropped); LEAK-30 / PROV-13 triggered (Trans_Tot referenced with the week's mean dark/white, test rows and
    readings up to 85 h later included), fixed by rebuilding nir_bin_* from each row's own dark/white pair (PROV-14:
    same units, same 256 features); EV-2 triggered (false notes), fixed by rewriting; USE-6: the block drop's premise
    is false, corrected, the drop itself stays a weighing call; SPLIT-3/9/10/11/13/14/17 hold; SPLIT-19 yields to
    SPLIT-14 (Must), no exception needed; USE-10 holds (known herd).
  Value: TP no flags (ridge 0.098-0.100 vs dummy 0.798, 4 of 4 windows; family spread 3.5-7 SE); MET-5 rmse holds.
    A window's level hinges on one or a few milkings (note, no drop).
  Quality: CLEAN-26 axis back to the guide (nominal nm, option b); CLEAN-11 fresh cows kept (default); CLEAN-22
    timestamp drop reason corrected.
  Weighed: gap 0, use case +, source +, shape +, risk 0.
  For the curator: issue 1 the 768 raw instrument columns (weighing); issue 2 cow_id (keep, weighing); issue 3 the
    59 fresh-cow samples (keep, low); issue 4 a spectra.md line for range-and-step axes (rule maintenance).

2. AGREED FACTS (no agent disputes these; numbers re-measured where marked "m")

  a. Deposit: Zenodo 8263430 v0.0.1, md5 7cd61315..., 1,224 x 1,038, no missing value; values and order equal the
     container's (claim auditor T8; blind reviewer).
  b. Trans_Tot = (S - mean_week(D)) / (mean_week(W) - mean_week(D)): to 5.3e-15 in weeks 2, 3, 7, 8; off by 1.8e-4
     to 2.1e-3 in weeks 1, 4, 5, 6, the weeks missing the 46 unlabelled samples (column auditor a8; m). Each test
     window is one whole week, so a test row's spectrum depends on the other rows of its window and on readings up
     to 45 h later (85 h in week 1). The data paper and the preprint describe per-sample or 0.5 h referencing; the
     deposit does neither (PROV-13 mismatch to record).
  c. No label path: the reference blocks alone predict the train mean (ridge 0.719-0.867 vs 0.720-0.872).
  d. Own-pair ratio (S - D)/(W - D) is strictly positive on all 1,224 x 256 cells (min 0.0011, max 8.01; min W - D
     185 counts, min S - D 6) (m): the rebuild needs no clipping.
  e. Sensor cycle: sample read 39-107 s, dark 54-122 s, white 71-144 s after milking end (m); the dark/white come
     after the sample, against the paper's "before".
  f. The "%" in Table 1 is the source's percent-transmittance convention (its absorbance 4-5 at 1450 nm =
     log10(100/T)), not a slip (claim auditor T2).
  g. The nominal axis 960 + 2.86 (p - 1) nm puts the source's removed 1360-1500 nm window at 1360-1492 nm, within
     about one pixel; the band-maximum argument for bins rests on a pixel in noise (claim auditor T3).
  h. Split: 4 expanding windows = weeks 8, 7, 6, 5; train 1,062/894/810/644 (oldest 52.6%); gap 3 d removes no row;
     98.1% (mean of windows) / 98.8% (pooled) of test rows have a seen cow.
  i. Cow 50435, 2017-07-11 21:38, lab fat 2.59% (neighbours 4.3-5.5%) is 75% of week 7's ridge squared error;
     without it the four-window ridge mean is 0.080, with it 0.098. Fresh cows as test rows carry 39.5% of week 8's
     squared error (mean 0.096 without, 0.098 with).
  j. Dropping the five fresh cows reproduces the preprint's Table 3 exactly (308 / 857); their protein max 3.88%
     (not colostrum); FPR > 1.4 in 11.9% of them vs 2.0% of the rest.
  k. Source protocol (train week 1, test weeks 2-8, 1,165 samples) under our harness: ridge 0.102; the source's
     RMSEP 0.0826 used water-band removal, preprocessing and wavelength selection on that protocol.
  l. Task gamer: no exploit beyond noise (~0.001 RMSE); cow_id helps untuned trees only (0.267 -> 0.213), linear
     models not at all.

3. DECISIVE EXPERIMENT: which causal rebuild (disputed point 1)

  Four models on the four shipped windows, absorbance -log10(T); RMSE per window (w8 w7 w6 w5) and mean:

    variant               ridge   PLS-15  PLS-30 SG-d1  LightGBM+cow
    shipped (week mean)   0.0983  0.1095  0.0977        0.2152
    own pair              0.0996  0.1125  0.1017        0.2179
    trailing 15 min       0.0994  0.1110  0.1027        0.2130
    trailing 30 min       0.0997  0.1097  0.1028        0.2115
    trailing 60 min       0.0994  0.1102  0.1024        0.2100
    0.5 h hold (sessions) 0.0982  0.1123  0.1001        0.2136

  Paired difference to the own pair, four-window mean, cow-cluster bootstrap SE (1,000 draws):
    trailing 30 min: ridge +0.0001 (0.0013), PLS-15 -0.0028 (0.0016), PLS-30 d1 +0.0011 (0.0013), LGBM -0.0064 (0.0026)
    0.5 h hold:      ridge -0.0014 (0.0014), PLS-15 -0.0003 (0.0017), PLS-30 d1 -0.0016 (0.0018), LGBM -0.0044 (0.0034)
    shipped:         ridge -0.0013 (0.0026), PLS-15 -0.0031 (0.0019), PLS-30 d1 -0.0040 (0.0015), LGBM -0.0028 (0.0040)
  The column auditor's numbers reproduce exactly (own pair ridge 0.0996 / PLS 0.1125; trailing 30 min 0.0997 /
  0.1097).

  Reproducibility: every variant is bit-identical when rebuilt from a row-shuffled read of the deposit (no ties in
  Time_Sample). The own pair needs only the row itself. The trailing mean needs a window length we choose (15 min:
  29.7% of rows have only their own pair; 30 min: 12.8%, median 3 pairs; 60 min: 3.4%, median 5) and lacks the 46
  unlabelled samples' pairs the sensor had. The 0.5 h hold needs a session boundary we infer (break > 1 h: 42
  sessions) and may pick a missing sample's pair as a block's first.

  Reading: no causal variant is better by score. The differences are within 1-2.5 SE and change sign by model
  (trailing better for PLS-15 and trees, worse for PLS-30 d1, equal for ridge), so they measure these four windows,
  not the referencing (evidence.md, "not decisive", aeolus). The future readings in the shipped spectrum are worth up
  to 0.004 RMSE for the best honest model (PLS-30 d1, 2.7 SE): weak but real, as LEAK-30 says.

4. DISPUTED POINTS, SETTLED

  (1) Which causal rebuild. Settled by rule: the row's own pair.
      Advocate: trailing 30-min mean, "the documented deployment procedure" (data paper 3.1). Critic: own pair, the
      preprint's default, exact on every row, no other row needed.
      Facts: the documented procedure holds ONE pair for 0.5 h from the session start; it never averages pairs. The
      trailing mean is therefore neither source procedure: it is our own construction with a free window length
      (Tensions row "A better version against our own fix": a fix of our own invention does not replace a version
      the source defines). The data paper's description of the deposit says each sample "with its corresponding
      white and dark reference ... is normalized" and "for the same sample, white and dark reference spectra were
      also acquired"; the preprint: "by default, a pair ... every time a milk sample spectrum was recorded". The own
      pair is that normalisation, rebuilt exactly from the origin (PROV-13, PROV-14), and a ratio within the row,
      which LEAK-30 names as fine. The closest reading of the 0.5 h procedure (the hold) cannot be rebuilt exactly
      (inferred sessions, 46 missing pairs). Scores do not separate them (section 3).
      Rule order: PROV-13 / PROV-14 (Must, P5) decide the remedy; within it the source's own definition beats a
      construction of ours (Tensions, P5). Change now. The curator may still prefer the 0.5 h hold as the source's
      deployment recommendation (the data paper names the reference frequency as a research use); that is a
      one-line override, not an open issue.

  (2) "The source's 0.083" as headroom. Settled: critic. Do not cite it as headroom.
      Advocate: best honest 0.096 vs RMSEP 0.083 shows headroom. Critic: different protocols.
      Facts (k, i): the 0.0826 is on week-1 training, 1,165 samples, one 857-row test set, with the water band
      removed; our harness on that protocol gives ridge 0.102; on the shipped windows the gap to 0.083 is mostly one
      2.59% row (0.098 with, 0.080 without). Rule: EV-8 (Should): say which version a number comes from; a number
      from another version may not hold for the shipped one. Nothing outranks it. Remedy: the notes give 0.0826 as
      the source's result on its protocol beside ridge 0.102 on the same protocol under our harness, and say nothing
      of headroom. The builder's checklist row "ridge 0.098 vs RMSEP 0.083" (P2) goes too. TP needs no headroom
      claim: no flag is raised.

  (3) A note on arXiv 2605.21544's TabPFN result. Settled: critic. No note.
      Advocate: "a contamination note at most"; blind reviewer: record the published TabPFN results. Critic: EV-4.
      Rule: EV-4 (Must) and PROV-15 (Must): other benchmarks' scores and pretraining overlap are never evidence and
      never an issue for the curator; another collection's version is named only for provenance or a duplicate. No
      higher rule pulls the other way. The existing provenance mention (the screening's 402 fat values superseded by
      the deposit's 1,224, curation_comments bullet 2; source_links) stays; no TabPFN score and no contamination
      sentence is added.

5. CHANGES TO MAKE NOW (no decision needed)

  1. Rebuild nir_bin_<i> in _clean as (Trans_Sample - Trans_Dark) / (Trans_White - Trans_Dark) of the row itself;
     drop Trans_Tot. State stays raw. Record in the notes: the deposit's Trans_Tot used the week's mean pair
     (exact to 5e-15 in 4 weeks), the paper's text says otherwise, the rebuild's cost on the four windows (ridge
     0.0983 -> 0.0996, PLS-15 0.1095 -> 0.1125, PLS-30 d1 0.0977 -> 0.1017), and the trailing-mean and 0.5 h-hold
     alternatives with their numbers. (LEAK-30, PROV-13, PROV-14; Tensions row: the source's version over ours.)
  2. Rewrite the false notes from the measurements: curation_comments bullet 5 ("session/0.5 h ... cannot be
     rebuilt"), bullet 4 ("%" is the source's percent-transmittance convention, values numerically the ratio), the
     Spectrum description, claims 16-18, and the builder's checklist rows (LEAK-27-31 "no all-row statistic", PROV-13
     "slip", P2 "vs RMSEP 0.083"). (EV-2, PROV-13, writing.md)
  3. Prediction point: the end of the sensor's cycle, up to 144 s after milking end (the row's dark and white are
     read after the sample). (USE-3, USE-6; needed by change 1)
  4. Bullet 6 (instrument blocks): replace "the inputs of the referencing that Trans_Tot already carries" with the
     fact: after change 1 the shipped spectrum is built from each row's own blocks; the blocks alone predict the
     train mean; shipping them would let a method choose its own referencing (the data paper's research use).
     Place USE-6 beside option A in issue 1. (USE-6, EV-2)
  5. Axis: columns on the nominal axis 960 + 2.86 (p - 1) nm, unit="nm", the description saying the axis is the
     source's nominal linear one, matching its 1360-1500 nm window within one pixel. (CLEAN-26 Should: the guide
     numbers bins only when the source gives no axis; option b returns to the rule, so no exception.)
  6. Notes on score levels: cow 50435's 2.59% row is 75% of week 7's squared error (four-window ridge 0.098 with,
     0.080 without), likely the preprint's -1.573; kept as the source kept it. Fresh cows hold 39.5% of week 8's
     squared error. (CLEAN-11, PROV-13 default keep; SPLIT-17 met)
  7. The source-protocol score beside the shipped windows (ridge 0.102 on 308/857) and the maintenance gain (train
     week 1 only 0.120 vs expanding 0.098), not as headroom. (EV-8)
  8. Fresh-cow decision reason: identification measured (removing the five cows reproduces Table 3, 308/857); not
     colostrum (protein max 3.88%); FPR > 1.4 in 11.9% vs 2.0%. (EV-1, CLEAN-11)
  9. fit_reason: about 160 lab references a week here vs about one per cow per 4-6 weeks on a farm; days in milk and
     parity, always known on a farm, are not in the deposit. (USE-8)
 10. Wording: splits_comment "cannot" -> "need not" (week 4, SPLIT-14); "weeks 4 to 13 days apart" scoped to the
     test windows; 98.1% named as the mean of windows (98.8% pooled); sensor-timestamp drop reason: a proxy of yield
     (r 0.83, partial r with fat -0.08). (writing.md, CLEAN-22)
 11. Re-run the probes and `dataset check` after changes 1 and 5 (EV-1: the shipped numbers change).

6. ISSUES FOR THE CURATOR (rank order)

  Issue 1 (P3/P7; USE-6 Must against CLEAN-22/CLEAN-26 Should; weighing). The 768 raw instrument columns
    (Trans_Dark, Trans_White, Trans_Sample).
    Problem: known at the prediction point; dropped. Effect: after change 1 the shipped spectrum already uses every
    row's own references, so what the blocks add is only the freedom to choose another referencing (frequency,
    averaging); alone they predict the train mean.
    Ship them (B): USE-6, "dropping it changes the task"; CLEAN-26's rationale (a method that processes spectra
    itself keeps the signal); the data paper names the reference frequency as a research use; the sensor holds
    them. Precedent checker: open_soil's "choice of actor" does not carry over (there the actor never had the
    inputs). Is it a USE-6 failure? Not on its own: USE-6 makes them legitimate, and the information they carry
    reaches the model through the rebuilt spectrum; it is a call on how much freedom to ship.
    Keep dropped (A): the source's on-farm models read the normalised spectrum; the domain practitioner would deploy
    that; 261 vs 1,029 features with no measured label signal in the blocks. Width is no argument either way (EV-4).
    What would settle it: a measured gain of a model reading the blocks (e.g. ridge on own-pair spectrum + blocks,
    or a learnt referencing) over the rebuilt spectrum on the four windows; none was run. Decision: A or B.
  Issue 2 (P3/P4; USE-6, USE-10, SPLIT-13; weighing, low). cow_id kept. Builder, domain practitioner, both sides,
    precedent checker: keep (robot knows the cow; wisconsin, sendy). Only trees gain (0.267 -> 0.213); the cow
    mean alone 0.575. Against: a cow-agnostic calibration is another product. Recommendation A keep.
  Issue 3 (P5/P7; CLEAN-11; low). The 59 fresh-cow samples kept. Measured: no effect as training rows (PLS 0.1058
    vs 0.1069); as test rows 39.5% of week 8's error; not colostrum; the cases health monitoring is for. The 2020
    article removed them; the data paper (first publication) releases them. Recommendation A keep.
  Issue 4 (rule maintenance; CLEAN-26). After change 5, a line in spectra.md for sources that give a range and a
    step but no per-pixel table (nominal axis, said so), so the next NIR source is decided alike; and, optionally,
    "referencing against the instrument's white and dark is raw" (open_soil, milk). Decision: add the lines or not.

7. TASK GAMER'S EXPLOITS, MAPPED

  The definition carries no `Potential leak, kept on purpose:` note and no accepted check warning.
  - Test-window centering (0.0961 vs 0.0960), pseudo-labels (0.0962), standardising over all rows (0.0986 vs
    0.0989), EPO with the test window (worse): LEAK-30 (transductive). No gain; nothing to note. The week-mean
    referencing found by the column auditor is the same rule's mechanism, built into the data rather than played by
    a participant; new (no note covers it), worth up to 0.004 RMSE (section 3), removed by change 1.
  - Cow-history residual correction (0.0949): USE-10, a known entity's history; honest, within noise.
  - Copies, ids, row order, number formats: LEAK-16 to LEAK-21, LEAK-34; nothing found.
  - Row 934 (cow 50435, 2.59%): not an exploit; CLEAN-11 / PROV-13, note (change 6).

8. CONSISTENCY WITH PRECEDENT

  Followed: cow_id kept as wisconsin PolicyNum and sendy Rider Id (USE-10); Prot/Lact/SCC/Urea dropped as caracas
  and open_soil (LEAK-10); state raw as open_soil's referenced absorbance (CLEAN-26); fresh cows kept as the
  CLEAN-11 default, set apart from ames_housing (the data's first publication releases them); SPLIT-19 yields to
  SPLIT-14, set apart from medical_facility (the 50% floor leaves one-week windows only); MET-5 as open_soil;
  rebuild from the origin as coad_colon_adenocarcinoma (LEAK-30 "rebuilt") rather than bioresponse's note, because
  the deposit holds the unprocessed counts.
  Departure removed: unit="bin" against micro_mass's fact (no axis published); change 5 returns to the guide.
  Open: issue 1 has no precedent with the same facts (open_soil's actor never held the inputs): the curator's call
  sets one. Reflection question: would you ship the reference blocks for the next NIR or Raman source that publishes
  them beside a normalised spectrum?
  Register: 34 flags, none triggered by this dataset; no drift, no third exception.
```

</details>

<details><summary>Claim audit</summary>

```text
CLAIM AUDITOR: milk_nir_composition (2026-11-09)
Folder: df-large/datasets/_dev/tabarena-v0pt2/milk_nir_composition/ ; claims: claims.md (43)
Scratch: the run folder (all runs inline, OMP/MKL/OPENBLAS threads 2; nothing written to the repository)

VERDICT: no validity claim refuted. All P1-P4 claims hold on the data and the sources, including the metric
(RMSE = the source's RMSEP; MET-1/2/3/5 hold). Two documentation claims are refuted and two are worded too strongly.
None of them changes a shipped value, the split or the metric. The fresh-cow identification now has measured proof
(it was an inference). Ranked list at the end.

KEY TESTS
T1 Trans_Tot rebuild (claim 17): for every row i and every row j of all 1,224 (not only the 60 before it),
   max|Trans_Tot_i - (S_i - D_j)/(W_j - D_j)|: the smallest is 0.0016, the median of the best is 0.0038, and no row
   is within 1e-4. The own pair gives 0.0378 at most, with 0 rows within 1e-3 and 541 within 1e-2. I tried four
   session schemes with breaks over 1 h: 42 sessions; the first pair of the session, the first pair of each 0.5 h,
   the mean pair of each 0.5 h, the mean pair of the session. Medians of the row errors: 0.013, 0.011, 0.010, 0.005.
   None is exact. Alignment check: Trans_Tot_i is closest to its own row's ratio for 88% of rows, so the spectrum
   belongs to its row. The per-row least-squares scale of Trans_Tot against the own ratio is 0.995 to 1.003, so
   there is no factor of 100 in the numbers. HOLDS.
T2 Unit "%" (claim 16, builder report PROV-13 "documentation slip"): the 2020 article (Figure 2 text) says the
   absorbance at the 1450 nm band is "between 4 and 5" and that "a very small fraction (10^-4 - 10^-5) of the
   incident photons" passes. At pixel 163 (the band's maximum), log10(1/T) is 2.00 to 3.05 (1st to 99th percentile
   2.39 to 2.90). log10(100/T) is 4.00 to 5.05 (4.39 to 4.90). The source therefore reads Trans_Tot as percent
   transmittance. Table 1's "%" is its convention, not a slip. REFUTED as a slip. The numbers are unchanged; an
   absorbance computed from them is off by a constant 2, which no model sees.
T3 Axis (claims 14, 15): direction. Mean absorbance at pixels 9, 74, 163 is -0.67, -0.47, +2.64, weak to strong as
   water's 970, 1200, 1450 nm bands. Pixel 1 is the short end: HOLDS. Per-pixel wavelength: the band-maximum argument
   is weak. At pixel 163, S - D is about 13 counts against W - D of about 5,250, so the maximum sits in noise; pixel 9
   lies on the sloping edge. A sharper test is the window the source removed as "very low" transmittance,
   1360-1500 nm (preprint, Methods). The linear axis 960 + 2.86 (p - 1) puts the pixels with median T < 0.03 at
   141-187, which is 1360-1492 nm, and median T < 0.01 at 143-180, which is 1366-1472 nm. Pixel 256 maps to
   1689.3 nm. The linear axis matches the source within about one pixel. "Would be a guess": OVERSTATED (partly
   refuted). Bins remain defensible because no per-pixel table is published.
T4 Fresh cows (claims 27, 28): without cows 55391, 55392, 55393, 55394 and 59137, week 1 has n = 308, fat mean 3.44,
   SD 0.86, range 1.61-6.25. Weeks 2-8 have n = 857, mean 3.54, SD 0.79, range 1.54-5.72, from 36 cows. This is
   exactly the article's Table 3 (calibration n = 308, test n = 857). 55391 is the only cow with 8 samples in
   week 1 and 15 in all. HOLDS, now measured, not inferred.
T5 Splits (claims 33-35, 37), through the container: test windows 162/168/84/166, train 1062/894/810/644,
   overlap 0. The gap between train end and test start is 97, 292, 311 and 293 h. Each window holds exactly one
   SET (5-8). Train sizes equal the counts of earlier weeks, so the 3-day gap removes no row. New cows per window:
   0, 1, 3, 0. Week 4 as a test window would have a train side of 585 = 47.8% and 59 test rows.
T6 Metric (MET-2): `scorer(c)` on a train-mean dummy gives 0.8566, 0.7440, 0.8723, 0.7200 (mean 0.798). Unit is the
   row; no scoring column needed; no sample weight; target_transform identity. Preprint: RMSECV selects the model,
   RMSEP is reported (Table 4: real-time fat 0.0826), and the ICAR limits are judged in RMSEP (0.1% laboratory,
   0.2% at-line, 0.25% in-line). Same target (lab fat, % w/w) and same cows; the five fresh cows are kept, but the
   fresh-only RMSE for week 8 (0.074) does not dominate.
T7 Replication (claims 41, 42), shipped splits: ridge as-is 0.105, SNV 0.090; PLS-15 as-is 0.1015, SNV 0.093;
   ridge on absorbance 0.098. Ridge with fresh cows trained in vs out, scored on non-fresh rows: 0.0968 vs 0.0967.
   Matches the claims.
T8 Values (claims 9, 13, 22): after sorting by time, Fat, Trans_Tot and Cow_ID equal the container's columns
   exactly (array_equal True).

CLAIMS TABLE (claim | source | test | result | evidence | rule)
1  | Zenodo 8263430 v0.0.1, 2023-08-18, one file, md5, 1224x1038 | curation_comments | Zenodo API, md5sum, shape | holds | API: v0.0.1, 2023-08-18, data_table.csv 11,343,720 B, md5 7cd61315...; local md5 equal; (1224, 1038) | PROV-8
2  | CC BY 4.0 | license | Zenodo API | holds | cc-by-4.0 | EV-4
3  | Authors | bibtex | Zenodo API | holds | 7 creators as listed | PROV-10
4  | DiB 51 (2023) 109767 | notes | dib.txt | holds | "Data Brief. 2023 Nov 4;51:109767" | PROV-10
5  | 2023 is the first publication | year | preprint data statement | holds | preprint ships no data ("no reuse allowed"); Zenodo is the first deposit | PROV-8
6  | 41 Holstein cows, Hooibeekhoeve, 8 weeks 2017, VMS | task_summary.row | data plus dib 3.1 | holds | 41 Cow_ID, 2017-05-24 to 07-27 (CEST), SET 1-8, "VMS (DeLaval)" | USE-1
7  | 1270 of 5969 (22%), 46 removed | row | dib 3.1 | holds | quoted | PROV-13
8  | MCC, CombiFoss FT+, ISO 9622, within 3 days | notes | dib 3.1 | holds | quoted (the preprint names a "Milkoscan FT+"; no effect) | USE-5
9  | Target = Fat, unchanged | notes | array_equal | holds | T8 | USE-5
10 | Fat on all rows, no missing values | notes | isna | holds | 0 missing in 1224x1038; Reiter et al.'s count not checked (outside the deposit) | CLEAN-11
11 | Fat 1.54-7.6, mean 3.52 | claims | describe | holds | 1.54, 7.60, 3.5247 | -
12 | Prot, Lact, SCC, Urea dropped (LEAK-10) | notes, _clean | dib: same sample tube, lab within 3 days, ISO 9622 / 13366-2 | holds | recorded after the prediction point, from the label's own lab analysis | LEAK-1, LEAK-10
13 | Trans_Tot, 256 px, renamed, unchanged | notes | array_equal | holds | T8 | CLEAN-26
14 | Pixel 1 = short end; no per-pixel wavelength published | notes, Spectrum | absorbance band order; dib Table 1 note b | holds | T3: band order weak to strong; only range and 2.86 nm/px published | CLEAN-26
15 | Linear axis misplaces the bands, so a per-pixel wavelength "would be our guess" | notes | source's own 1360-1500 nm low-T window under the linear axis | overstated (partly refuted) | T3: 1360-1492 nm at T < 0.03; the band maxima used sit in noise | CLEAN-26, EV-6
16 | Trans_Tot is a plain ratio "though Table 1 says %"; ">1 where milk passes more light than the Spectralon" | notes; builder PROV-13 | source's absorbance scale (Fig. 2 text) against log10(1/T) and log10(100/T) | refuted (as a source slip) | T2: the source's A = 4-5 at 1450 nm matches log10(100/T) = 4.00-5.05, not log10(1/T) = 2.00-3.05 | PROV-13, EV-2
17 | Not rebuildable from own or recent dark/white | notes | all pairs from all rows plus four session schemes | holds | T1 | EV-1
18 | Source used a session pair, refreshed every 0.5 h | notes | dib 3.1, preprint | holds | quoted in both; the preprint adds that by default a pair was taken with every sample | -
19 | State `raw` | Spectrum | spectra.md definitions, precedent, code | holds, with a note | the source calls Trans_Tot "Normalized"; spectra.md calls "a normalisation applied by the source" processed, but referencing to white/dark is the instrument's standard output (open_soil_spectral_library absorbance declared raw); `spectrum_encoding` uses the state only for mass spectra, so nothing changes | CLEAN-26
20 | Dark/white/sample blocks known at prediction, dropped by choice | notes | timestamps, dib | holds (a choice) | read 39-144 s after milking end; the data paper names them a research use (reference frequency) | CLEAN-26, USE-6
21 | SET and sensor times dropped; offsets 39-144 s; order S, D, W | notes | raw diffs | holds | Sample 39-107, Dark 54-122, White 71-144 s | -
22 | Kept fields | _clean | columns | holds | 5 non-spectral features plus 256 bins = 261 | -
23 | Interval 245-1118 s below the timestamp difference | notes | raw | holds | 245, 1118, 0 negatives | -
24 | Unix seconds converted to CEST | notes | conversion; tz names | holds (conversion); untested (that the epoch is true UTC) | all 1224 CEST; no outside clock to test against; hours flat 0-23 (the robot runs 24 h) | -
25 | Robot knows the cow, cow_id at prediction | notes | dib (AMS), preprint (cows in both sets) | holds | the preprint's real-time setting has "all cows represented in calibration and test" | USE-6, USE-10
26 | No duplicate rows or spectra | notes | duplicated() | holds | 0 and 0 | LEAK-16
27 | Article removed 59 samples, leaving 1165/36 | notes | preprint | holds | quoted | -
28 | The five fresh cows | notes, FRESH_COWS | reproduce the article's Table 3 | holds (now measured) | T4 | EV-1
29 | 7.6% is cow 55394 in week 8; the article's range ends at 6.25 | notes | raw; preprint Fig. 2, Table 3 | holds | max 7.60 (55394, SET 8); article maximum 6.25 | -
30 | Fresh cows change nothing | Decision | ridge replication | holds | 0.0968 vs 0.0967 (PLS 0.1058 vs 0.1069 in the builder's json) | CLEAN-11
31 | Use case: real-time on-farm, calibration updated | task_summary | dib abstract, preprint | holds | "real-time prediction", "calibration maintenance", "by adding new samples to the calibration set" | USE-1
32 | Fit direct | fit | - | holds (an inference) | rows are the sensor's own readings in time order | USE-8
33 | 4 windows, sizes, expanding | splits_comment | container | holds | T5 | SPLIT-11
34 | Gap 3 days removes no row; "weeks are 4 to 13 days apart" | splits_comment | week boundaries | holds for the gap; the wording is too broad | weeks before the test windows are 4.06-13.0 days apart; weeks 1-2 are 2.1 and weeks 2-3 are 1.3 days apart | SPLIT-10
35 | Week 4 "cannot" be a test window under SPLIT-14 | splits_comment | SPLIT-14 as amended 2026-11-08 | overstated | 47.8% is at least 40%, and 98% of cows recur, so the amended clause would allow it; that clause is for releases with two valid windows, and here there are four, so leaving it out is right ("need not") | SPLIT-14, SPLIT-17
36 | Source: train week 1 (308), test 2-8 (857) | notes | preprint | holds | quoted; reproduced in T4 | SPLIT-12
37 | Four cows new in their first test window | splits_comment | container | holds | new cows per window 0, 1, 3, 0; seen 98.1% | SPLIT-13
38 | Metric rmse = source RMSEP | metric | preprint Methods, Table 4, ICAR text; scorer per fold | holds | T6; the journal version (the declared reference) was not readable here, the preprint was | MET-1, MET-2, MET-3, MET-5
39 | Real-time fat RMSEP 0.0826 | notes | preprint Table 4 | holds | "Real-time 0.0826b" | MET-11
40 | Domain chemistry & material science | domain | domain list | holds (a judgment) | no agriculture domain exists; 16 definitions use this one | -
41 | Scratch scores | notes | json arithmetic; partial refit | holds | dummy 0.798, cow 0.575, PLS trans 0.105, abs 0.105, ridge 0.098, LGBM 0.271/0.267/0.213, bias-corrected 0.106; ridge refit 0.098 | EV-8
42 | Encodings | notes | refit of ridge and PLS-15, as-is vs SNV | holds | 0.105 / 0.090 and 0.1015 / 0.093 | CLEAN-26
43 | Probe numbers | claims | probe logs | holds | every number matches leak_probes.log, task_probes.log, hidden_groups.log | EV-3

IMPLIED CLAIMS ATTACKED
- Every feature is known at the prediction point: holds. Yield, interval and the robot's times are robot fields;
  the spectrum is read 39-107 s after the end of milking, and the prediction point is "when the sensor has read".
- The target is the real-world target: holds (lab reference fat, ISO 9622).
- No copy across the split: holds (0 exact copies; 1-NN R^2 0.742 is the natural similarity of milk spectra).
- The split is the one the use case needs: holds. The use case is a known herd, so temporal; the source's
  real-time protocol is temporal with every cow in calibration (USE-10, SPLIT-13).
- USE-10 "the previous outcome is a feature": the cow's last known lab fat is not shipped. Measured: ridge on
  absorbance 0.0984 alone, 0.0986 with the cow's last training-side fat, 0.0987 with the cow's training mean.
  No gain, so nothing to add.
- Not written anywhere: one row (cow 53318, 2017-06-14 07:51) has milking_interval_seconds 1685 (0.47 h; 0.63 h by
  the timestamps) with 10.95 L, which is 23.4 L/h. The median is 1.5 L/h and the next largest 3.0 L/h. This is
  probably an incomplete previous milking recorded by the robot. It is a real robot record, but the notes could
  name it (CLEAN-11, P7, low).

REFUTED / OVERSTATED, RANKED (all P5/P7 documentation; no Must broken)
1. Claim 16 and the builder's PROV-13 "Table 1's % is a documentation slip" (P5, PROV-13; low). The source reads
   Trans_Tot as percent transmittance (T2). Changes: the notes sentence "Table 1 gives the unit as %, but the
   values are the plain ratio ... above 1 where the milk passes more light than the 2 mm Spectralon reference",
   the Spectrum description, and the builder's PROV-13 row. Values, models and metric are unchanged. Mildest
   remedy: reword. For example: "Trans_Tot equals (sample - dark)/(white - dark) numerically (0.0009 to 7.99); the
   source reads it as percent transmittance (its absorbance of 4-5 at 1450 nm is log10(100/T))".
2. Claim 15, "a per-pixel wavelength would be our guess" (P7, CLEAN-26; low). The source's 1360-1500 nm window
   matches the linear axis within one pixel (T3). The band-maximum test used noise-level pixels. Changes: the
   reasoning in the notes. `unit="bin"` can stay. Mildest remedy: keep bins and state that the linear axis
   960 + 2.86 (p - 1) nm agrees with the source's water window within about one pixel. Declaring nm as an
   approximation is a curator call.
3. Claim 35, "cannot be a test window under SPLIT-14" (P4 wording; low). The amended SPLIT-14 would permit week 4
   (47.8%), but four valid windows exist and week 4 has 59 rows. Remedy: "need not" in the splits comment.
4. Claim 34, "the measurement weeks are 4 to 13 days apart" (wording; low). This is true only before the four test
   windows. Remedy: "the weeks before each test window end 4 to 13 days before it".

UNTESTED
- Claim 24: whether the Unix seconds are true UTC (the robot runs 24 h, and there is no outside clock). If they are
  local time, the hour-of-day shifts by a uniform 2 h; there is no validity effect.
- Claim 38 against the journal text of Comput. Electron. Agric. 178:105734 (not readable; the preprint was read).
  Low risk: the metric statements are in Methods and Table 4 of the preprint.
- Claim 10's statement about Reiter et al.'s 402 Milk_Fat samples: their table was not opened. It does not affect
  the deposit.

STRENGTHENED
- Claim 28 (fresh-cow identification) is now measured: removing the five cows reproduces the article's Table 3
  exactly. The notes can say so in place of "identified by their counts".
```

</details>

<details><summary>Column audit</summary>

```text
COLUMN AUDITOR REPORT: milk_nir_composition (2026-11-09)
Scripts and outputs: the run folder (a1-a8.py, clean.parquet, dtype probe output)
Sources read: data paper (papers/dib.txt, Table 1, section 3.1), bioRxiv preprint of the 2020 article (papers/biorxiv.txt,
methods), builder_report.md, claims.md, probe logs; rules principles.md, use_case.md, leak_checks.md, cleaning_features.md
(from the df-large worktree).

VERDICT: ship after changes. One P4 finding that no probe flags: the shipped spectrum is NOT referenced per session and
every 0.5 h, as the definition says. Every row is normalised with ONE reference pair per trial week, the mean of all
that week's dark and white readings. These include readings taken up to 85 h after the milking, the other test rows of
the same test window, and the 46 samples without a lab value. It is a weak transductive leak (LEAK-30). It carries no
label information and is measured at <= 0.003 RMSE. The raw blocks to rebuild the spectrum causally are in the deposit.
The definition's bullet on the referencing is contradicted by the data and must be corrected whatever the remedy.

====================================================================================================================
1. THE KEY MEASUREMENT: how Trans_Tot was referenced
====================================================================================================================
- Sorted by Time_Sample, row k fits the reference pair recovered from rows k-2 and k-1 exactly (|residual| < 0.01
  counts) for 92.3% of consecutive triples. Grouping rows greedily by that fit gives exactly 8 blocks, one per SET
  (trial week): 316, 190, 79, 59, 166, 84, 168 and 162 rows, spanning 21.9 to 85.1 h each (a4.py).
- The recovered dark and white are non-integer (e.g. 21412.63), so they are no single measured pair; no row's own pair
  matches (best row 2.4-5.8 counts off).
- Trans_Tot == (Trans_Sample - mean_week(Trans_Dark)) / (mean_week(Trans_White) - mean_week(Trans_Dark)) to 5e-15
  (machine precision) in weeks 2, 3, 7 and 8. These are exactly the weeks whose deposit count equals the data paper's
  Table 2 N (190, 79, 168, 162). In weeks 1, 4, 5 and 6 the deposit lacks 32, 1, 1 and 12 samples (= the 46 "no
  reference" samples). There the rebuild is off by at most 2.1e-3 absolute: their readings were in the source's mean
  (a8.py).
- So the source took the mean of the week's references, including the 46 dropped samples. It is not the start of the
  session plus every 0.5 h that the data paper (section 3.1) and the 2020 article describe.
- No label path: ridge on a row's own dark, white or (white - dark) block predicts fat no better than the train mean
  (windows 5-8: 0.719-0.867 vs 0.720-0.872, a7.py).
- The split does not mix train and test: each test window is exactly one SET (166/84/168/162 rows = weeks 5-8), and the
  training weeks are referenced with their own week means.
- Effect, the four shipped windows, absorbance -log10(T), PLS-15 / RidgeCV on standardised bins (a6.py):
    shipped (week-mean reference)       PLS 0.1095  ridge 0.0983
    row's own pair (the paper's default) PLS 0.1125  ridge 0.0996
    expanding mean of the week so far   PLS 0.1114  ridge 0.0996
    mean of the pairs of the last 30 min PLS 0.1097  ridge 0.0997
  Per window the order is mixed (e.g. window 1 PLS: shipped 0.1588, causal 0.1507-0.1533). The future readings are
  worth at most 0.003 RMSE (about 1-3%): weak.
- What a test row then holds: its spectrum depends on the instrument readings of every other milking of its test week,
  up to about 45 h later in the test weeks (85 h in week 1). The milking robot "predicting at once" (task_summary
  use_case) cannot have those readings.

====================================================================================================================
2. COLUMN TABLE (cleaned frame: 1,224 rows x 262 columns; then the dropped source columns)
====================================================================================================================
column | meaning | known at prediction? | dtype and cleaning | verdict | rule

nir_bin_1..256 | Trans_Tot, normalised transmittance (S-D)/(W-D) per pixel of the 256-px InGaAs array, 960-1690 nm,
  pixel 1 the short end (data paper Table 1 note b) | NO in part: the reference is the mean of the whole week's
  dark/white readings, up to 85 h after the milking and from other test rows (section 1) | float64; a plain ratio
  0.00086-7.99, not % (Table 1 is wrong; handled). Above 1 in every row for pixels 1-134 and 234-256: the 2 mm Spectralon
  "white" transmits less light than 2 mm of milk (white-dark only 185-6,000 counts, sample up to 57,324). That is real
  physics, not damage. No saturation: raw counts max 57,324 of 65,535, white max 27,580. No dead pixel: the smallest
  per-pixel SD of the raw counts is 4.3, of Trans_Tot 0.00064. No zero or negative value. The water band is weak
  (sample-dark down to 6 counts near pixels 140-200; the source cut 1360-1500 nm in its models); kept whole (CLEAN-26).
  Axis direction confirmed: the largest absorbance is at pixel 163 (the 1450 nm water band), local maxima at 9 and 74;
  reversed, the strongest band would sit near pixel 85. unit="bin" is the safe choice, since a linear axis puts the
  peaks at 983/1169/1424 nm | weak leak + wrong documentation | LEAK-30 (Should when weak), LEAK-10 timing; EV-2

cow_id | Cow_ID, "Identification number of each measured cow" | yes: the VMS identifies the cow at attach | category of
  strings, 41 levels (the dtype probe's numeric_levels flag is answered: an id, categorical by meaning). The id does not
  encode the label: Spearman of id with the cow's mean fat -0.098, with mean yield -0.245. Four cows new in their first
  test window | fine | CLEAN-3 (an identifier with meaning, kept), CLEAN-14, USE-10 (a known herd), LEAK-34

milk_yield_liters | Milk_yield, "Total milk yield", liters, from the robot's meter | yes, at the end of the milking |
  float64, 6.16-27.77, plausible | fine | USE-6

milking_interval_seconds | Milk_Interv, "Time difference since the last milking" | yes (known at the start of the
  milking) | int64, 1,685-65,175 s. It is 245-1,118 s shorter than Time_Milk - Time_PrevMilk: start-to-previous-end
  versus end-to-end, so the difference is the milking's duration. The 1,685 s minimum is real, not an impossible value:
  cow 53318 gave 6.89 L at 05:14 after a 12.4 h interval (an incomplete milking), then 10.95 L 37 min later. 4 rows are
  under 4 h | fine | CLEAN-11 (nothing to repair)

milking_end | Time_Milk, "end of milking process", Unix s -> Europe/Brussels wall clock (CEST, every row), naive |
  yes: the prediction moment (the sensor reads 39-107 s later) | datetime64; the temporal axis; frame sorted by it, no
  duplicate times. The week sessions start at 11:13-19:43 local, plausible. No hour-of-day column built: under the
  CLEAN-2 precedent (nyc_taxi) a datetime's encoding is the pipeline's. Fat-hour r = 0.095. A VMS has no fixed schedule,
  and the interval, which drives the schedule effect, is shipped | fine | CLEAN-19 (not needed), CLEAN-2, CLEAN-23

previous_milking | Time_PrevMilk, timestamp of the cow's last milking | yes (earlier than the milking) | datetime64;
  in 915 of 1,183 rows it equals the same cow's previous deposit row; nearly redundant with milking_end minus the
  interval and the duration, but no exact copy | fine | CLEAN-5 (not a copy)

fat_percent (target) | Fat, % w/w, MCC lab, CombiFoss FT+, ISO 9622 | arrives up to 3 days later (gap 3 d) |
  float64, 1.54-7.60, complete | fine | USE-5

Dropped source columns:
Prot, Lact, SCC, Urea | the same lab analysis of the same sample | no (up to 3 days later) | - | correct drop | LEAK-10

Trans_Sample, Trans_Dark, Trans_White (768) | raw counts, the row's own dark and white references | yes (taken 39-144 s
  after the milking end, during the sensor's cycle) | 16-bit integers, unsaturated | weighing call (builder issue 2),
  but its stated reason is wrong: they are not "the inputs of the referencing that Trans_Tot already carries".
  Trans_Tot discards the per-row references (it uses the week mean), so they hold information Trans_Tot lacks, and
  they are the only way to a causal rebuild | CLEAN-22, CLEAN-26

SET | trial week 1-8 | yes | = the reference block and the date's week | correct drop (derivable from milking_end) |
  CLEAN-5 spirit

Time_Sample, Time_Dark, Time_White | sensor timestamps, 39-107 / 54-122 / 71-144 s after Time_Milk; the dark comes 14-32 s
  after the sample, so the timestamps contradict the paper's "references before the sample". Table 1 also labels
  Time_Dark "white" | yes | - | drop acceptable, but the stated reason ("measure its own cycle, not the milk") is
  inaccurate: the offset correlates 0.83 with yield and -0.30 with fat, and given yield its partial r with fat is only
  -0.082. Correct the reason: a proxy of the shipped yield | minor note | CLEAN-22

====================================================================================================================
3. PROBLEMS, ranked by principles.md
====================================================================================================================
1. [P4, LEAK-30 (Should, weak), with LEAK-10's timing] The spectrum carries a statistic over the week's rows, test rows
   and readings after the prediction point included.
   Evidence: section 1 (exact rebuild with the week mean in 4 of 8 weeks; the other 4 off only by the 46 dropped
   samples). No label content (the reference blocks alone = train mean). No train/test crossing (windows = weeks).
   Worth <= 0.003 RMSE.
   Remedies, mildest first in the rule's order (LEAK-30: "Rebuild from the unprocessed values when the source has
   them"; the source has them):
   (A) Recommended: rebuild nir_bin_* causally in _clean from the deposit's own blocks. Two options:
       - the mean of the dark/white pairs measured in the 30 min up to and including the row (closest to the documented
         0.5 h procedure; PLS 0.1097, ridge 0.0997);
       - the row's own pair (the preprint: "by default, a pair ... was acquired every time a milk sample spectrum was
         recorded"; PLS 0.1125, ridge 0.0996).
       The state stays raw. Note that the 46 dropped samples' pairs are not in the deposit, so the trailing mean
       approximates the sensor's state.
   (B) Keep the deposit's Trans_Tot with a "Potential leak, kept on purpose:" note: the source's published
       normalisation, a weak transductive step within each week, measured at <= 0.003 RMSE.
   (C) Ship the raw blocks as spectra (joins builder issue 2), with the causal rebuild of (A).
   Weighing call for the curator. The rule leans to (A), P4 over CLEAN-26's "as the source publishes it" (P7).

2. [P5 / evidence, EV-2; writing] The definition states a falsehood about its main feature.
   - curation_comments bullet 5 says the source normalised "with a reference pair taken at the start of each session
     and every 0.5 h ... which the deposit does not ship. So the shipped spectrum ... cannot be rebuilt from the other
     blocks". The measurement says the opposite: one week-mean pair, rebuilt exactly. The same goes for claims.md 17-18.
   - The builder checklist line "Trans_Tot referenced per session/0.5 h (no label, no all-row statistic)" is wrong: it
     is a statistic over the week's rows. The "largest difference 0.038" is absolute; the relative difference reaches
     87-130% in the water band.
   - Bullet 6's reason for dropping the instrument blocks rests on the same error.
   - The Spectrum description should name the week-mean reference, or the causal one after (A).
   Fix: rewrite these bullets with the measurement, whatever option issue 1 takes. Also name the documentation
   mismatch (paper: per session/0.5 h; deposit: per week) as a PROV-13 note.

3. [P7, CLEAN-22/CLEAN-26] Builder issue 2 (the instrument blocks) needs its premise corrected. The blocks are not
   carried by Trans_Tot; they add the per-row reference information Trans_Tot averages away. Alone they predict nothing.
   The weighing call stays, but the record should say this.

4. [P7, CLEAN-22, minor] The reason for dropping the sensor timestamps is inaccurate: the offset tracks yield (r 0.83),
   with a partial r of -0.08 with fat beyond it. Keep the drop and correct the sentence.

Not problems (checked):
- cow_id: categorical by meaning; a known herd (98.1% of test rows' cows seen); the id order does not encode the label.
- The times: Unix to CEST is plausible, sorted, no hour feature needed (CLEAN-2 precedent).
- milking_interval: the minimum is a real re-milking.
- yield: the robot's own field.
- Prot/Lact/SCC/Urea drop correct (LEAK-10).
- SET drop correct.
- No saturated or dead pixels; values above 1 are real physics; the axis direction is confirmed.
- The dtype probe's only flag (cow_id numeric_levels) is answered.
```

</details>

<details><summary>Split audit</summary>

```text
SPLIT AUDITOR REPORT: milk_nir_composition (2026-11-09)

Verdict: RIGHT WITH NOTES. Temporal on `milking_end`, 4 expanding weekly windows (weeks 5-8), gap 3 days. The regime
matches the use case (a robot on one farm predicting for its own herd, calibration maintained as references arrive;
USE-10 known entity, SPLIT-3). No validity problem found. The notes concern how stable each window's score level is
(one milking dominates week 7), the documented departure from the source's week-1 protocol, and two wording points.

Judgment record:
  Validity: USE-10 holds (known cows, temporal); SPLIT-1/3/4 hold; SPLIT-9 holds (no training label arrives after a
    window start); SPLIT-10 holds (gap 3 d = lab delay, removes no row); SPLIT-11 holds (expanding); SPLIT-13 holds
    (cows recur, as the task does); SPLIT-14 holds (oldest train 52.6%, 4 windows); SPLIT-17 holds (84-168 test rows,
    32-36 cows per window); SPLIT-19 departed from, required by SPLIT-14 (Must), stated in splits_comment.
  Value (for the metric/task agents): window RMSE levels hinge on single rows; rankings stable.
  Weighed: refit cadence weekly vs the source's "milk recording every 4 to 6 weeks"; the one season of the trial.

Data: loaded through dataset_io.from_definition(raw=True) (week from raw `SET` traced by the index), 1,224 rows.
Scripts and outputs: the run folder, a2_models.py, a2_models.json, a3_outliers.py}.
Models (untuned): ridge = RidgeCV on standardised absorbance -log10(T); PLS-15 on absorbance; LightGBM (500 trees,
spectrum + yield + interval) with and without the cow as a category; dummy = train mean.

------------------------------------------------------------------------------------------------------------------------
1. WINDOWS, TRAIN SIDES, GAP (P4; SPLIT-10, SPLIT-11, SPLIT-14, SPLIT-17)  -> holds

Weeks as measured (n, first and last milking, span, days to next week's first milking, mean fat):
  w1 316  05-24 19:43 .. 05-28 08:51  85 h  2.10 d  3.449
  w2 190  05-30 11:13 .. 06-01 08:51  46 h  1.26 d  3.452
  w3  79  06-02 15:08 .. 06-03 14:19  23 h  4.94 d  3.496
  w4  59  06-08 12:50 .. 06-09 10:45  22 h  4.06 d  3.343
  w5 166  06-13 12:06 .. 06-15 09:08  45 h 12.17 d  3.472
  w6  84  06-27 13:06 .. 06-28 13:03  24 h 12.95 d  3.585
  w7 168  07-11 11:49 .. 07-13 08:44  45 h 12.21 d  3.663
  w8 162  07-25 13:52 .. 07-27 10:22  44 h   -    3.716
Shipped splits, as read from the plan: each test side is exactly one whole week (w8, w7, w6, w5), each train side is
every earlier week: 1,062 / 894 / 810 / 644 rows (86.8 / 73.0 / 66.2 / 52.6%). Time from the last training milking to
the first test milking: 12.21 / 12.95 / 12.17 / 4.06 days. The lab reports "within no more than three days", so every
training label had arrived before each window starts (smallest margin 1.06 d, week 5); the 3-day gap removes no row.
No training row's label is unknown at the prediction point (SPLIT-9 holds). A week-4 window is impossible: its train
side (weeks 1-3) would hold 585 rows, 47.8% < 50% (SPLIT-14), as the comment says.
Wording (claim auditor): splits_comment says "the measurement weeks are 4 to 13 days apart"; true from week 4 on, but
weeks 1->2 and 2->3 are 2.1 and 1.3 days apart. Mildest remedy: "each test week starts 4 to 13 days after the
previous week's last milking". No effect on any split.

2. SCORE STABILITY OF THE SMALL WINDOWS (P6 boundary; SPLIT-17, TP)  -> note; no re-split

Per-window RMSE (cluster bootstrap over the window's cows, 2,000 draws, SE in brackets):
                 w8              w7              w6              w5             mean
  dummy          0.857 (0.090)   0.744 (0.055)   0.872 (0.064)   0.720 (0.060)  0.798
  ridge          0.058 (0.009)   0.143 (0.054)   0.106 (0.029)   0.084 (0.014)  0.098
  PLS-15         0.065 (0.005)   0.159 (0.044)   0.118 (0.026)   0.097 (0.012)  0.110
  LightGBM       0.275 (0.058)   0.312 (0.037)   0.239 (0.030)   0.248 (0.024)  0.268
  LightGBM+cow   0.232 (0.060)   0.238 (0.045)   0.215 (0.042)   0.176 (0.015)  0.215
Rankings are stable: LightGBM - ridge = +0.211 / +0.176 / +0.135 / +0.165 (SE 0.050 / 0.041 / 0.029 / 0.024, 3.5 to 7
SE per window); PLS - ridge = +0.007 / +0.016 / +0.012 / +0.013 (SE 0.005 / 0.011 / 0.007 / 0.004), same sign 4 of 4.
The levels are not: week 7's ridge RMSE is 75% one milking. Cow 50435, 2017-07-11 21:38, reference fat 2.59% between
4.38% and 5.47% of the same cow's neighbouring milkings (its weeks 5-8 lie 4.26-5.47); ridge predicts ~4.19 (residual
-1.60). This is very likely the preprint's "fat test error of -1.573" plotted off-scale (the source kept it in its
RMSEP). Without that row week 7's ridge RMSE is 0.072 and the four-window mean 0.080 instead of 0.098 (one row of 580
lifts the headline 22%). The top 3 rows carry 38 / 79 / 67 / 42% of each window's squared error (w8 / w7 / w6 / w5);
w8's largest is the fresh cow 55394 at 7.60% (train max 6.25%).
Remedy: none on the split (SPLIT-17 is met; widening windows adds no test rows, the 50% floor fixes the pool). A note
in splits_comment or the metric notes that a window's level hinges on a few milkings, and a question for the data
auditor whether the 2.59% reference is a laboratory or sample-pairing error (PROV-13 / CLEAN; the source kept it, so
keeping it is the default).

3. REGIME: MAINTAINED CALIBRATION vs THE SOURCE'S FIXED WEEK-1 CALIBRATION (P4; SPLIT-19 vs SPLIT-14, SPLIT-12)
   -> shipped choice right; optional note

The source's real-time protocol (train week 1, test weeks 2-8) has one window and a 25.8% train side (316 of 1,224):
it breaks SPLIT-14 (Must), which outranks SPLIT-19 (Should). The source also asks for calibration maintenance ("By
adding new samples to the calibration set ... the models can be made robust"; data paper: "how to maintain them in
time"), so the expanding windows are the source's own next step, not our invention.
Reproduced: dropping the five fresh cows gives exactly the preprint's 308 calibration and 857 test samples. On it,
ridge 0.102, PLS-20 0.134, PLS-15 0.172, LightGBM 0.291, LightGBM+cow 0.291, dummy 0.791 (source RMSEP 0.0826 with
water-band removal, preprocessing and wavelength selection; with the fresh cows: ridge 0.119).
Value of maintenance on the shipped windows (train week 1 only vs every earlier week): ridge 0.071 / 0.191 / 0.126 /
0.092 (mean 0.120) vs 0.058 / 0.143 / 0.106 / 0.084 (mean 0.098); PLS-15 0.085 / 0.276 / 0.136 / 0.118 vs 0.065 /
0.159 / 0.118 / 0.097. Same model ranking under both protocols (ridge < PLS < LightGBM).
Cadence (weighed, not a problem): the test weeks 5-8 are two weeks apart, so the refit is fortnightly; the source names
routine milk recording every 4-6 weeks as the reference supply in practice, while this trial had weekly references.
The shipped cadence is the trial's real one; a 4-6-week cadence cannot be built with 8 weeks and 3 windows.
Optional remedy: add the source-protocol score (ridge 0.102 on the 857) to the notes beside the shipped windows.

4. COWS RECUR (P3/P4; USE-10, SPLIT-13, SPLIT-4)  -> holds

Test rows whose cow is in training: w8 100%, w7 99.4% (1 row), w6 92.9% (6 rows), w5 100%; pooled 573 of 580 =
98.8% (the builder's 98.1% is the mean of the four window shares; both are right, say which). The robot identifies
every cow and the source's real-time evaluation kept every cow on both sides: a known entity, temporal is right.
Grouped by cow (GroupKFold 5 x 3 repeats, 41 cows): ridge 0.087, PLS-15 0.103, LightGBM 0.270, LightGBM+cow 0.304,
dummy 0.819; random IID 5-fold: ridge 0.085, PLS 0.100, LightGBM 0.238, LightGBM+cow 0.176.
Reading: the shipped temporal split is not easier than a cold start for the linear calibrations (ridge 0.098 temporal
vs 0.087 grouped: time costs more than unseen cows). The known cow helps only a tree that reads the cow id (0.268 ->
0.215 temporal; under grouping the id hurts, 0.270 -> 0.304). So recurrence does not inflate the task; the known-cow
gain is the robot's legitimate knowledge (issue 1 of the builder; keeping `cow_id` is consistent with this regime).
A temporal cold-start check (drop the test week's cows from training) is degenerate: 62 training rows remain.
Near copies of spectra seen across the split: 11.7% of test rows (hidden probe), distinct milkings; not a group.

5. DRIFT AND SEASON (P4; SPLIT-20)  -> holds, with the drift being the task

Mean fat per week rises 3.34-3.50 (w1-w4) to 3.66 / 3.72 (w7, w8), as in the data paper's Table 2. Within cows: +0.293
% fat (SE 0.057, 32 cows present in both) from weeks 1-4 to weeks 7-8, so it is a real level change inside the herd,
not a change of herd composition (only the four calved cows are new in w6-w8). The maintained calibration absorbs it:
ridge's mean residual is +0.001 / +0.001 / +0.003 / -0.023 (w8 / w7 / w6 / w5). The test windows all sit in the
drifted second half; that is the source's question (model drift over time). The whole trial is one season (24 May to
27 July 2017): no test window can be compared with another season; fit_reason already limits the claim to one farm and
eight weeks. No break in the training history (fresh cows enter in weeks 6-7; their effect was measured by the
builder as nil).

------------------------------------------------------------------------------------------------------------------------
Ranked problems (all notes; none blocks shipping)
 a. P6/SPLIT-17 boundary: one milking (cow 50435, 2.59%) is 75% of week 7's squared error and lifts the 4-window ridge
    mean from 0.080 to 0.098; rankings stable (LightGBM vs ridge 3.5-7 SE per window, PLS vs ridge same sign 4/4).
    Remedy: a note; data auditor to judge the reference (keep by default, as the source did).
 b. P4/SPLIT-19 departure (required by SPLIT-14): stated; optionally add the source-protocol score (ridge 0.102 on the
    paper's 308/857) and the maintenance gain (0.120 -> 0.098) to the notes.
 c. Wording: "measurement weeks 4 to 13 days apart" (true for the test weeks only); 98.1% (mean of windows) vs 98.8%
    (pooled) of test rows with a known cow.
```

</details>

<details><summary>Domain practitioner</summary>

```text
DOMAIN PRACTITIONER REPORT: milk_nir_composition (record milk_nir_composition), 2026-11-09
Actor played: a dairy farmer or herd adviser with an in-line NIR milk analyser on an automatic milking system (AMS),
reading each cow's milk fat after every milking, the calibration kept up with laboratory references.

VERDICT
Fit: direct (USE-8). One row is one labelled milking that the sensor reads at the end of milking. The inputs are what
the robot and sensor hold at that moment. The target is the laboratory reference that on-farm analysers are approved
against, and the test weeks come after the calibration weeks, which is how a farm keeps a sensor calibrated.
Metric: yes. RMSE per milking in % fat is the source's RMSEP (MET-5) and the quantity I would choose a calibration by.
The ICAR comparison is approximate, because ICAR states s_y,x and mean bias separately (see Q5).
Draft issues: issue 1 (cow_id) A keep; issue 2 (instrument blocks) A, normalised spectrum only; issue 3 (fresh cows)
A keep, with a stronger reason than the builder gives (see Q2/Q3). There is nothing blocking.

HOW THE DECISION IS MADE TODAY (sources below)
* Per-cow milk composition comes from milk recording (DHI): one laboratory sample per cow every 4 to 6 weeks
  (bioRxiv preprint, Discussion: "individual cow milk samples are already collected every 4 to 6 weeks"). In-line
  analysers on robots fill the gap between those samples. DeLaval (VMS V300 NIR milk-solids sensor), BouMatic
  MilkGenius and Afimilk sell them, and each vendor claims "self-calibrating" or "no calibration needed" without
  publishing how.
* What per-cow fat drives:
  (a) Health screening. Ketosis or negative energy balance shows as a rising fat:protein ratio (FPR). The usual
      cut-off is 1.4 in Holsteins (Oregon State 2010); one large farm treats after two consecutive milkings above
      1.55. A low ratio (about 1.0) is read as SARA or milk-fat depression. All of these act on fat AND protein, and
      most acting happens in early lactation.
  (b) Feeding. Concentrate in the AMS is allocated per cow, and ECM-based allocation needs fat and protein. Herd
      ration changes respond to herd fat levels.
  (c) Milk payment. The dairy pays on the bulk tank, sampled at collection, so per-cow fat does not set payment.
      Per-cow fat only informs component-yield estimates and culling or selection. Payment is the weakest of the three
      decisions in the briefing.
* Approval: ICAR Section 13 (on-farm milk analysis, wiki version) sets per-animal-sample accuracy for fat (medium
  range, g/100 g):
    s_y,x  0.10 laboratory, 0.20 on-farm at-line, 0.25 on-farm in-line
    mean bias  +-0.05, +-0.10, +-0.13
  ICAR tests on 100 animals across 5 herds against an accredited reference laboratory. The source compares its RMSEP
  with these s_y,x limits.

Q1. DO I HAVE THESE INPUTS AT THE MOMENT OF PREDICTION?
* Spectrum (nir_bin_1..256, Trans_Tot): yes. The sensor produces it 39 to 107 s after milking ends. The source
  referenced it against a dark/white pair taken at the start of the session and then every 0.5 h, which is also how
  the sensor would run in deployment.
* Milk yield, milking interval, milking times: yes. The AMS records them at the end of every milking.
* cow_id: yes. The robot identifies every cow by transponder (USE-6). The cow's earlier lab references from the
  calibration weeks are also legitimately mine (USE-10, a known entity).
* Prot, Lact, SCC, Urea: correctly dropped. They come from the same lab analysis as the target and arrive days later
  (LEAK-10).
* Inputs I would ALWAYS have and the deposit lacks:
  - Days in milk, parity and calving date, from the herd software (DelPro). Days in milk is the strongest prior for
    fat and ketosis risk, and it is the variable that would show directly which fresh-cow samples are colostrum.
  - The sensor's readings on the roughly 78% of milkings without a lab sample (the cow's recent trajectory).
  - Conductivity, activity, and any Herd Navigator readings.
  None of these can be shipped from the deposit, so this is no defect of the folder, but a calibration on a real farm
  would use days in milk. Weight: low to moderate.
* Instrument blocks (Trans_Dark, Trans_White, Trans_Sample): known at prediction time. The farm's model reads the
  normalised spectrum, so dropping them (issue 2 A) matches deployment. They only serve the data paper's research
  question about how often to take references.

Q2. IS THE TARGET WHAT I ACT ON?
* Yes, with one caveat. Lab fat (MCC Vlaanderen, CombiFoss FT+, ISO 9622 MIR) is the reference that ICAR approves
  on-farm analysers against, and it is the number milk recording gives me today (USE-5).
* The caveat is that the decisions in (a) and (b) above act on fat together with protein (FPR, ECM). Fat alone is half
  the input to the ketosis rule. Protein is a sibling task on the same spectra (CLEAN-18). I would welcome it as a
  second folder, but this one stands on its own.
* I want a number in % w/w, not a class. Thresholds on FPR vary between 1.4 and 1.55, and between breeds, and they
  are applied to the ratio over consecutive milkings, so no single class cut belongs in the target.
* Fresh cows (issue 3), measured on the deposit:
  - The 59 samples are not colostrum. Their protein is mean 3.29% and max 3.88%, against 2.63 to 4.34% for the other
    1,165 samples. Their lactose is 4.77% on average, against 4.70%. Colostrum at the first milking has protein far
    above 10% and low lactose. The article's removal "to avoid the inclusion of colostrum samples" was therefore a
    precaution that also took the transition milk of the following weeks. The robot diverts true colostrum anyway.
  - They are the samples my health decision is about. FPR above 1.4 occurs in 7 of 59 fresh-cow samples (11.9%),
    against 23 of 1,165 others (2.0%). The 7.6% fat sample (cow 55394, week 8, yield 7.2 L, FPR 2.3) is exactly the
    kind of milking I would want flagged.
  - Removing them would remove the early-lactation cases that per-milking monitoring exists for. Keep (A). The builder
    measured no change to the overall error (PLS 0.1058 vs 0.1069), so keeping them costs nothing.

Q3. DOES ONE ROW MATCH ONE DECISION? IS THE TEST WHAT I WOULD FACE?
* One row is one milking read by the sensor, which is one prediction (and possibly one alert). That matches my
  decision. Each milking is its own decision, so a per-row score is right and no unit weight per cow is needed
  (MET-17, the per-decision clause).
* Test = later weeks on my own herd, after a 3-day lab delay. This matches running the sensor on my farm with
  calibration maintenance (USE-10: known cows, temporal split). Four cows that calve during the trial enter in weeks
  6 to 8 as new cows, as fresh cows do on a real farm.
* Gaps, ranked by how much they change the task:
  1. One farm, one prototype sensor (KU Leuven's bypass on a DeLaval VMS / Herd Navigator sampler), eight weeks in one
     season. A vendor or adviser installing on a new farm faces calibration transfer across farms, diets and genetics,
     and ICAR approval is tested on 5 herds. The farm's own task stays direct; transfer is not tested. fit_reason
     already names this. MODERATE for the adviser, none for the farmer.
  2. Label richness. The feeding trial gave about 160 lab references per week, from 32 to 37 cows in each of the 8
     weeks, and the expanding windows train on 644 to 1,062 references. A commercial farm on milk recording gets about
     one reference per cow every 4 to 6 weeks (about 40 for this herd per month). The source's own real-time protocol
     trained on week 1 only (308). The benchmark is therefore richer in labels than practice, and it may favour
     label-hungry methods somewhat, but it still mirrors "update the calibration with the references received". This is
     a known gap that I would note, not one that changes the fit. LOW to MODERATE.
  3. Missing always-known inputs: days in milk, parity, the sensor's unlabelled readings (Q1). LOW to MODERATE.
  4. Fat alone where some decisions act on FPR (Q2). LOW.
  5. Milkings were sampled on the trial's schedule (21 to 85 h per week, 22% of milkings), not by outcome, so this is
     no selection bias on fat. NEGLIGIBLE.

Q4. WOULD I USE THIS MODEL? TRUST AND DISTRUST
* I would trust a calibration that:
  - stays below about 0.10 to 0.15% RMSE in every window, including the hard week 7 (PLS 0.14 to 0.16 there, against
    about 0.06 to 0.11 in the others);
  - has no systematic bias drift over the weeks (the source saw drift, worst for protein);
  - tracks a cow's deviations from her own baseline, because the alerts are built on those deviations.
* What would make me distrust it is a model that leans on cow identity. Measured: untuned LightGBM goes from 0.267 to
  0.213 RMSE with cow_id, while PLS and ridge (0.10) gain nothing. The source's median cow-bias correction did not help
  fat either (0.0838 vs 0.0826), and the builder's re-run agrees (0.1056 vs 0.1054). A model that predicts close to a
  cow's usual fat would under-report the very deviations I act on. RMSE rewards that shrinkage only a little here,
  because the spectrum carries far more signal: the cow mean alone scores 0.575, the spectrum about 0.10, the
  within-cow SD of fat is 0.43 and the between-cow SD of cow means is 0.66.
* So I would deploy a calibration that may use the cow, the way the source's bias correction does (USE-6, USE-10).
  Dropping cow_id would test a different product, a cow-agnostic factory calibration, which is the transfer question
  of gap 1, not my farm's. Issue 1: A keep.
* A minor point: milking_end and previous_milking as datetimes let a model fit a calendar trend. Time of day and the
  interval are real physiology (fat rises after short intervals). The absolute date only stands in for drift. Nothing
  to change; methods choose how to encode it.

Q5. DOES THE METRIC SCORE MY DECISION?
* Yes.
  - RMSE of fat in % w/w per milking is the source's RMSEP. The source selects models by RMSECV, reports RMSEP and
    argues it against ICAR (MET-5: one deliberate criterion; MET-1: per milking, the unit I act on).
  - ICAR scores s_y,x (the residual SD after the regression on the reference) and mean bias separately. RMSE is about
    sqrt(bias^2 + SEP^2), so it combines the two: the bias matters for herd-level feeding and payment-side estimates,
    the SEP for per-cow alerts.
  - I would choose a calibration by RMSE. As diagnostics I would also look at bias and s_y,x per window against ICAR's
    0.25 / +-0.13 (in-line) and the worst window, but these are reporting, not a different selection metric.
* No threshold metric applies. FPR cut-offs range from 1.4 to 1.55 and need protein too, so the source fixes no single
  threshold or cost, and a threshold-free score is right (MET-6, MET-7; MET-9 does not apply to a regression).
* Per row and unweighted is correct, because each milking is a decision of its own (MET-17).
* Metric I would use: rmse (as declared).

WHAT A DOMAIN EXPERT WOULD CHANGE (none blocking)
1. Strengthen the reason for keeping the fresh cows in the notes or in the _decisions table:
   - the protein and lactose of the 59 samples are normal milk, not colostrum (protein max 3.88%);
   - FPR > 1.4 occurs in 11.9% of them against 2.0% of the rest, so they are the early-lactation cases the health
     decision is about.
   The current text rests on "the robot meets fresh cows" alone.
2. Name in the notes or fit_reason that the calibration-maintenance windows have far more references per week (about
   160) than a farm on milk recording (about one per cow per 4 to 6 weeks), and that the source's real-time model used
   week 1 only.
3. Name days in milk and parity as inputs a farm always has, missing from the deposit (they could be requested from the
   authors; this does not affect shipping).
4. Optional sibling folder: protein on the same spectra, since the ketosis and SARA decisions use fat and protein
   together (CLEAN-18 allows it as another framing).
5. Nothing to change in the target, the split, the drops or the metric.

SOURCES
* Diaz-Olivares et al. 2020, bioRxiv 10.1101/2020.06.02.129742 (= Comput. Electron. Agric. 178:105734), the
  extracted text in papers/biorxiv.txt: the real-time protocol, the cow-bias correction
  (Table 6), the colostrum removal, the ICAR comparison, the 4-to-6-week milk recording.
* Diaz-Olivares et al. 2023, Data in Brief 51:109767 (papers/dib.html): Table 1, section 3.1, "Value of the data".
* ICAR Guidelines Section 13, On-farm milk analysis
  (https://wiki.icar.org/index.php/Section_13_%E2%80%93_On-farm_Milk_Analysis): accuracy limits s_y,x 0.10/0.20/0.25
  and bias +-0.05/0.10/0.13 for laboratory / at-line / in-line, 100 animals in 5 herds. The table was read from the
  wiki's garbled extraction; the PDF https://www.icar.org/Guidelines/13-On-farm-milk-analysis.pdf could not be parsed
  here.
* DeLaval milk-solids sensor press release (https://www.delaval.com/en-gb/knowledge-hub/news-events/press-releases/milk-solids-press-release/),
  BouMatic MilkGenius (https://boumatic.com/products/milkgenius/), Progressive Dairy on FPR and ketosis in in-line
  testing (https://www.agproud.com/articles/19880-detect-ketosis-using-milking-equipment,
  https://agproud.com/articles/22317-how-to-monitor-energy-balance-using-in-line-milk-testing).
* My measurements on the deposit (data_table.csv): fresh-cow composition, FPR shares, per-week counts and cows,
  within- and between-cow fat SD. The builder's probes/experiments.json supplies the per-window PLS, LightGBM and
  cow-bias numbers.
* Rules: use_case.md USE-1, USE-3, USE-5, USE-6, USE-8, USE-10; metrics.md MET-1, MET-5, MET-6, MET-7, MET-9, MET-17;
  leak LEAK-10; CLEAN-18.
```

</details>

<details><summary>Blind review</summary>

```text
BLIND REVIEW: milk_nir_composition (target fat_percent, regression, 1,224 x 262, temporal split on milking_end, 4 test windows)

VERDICT: Include with changes. It is a real, honestly built calibration task. Two changes are needed: stop using the two
datetime columns as raw features, and declare the 256 NIR bins as an ordered spectrum. Also note that a linear model
nearly saturates the task (R2 about 0.985), so it mostly tests how a model handles smooth, collinear spectra.

WHAT THE TASK IS
An in-line NIR transmittance sensor (Zeiss 1.7-256 grating spectrometer, 256 pixels, 960-1690 nm, 2.86 nm/pixel)
sits on an automatic milking system on a Belgian (KU Leuven) farm. The data covers 41 Holstein cows over 8 weeks in 2017.
For each milking, the sensor measures a milk subsample about 78 s after the milking ends (median 77 s, range 39-107 s,
from the source Time_Sample - Time_Milk). The model predicts that milking's fat %. The reference value is the lab fat
of a parallel VMX sample, measured on a CombiFoss FT+ (ISO 9622) at MCC-Vlaanderen. The companion paper (bioRxiv
10.1101/2020.06.02.129742) gives the purpose: the sensor "can analyze the milk of each individual milking session
autonomously to support the cost-efficient monitoring of performance, efficiency, and welfare of individual dairy
cows". This is a real use. The farmer or AMS software would make the prediction at every milking to drive cow-level
health and feeding decisions. The sensor is calibrated on the same herd and then used going forward, so a temporal
split with the same cows in train and test matches deployment.

PROVENANCE CHECK (done)
I downloaded data_table.csv from Zenodo 8263430 (md5 7cd61315ad73fbdc6461ad85f59b6f90, matches the record).
- nir_bin_1..256 equal the source Trans_Tot_1..256 exactly (max abs diff 0.0).
- fat_percent equals Fat exactly. Rows are in the same order. The source has no missing values (1,224 rows = 1,270
  milkings minus 46 without a lab reference, as the article says).
- Dropped columns: Prot, Lact, SCC, Urea, SET, Time_Dark/White/Sample, and the raw Trans_Dark/White/Sample counts.
  Dropping the other lab values is correct, because they are lab-only and would leak. Dropping the raw counts is fine.
- milking_end and previous_milking are the source Unix times shifted by exactly +7,200 s (UTC to CEST). The shift is
  consistent and harmless.
- milking_interval_seconds equals Milk_Interv exactly.
- No duplicate spectra and no duplicate rows.
The data is real, not generated. The values are plausible:
- Fat 1.54-7.6 %, mean 3.52, sd 0.81. Single AMS milkings vary this much.
- Yield 6.2-27.8 L.
- Interval 0.5-18 h.
- Transmittance is near 0 (about 0.001-0.01) in the 1,400-1,500 nm water band, as expected.

BASELINES (my own approximation of the split: rows sorted by time, cut into 5 equal blocks, train on everything before
each of blocks 2-5; RMSE per window; target sd per window about 0.79)
  predict train mean                          0.802
  per-cow train mean                          0.523
  LightGBM on cow/yield/interval/hour/time    0.596
  LightGBM on 256 bins                        0.279
  LightGBM on all columns                     0.240
  LightGBM on first-difference absorbance     0.157
  PLS 20 comp. on absorbance                  0.102
  RidgeCV on transmittance                    0.105
  RidgeCV on absorbance (-log10)              0.096   (R2 about 0.985)
  RidgeCV absorbance + cow one-hot + meta     0.097
  RidgeCV absorbance, random 5-fold           0.089
The authors' own time-based result (train on week 1, test on weeks 2-8) is RMSEP 0.083, consistent with these.

CONCERNS, MOST TO LEAST SERIOUS

1. A linear model nearly saturates the task, and the score mostly measures inductive bias for spectra.
   Evidence: ridge reaches RMSE 0.096 against a target sd of 0.80. Trees on the same bins are about 2.5-3x worse
   (0.24-0.28). The metadata and cow_id add nothing on top of the spectrum (0.097 vs 0.096). The headroom is small: the
   floor is the error of the lab reference itself, which I did not verify but which is usually a few hundredths of a
   percent fat. Random 5-fold is only slightly easier than temporal (0.089 vs 0.096), so drift is mild.
   Change: keep the task, but tag it as spectral/chemometric so that it does not count as a generic tabular task in
   aggregates. Declare nir_bin_* as one ordered spectrum feature with the wavelength grid (960 + 2.86*(i-1) nm), so
   that methods can use spectral preprocessing (absorbance, derivatives, SNV). Consider adding the absorbance
   transform as a documented option. Consider the closely related targets (protein, lactose) as separate tasks only if
   you want more spectral weight; otherwise one task from this source is enough.

2. Two datetime columns are model inputs under a temporal split.
   Evidence: milking_end is both the split key and a feature, so every test value lies outside the training range.
   previous_milking is redundant: it equals milking_end - milking_interval_seconds - 450 s (the gap ranges 245-1,118 s),
   so it adds only the same out-of-range date.
   Change: drop previous_milking, and use milking_end only as the split key. If you want time-of-day information, add
   hour of day, which is causally sensible because fat varies with time of day and interval.

3. The dataset is already published in an NIR benchmark that is aimed at tabular foundation models.
   Evidence: arXiv 2605.21544 ("Tabular foundation models for robust calibration of near-infrared chemical sensing
   data") lists "Milk_Fat ... TabPFN-opt 0.078", plus Milk_Lactose, Milk_Urea and Milk_Ratio. Its dataset-metadata
   table was cut off in my fetch, so I could not confirm that this is the same KU Leuven source. task.md links the
   paper, which suggests it is.
   Change: record it as a known public dataset with published TabPFN results, and check for overlap with any
   foundation model's training or tuning collections before reporting it as held out.

4. The evaluation windows are small and clustered.
   Evidence: there are 23 sampling days in 8 weekly sessions (week counts 316/269/59/166/84/168/162). Each test
   window is about 245 rows. One quintile window runs from 14 Jun to 12 Jul and spans a 2-week gap. Rows within a
   session share white/dark reference updates (every 0.5 h), so errors are correlated. 41 cows give a median of 32
   rows per cow (4 to 55).
   Change: align the 4 windows to the source SET weeks or sessions rather than to arbitrary row counts, and report the
   spread across windows. Per-window RMSE differs by up to about 2x (0.062-0.131).

5. One farm, one sensor, one season.
   Evidence: the article covers 41 cows, May-July 2017 and one instrument. Results will not transfer to other
   instruments, but that is inherent to sensor calibration and is fine for a benchmark.
   Change: none, beyond documenting it.

6. Minor preparation points:
   - cow_id is categorical with 41 levels, which is correct.
   - 19 test rows (2 later windows) belong to cows not seen in training. This is realistic, because cows enter the herd.
   - The bins are stored as float transmittance in % (0.0009-7.99). The column names should carry the wavelength.
   - The source labels Trans_Tot as "%" and calls it (sample - dark)/(white - dark). Recomputing that from the raw
     counts does not reproduce Trans_Tot (diff up to 793), so some other scaling, such as integration time, is
     applied. This does not matter for modelling, but the definition is not fully documented.

COULD NOT CHECK
- How the benchmark harness encodes the datetime columns (as raw features, dropped, or expanded).
- The exact boundaries of the 4 official test windows. I used equal row quintiles.
- Whether arXiv 2605.21544's Milk_Fat is this exact dataset, and what its split was.
- The repeatability of the lab reference, which sets the noise floor.
- The full Data in Brief text on Elsevier, which redirected. I used the PMC copy (PMC10700509) instead.

Source copy: .../work_blind_reviewer/src_download/data_table.csv
```

</details>

<details><summary>Task gamer</summary>

```text
TASK GAMER REPORT - milk_nir_composition (fat_percent, RMSE, 4 temporal windows = source weeks 8, 7, 6, 5)

Verdict: I could not game this task. No exploit beat the honest model by more than the noise spread (about 0.001 RMSE).

Honest baselines (per split r0f0 r1f0 r2f0 r3f0, then the mean)
  train mean                       0.8566 0.7440 0.8723 0.7200  mean 0.7982
  LGBM untuned, all features       0.2449 0.2137 0.2287 0.1486  mean 0.2090  (work/baseline.py)
  LGBM + random column (3 seeds)   mean 0.2114 to 0.2121, so the spread is about 0.003
  Better honest model: PLS with 30 components on the Savitzky-Golay first derivative of the absorbance -log10(T)
                                   0.0611 0.1380 0.1011 0.0839  mean 0.0960  (work/honest.py, work/models.py)
  PLS + random column (3 seeds), PLS with 28 or 32 components: mean 0.0955 to 0.0965, so the spread is about 0.001
  The source paper reports a fat RMSEP below 0.092, in line with this.

Exploits ranked by gain: none found.
| # | Exploit | Script | Honest | Exploited | Gain | A deployed model has it? | Fix |
| - | (nothing beat the honest PLS or LGBM beyond the noise) | | | | | | |

Flaws that hurt an honest model: none found that an honest choice can fix.
  - Dropping training rows with an OOF residual above 0.5: 0.0958 vs 0.0960 (noise). Above 0.3: 0.0980 (worse).
  - Training only on recent weeks is worse: 21 days 0.1327, 35 days 0.1082.
  - Remark, not a flaw to fix: test row 934 (cow 50435, 2017-07-11 21:38, lab fat 2.59) is a likely sample or
    lab mix-up. The cow's other milkings read 4.3 to 5.5, and the spectrum predicts 4.11. That one row is about half
    of the r1f0 MSE: r1f0 is 0.138 with it and 0.073 without it. No feature identifies it, so it cannot be exploited.
    It only makes r1f0 noisy. A possible fix: flag it in the task notes or drop it from the test set.

Attacks that found nothing (mean RMSE; honest PLS 0.0960, LGBM 0.2090)
  Transductive and test-row statistics:
    - spectra centered per weekly window, test window included, + honest level: 0.0961
    - EPO, projecting out the window-mean drift directions with the test window: 0.205 to 0.223 (worse).
      The same with training weeks only: 0.123 to 0.162
    - self-training with test pseudo-labels: 0.0962
    - spectra standardized over all rows: 0.0986. Over training rows only: 0.0989
    - adversarial AUC of training vs test spectra: 0.78 to 0.96. The weeks drift, but using the test rows does not
      help. The honest model's bias per window is under 0.012, so there is no level shift to correct.
    - LGBM + spectra centered per window: 0.2358 (worse). LGBM + ranks over all rows + per-window cow counts: 0.2107
    - blending each prediction with the cow's mean prediction over the whole test window: 0.1580 (worse).
      Within a window, the residuals of a cow's consecutive milkings correlate only 0.04 to 0.19.
  Copies across the split: there are no exact or near copies. The nearest test-to-train distance is 0.047 vs a
    median of 0.125. kNN1 and kNN5 labels from the training spectra: 0.356 and 0.285.
  Order and ids: rows are sorted by time, as in the source, and the time is already a feature. corr(position, fat)
    = 0.105, a seasonal rise (week means 3.45 to 3.72). cow_id is an honest feature. Cow-history residual correction
    (OOF training residuals per cow, shrunk): 0.0949, which is honest and within noise. The PLS + LGBM residual stack
    on yield, interval, time and hour: 0.0971.
  Training rows from the future: none. Every test window is a whole week. Training ends 4 to 13 days before it, and
    the lab result comes "days later", so no fix is needed.
  Formats: fat always has 2 decimals, and its last digit is uniform (107 to 137 rows per digit). Last digits of
    yield, interval and seconds alone: 0.849, worse than the mean. The significant-digit count of the NIR floats:
    0.768 vs 0.798 for the mean. It is a weak echo of magnitude, not a recording artefact. The NIR values equal the
    source's Trans_Tot exactly.
  Columns from after the prediction point: none in the kit. The preparation dropped Prot, Lact, SCC and Urea (lab
    values that arrive with the label), SET (the week), the dark and white reference spectra, and the timestamps of
    the sensor reads. Non-spectral features alone (cow, yield, interval, times) in LGBM: 0.547.
  Time columns are shifted by +2h from the source's unix time (local time). milking_end - previous_milking exceeds
    milking_interval_seconds by 245 to 1118 s (likely the milking duration). Both are honest.
  Web: Zenodo 8263430, the Data in Brief paper (PMC10700509) and arXiv 2605.21544 (TabPFN on NIR). I found no leak
    or magic-feature threads; this is not a competition dataset. The rows can be looked up in the public CSV (exact
    match, same order), which every public dataset allows and is not ranked here.

Not checked: whether the dropped dark and white reference spectra (sensor data, available at prediction) would help
an honest model; the full text of arXiv 2605.21544.
Scripts in work/: common.py, models.py, baseline.py, honest.py, bias.py, resid_struct.py, attacks1.py, attacks2.py,
format_check.py, attacks_lgbm.py. The source CSV is in work/src/data_table.csv.
```

</details>

<details><summary>Precedent check</summary>

```text
PRECEDENT CHECKER: milk_nir_composition (2026-11-09)
Definition: df-large/datasets/_dev/tabarena-v0pt2/milk_nir_composition/dataset.py; record curation/records/milk_nir_composition.md
(only curator line: CC 2026-11-08 Lennart, accepted for adding). Register: panel/register.json (5,226 decisions, 34 flags; none
names this dataset, and none of the 34 is triggered by these calls). Scratch: the run folder.

VERDICT: 7 of 8 calls consistent with precedent (2 of them with a stated reason that sets the case apart). One call, the
spectrum's axis as `unit="bin"`, departs from the documented meaning of `bin` and from micro_mass's fact, and its stated
reason is weakened by the claim auditor: the one consistency prompt below. No drift, no third exception, no Must broken.
bacteria_id_raman and raman_mlrod are builder decisions of this same batch (not reviewed by a curator yet): cited as
siblings, not as precedents.

Judgment record:
  Validity: USE-10 holds (cow_id kept, as wisconsin PolicyNum, sendy Rider Id, uniform_soybean genotype); LEAK-10 holds
    (as caracas_cervical_cancer, open_soil_spectral_library); SPLIT-19 departed from, required by SPLIT-14 (a Must, no
    exception needed); SPLIT-12 departure from the source's horizon set apart by the 50% floor (vs medical_facility).
  Value: MET-5 holds (as open_soil_spectral_library; the fallback would be rmse too).
  Quality: CLEAN-26 state `raw` consistent (open_soil absorbance); CLEAN-26 axis `bin`: departs, prompt 1; instrument
    blocks dropped: open_soil's "choice of actor" in kind, not in fact (bullet for issue 2); CLEAN-11 fresh cows kept:
    the default, set apart from ames_housing; CLEAN-18 consistent.
  For the curator: prompt 1 (axis), plus consistency bullets for builder issues 2 and 3.

------------------------------------------------------------------------------------------------------------------------
1. cow_id kept as a categorical feature of a known herd (USE-10, LEAK-34, CLEAN-3, CLEAN-14)  -> CONSISTENT

Precedents (entity ids kept as inputs under a temporal split, the entity recurring):
  - wisconsin_local_government_property_insurance_fund: `PolicyNum` an input, "the fund rates the members it has insured
    before (USE-10)", 97.6-98.8% of test members in training; with/without measured (LightGBM). Split by Andrej's CC
    2026-11-02, definition as reviewed by Lennart.
  - sendy_logistics_challenge: `Rider Id`, `User Id` categorical inputs, "known at pickup", 99.1-99.4% seen (Myunghwan's
    CC 2026-10-29; the definition shipped with PR #33).
  - uniform_soybean_tests_yield: `genotype` kept as a category, "a breeder knows which line a plot is" (LEAK-34).
  - airqo_low_cost_air_quality_monitor_calibration_challenge: `site` kept nominal (Lennart 2026-11-05, known sites).
  - ieee_fraud_detection `uid` kept (LEAK-34 case); corporate_credit_rating (USE-10 case, known entity).
  Milk: the robot identifies every cow; 98.1% of test rows (window mean; 98.8% pooled, split auditor) have a seen cow;
  the source's real-time protocol kept every cow in calibration and test. Same facts as wisconsin and sendy.
Contrasts checked, none a real opposite pair:
  - tunisian_fraud_detection_challenge dropped `CTR_MATFIS` (Lennart CC 2026-11-05) after building the taxpayer's
    previous label from it; its rationale is LEAK-33 (a group id is split metadata). milk declares no group, so LEAK-33
    is not triggered.
  - backblaze_hard_drive_failure_1m drops `serial_number`; 5g_energy_consumption keeps `BS` as a group only (every test
    station unseen): both cold-start or one-event-per-entity settings, unlike a herd re-read every milking.
  - USE-10 says "the previous outcome is a feature" for a known entity; milk builds none. Like wisconsin and sendy (id
    only); unlike tunisian (built on Lennart's choice, issue 1 B). The claim auditor measured no gain from the cow's
    last training-side fat (ridge 0.0984 alone, 0.0986 with it), so leaving it out is measured, not a departure.
  CLEAN-14: id as a string category, as Lennart's marks on issue #48 (ids categorical by meaning). Consistent.

2. Spectrum declared with `unit="bin"` rather than nm (CLEAN-26; spectra.md "What ships")  -> DEPARTS, reason weakened
   (prompt 1)

Precedents:
  - micro_mass (Lennart CC 2026-11-02, CLEAN-26 case): `bin` because "the m/z of the bins is not published".
  - pancreatic_cancer_mouse_detection (Lennart 2026-11-02): m/z from the source's own per-row M/Z column.
  - open_soil_spectral_library (Lennart 2026-11-04): cm-1 from the source's column names.
  - siblings of this batch (AI, not reviewed): bacteria_id_raman cm-1 from `wavenumbers.npy`; raman_mlrod cm-1 on the
    source's own grid (built by the source's code).
  - spectra.md: "When the source gives the axis in a separate file, build the names from it. When it gives no axis,
    number the bins (unit="bin", micro_mass)." The API (src/data_foundry/v2/spectra.py, Spectrum.unit): "`bin` when
    the source gives only a bin number".
Milk's facts: the data paper's Table 1 note b gives the range and the step ("960 nm to 1690 nm, at a resolution of
2.86 nm per pixel"; 960 + 255 x 2.86 = 1689.3); no per-pixel table. So the source gives more than a bin number and
less than a table: no precedent has these facts, so the curator's call sets the precedent for the NIR records to come
(mango_dmc_nir, beef_marbling_nir and the raman_* records publish their own grids, so they do not reopen it, but any
array-detector source that states only a range will).
The stated distinguishing fact (the band maxima at pixels 9, 74, 163 fall at 983, 1169, 1424 nm against the article's
970, 1200, 1450) is weakened: the claim auditor (T3) shows pixel 163 sits in noise (S - D about 13 counts) and that
the linear axis puts the source's own removed low-transmittance window (1360-1500 nm) at pixels 141-187, i.e.
1360-1492 nm, within about one pixel. What remains is that a grating array's pixel-to-wavelength map is a calibration
the source does not publish, so a linear nm axis is nominal.
Effect: none on the values or on any encoding (the vibrational default is as-is; the Savitzky-Golay candidate works
"per position on the grid (not per axis unit)"); only the container's metadata, which a wavelength-aware method or a
cross-dataset comparison would read. P7 only.

3. State `raw` (CLEAN-26)  -> CONSISTENT
  open_soil_spectral_library (Lennart 2026-11-04): KSSL absorbance, i.e. the instrument's referenced output, declared
  raw; "OSSL applies SNV inside its models, not in the table". Milk's Trans_Tot is the same kind of product: the
  standard (sample - dark)/(white - dark) referencing, with no smoothing, baseline, scatter correction or derivative.
  bacteria_id_raman (this batch) is `processed` for a fact milk does not share (polynomial baseline + 0-1 scaling).
  Note for the rules: spectra.md defines `processed` as "a baseline removed, a normalisation or a derivative applied
  by the source", and the source names Trans_Tot "Normalized". Two curators could read that word differently; one
  line in spectra.md ("referencing against the instrument's white and dark standards is raw", citing open_soil and
  milk) would prevent drift. No effect on the shipped encoding (vibrational: as-is for either state).

4. The instrument's dark, white and raw-count blocks dropped (CLEAN-26, USE-6; builder issue 2)  -> CONSISTENT IN
   KIND with open_soil, not in fact; already a weighing call
  Closest precedent: open_soil_spectral_library (Lennart CC 2026-11-05, issue 6): the depths and preparation code are
  known to a KSSL laboratory and left out as "a choice of actor", because the source's scan-upload service "accepts
  none of them" (they lowered RMSLE by 3.6%). The milk reason is of the same kind (the source's on-farm models read
  Trans_Tot only), but the fact differs: open_soil's chosen actor never receives the left-out inputs; milk's actor, the
  robot, holds the per-row dark, white and sample counts (read 39-144 s after milking end).
  Two rules lean the other way, and the curator should see them next to the option: USE-6's own "Why" ("dropping it
  changes the task into predict without ..."), and CLEAN-26's rationale (ship as published and leave processing to the
  benchmark, so "a method that processes spectra itself" keeps the signal); the claim auditor (T1) shows Trans_Tot
  cannot be rebuilt from the per-row pairs, so the blocks carry information Trans_Tot does not. Width is no argument
  either way (Tensions, coad, Lennart 2026-10-15); the builder does not use it.
  Not a departure without a reason, so no separate prompt. Suggested bullet for issue 2:
    **Consistency:** open_soil_spectral_library left out inputs a laboratory knows because the source's service takes
    none of them; here the robot itself holds the blocks, so the reason is the source's model input alone[^use6].

5. The 59 fresh-cow samples kept although the 2020 article removed them (CLEAN-11; builder issue 3)  -> CONSISTENT
   (the default), set apart from the drop precedents
  CLEAN-11: "the row stays"; a row whose target the source names as not the task's quantity "may leave, with the
  source's words". Drop precedents: ames_housing (De Cock's partial sales, Lennart 2026-10-21), sendy_logistics_challenge
  (short legs, Lennart 2026-11-05), mercedes_benz (single extreme training target). Keep precedent: open_soil (3 layers
  above 70% OC kept, unusual not impossible).
  Fact that sets milk apart from ames: in ames the data's own publication (De Cock 2011) recommends the removal; here
  the data's first publication (the 2023 data paper, same group) releases all 1,224 and names only the 46 samples
  without a reference as removed; the article that removed them is an earlier analysis. Also the use case (cow-health
  monitoring) meets fresh cows, unlike sendy's delivered parcels. The single-extreme clause does not apply: the 7.6%
  is a test row (week 8).
  New measurement for issue 3 (this checker, ridge on absorbance -log10(T), standardised, RidgeCV, shipped windows):
  the builder's "no effect" covers the fresh cows as TRAINING rows. As TEST rows they are 44 of 580 (20 / 18 / 6 / 0 in
  weeks 8 / 7 / 6 / 5) and carry 39.5% of week 8's squared error (RMSE 0.058 with them, 0.048 without); weeks 7 and 6:
  4.1% and 10.0%; four-window mean RMSE 0.098 with them, 0.096 without. A modest effect on one window's level, not on
  the call. Suggested bullet for issue 3:
    **Experiments:** as test rows the fresh cows hold 39.5% of week 8's squared error under ridge (RMSE 0.058 against
    0.048 without them) and change the four-window mean from 0.096 to 0.098.

6. Prot, Lact, SCC, Urea dropped as the same laboratory analysis (LEAK-10)  -> CONSISTENT
  caracas_cervical_cancer (Lennart CC 2026-10-15): four results of one work-up, the folder predicts the biopsy alone.
  open_soil_spectral_library (Lennart 2026-11-05): "other chemistry outcomes ... never enter its inputs (USE-3,
  LEAK-10)". sdss_17 `redshift` (LEAK-10 Mechanisms row: fitted from the same measurement that gives the label). Milk:
  one CombiFoss run on the same tube, reported within three days, after the prediction point. Same facts.

7. Temporal weekly windows against the source's week-1 calibration (SPLIT-19 vs SPLIT-14; SPLIT-12)  -> CONSISTENT
  The source's protocol (train week 1, 316 rows = 25.8%; test weeks 2-8, one window) breaks SPLIT-14 (a Must: at least
  3 windows, every train side >= 50%), which outranks SPLIT-19 (a Should). A Should yielding to a Must is no exception
  and needs no record line; the splits_comment states it. Regime: temporal, the one the use case implies (Tensions,
  "Temporal against grouped", Lennart 2026-10-12); the screening's grouped-by-cow option is correctly not taken.
  Closest precedent on horizon: medical_facility_operational_data (Lennart CC 2026-11-05): the source's two-week test
  horizon followed (SPLIT-12, SPLIT-19) because SPLIT-14 allowed it. Fact that sets milk apart: the 50% floor leaves
  only weeks 5-8 (580 rows) as test pool, so three or more non-overlapping windows can be one week each at most; the
  source's multi-week horizon cannot be mirrored, and the source itself asks for calibration maintenance ("By adding
  new samples to the calibration set ... the models can be made robust"; data paper "how to maintain them in time").
  The split auditor measured the same model ranking under both protocols. Other precedents: airqo (windows widened to
  cover both seasons, SPLIT-20, Lennart 2026-11-05), ppnn_ecmwf (source's test year vs two-week windows, open).
  Wording only (claim auditor 35): "cannot be a test window" should read "need not": the amended SPLIT-14's 40% clause
  is for a release with two windows above the floor, and here four are.
  Register: the SPLIT-14 "amendment_due" flag (5 datasets) is not fed by this case (no SPLIT-14 exception here).

8. RMSE as the source's RMSEP (MET-5, MET-1)  -> CONSISTENT
  open_soil_spectral_library (Lennart CC 2026-11-05, MET-5 case): the tuning criterion kept although the paper reports
  CCC and RPIQ beside it; forest_fires (ranked by MAD: kept). Milk: PLS selected by RMSECV, RMSEP reported, the sensor
  judged against ICAR's limits stated in RMSEP: one deliberate criterion with R2 reported beside it. Even under the
  strict reading of MET-5 the regression fallback is rmse, so the declared function cannot change; only `source` vs
  `fallback` would. The reference is the journal DOI read through the preprint (claim auditor: untested against the
  journal text, low risk).

9. Protein and lactose as other framings, not built (CLEAN-18, PROV-7)  -> CONSISTENT
  selection.md names "several soil nutrients" as the Multi-target example; open_soil_spectral_library ships organic
  carbon alone, caracas_cervical_cancer the biopsy alone (Lennart 2026-10-15), bias_correction one of its two targets.
  The record carries no `Multi-target` tag, so CLEAN-18 has nothing to remove. If the curator wants sibling folders
  (protein, lactose; Reiter et al. 2026 carry fat, lactose and urea), PROV-7 sets them apart as distinct tasks, each
  record saying why.

Drift: none. Lennart's spectrum calls (micro_mass, pancreatic 2026-11-02; open_soil 2026-11-04/05), known-entity id
calls (airqo, tunisian 2026-11-05) and LEAK-10 same-analysis drops (caracas 2026-10-15, open_soil 2026-11-05) run one way.
Third exception: none; this definition records no exception.

------------------------------------------------------------------------------------------------------------------------
PROMPT 1 (for the folder's REVIEW.md, as a turn on a new issue or appended to the builder's list)

**Consistency check (AI, 2026-11-09):** Number the 256 pixels as bins, though the source states their range and step?

* **Problem:**
  * The source gives the axis as a range and a step ("960 nm to 1690 nm, at a resolution of 2.86 nm per pixel"), and the only precedent for numbered bins, micro_mass, had no axis at all[^c26].
  * The stated reason, that the absorbance maxima do not line up with a linear axis, rests on a pixel in noise; on the source's own removed window (1360-1500 nm) the linear axis agrees within about one pixel.
  * No values or encodings change either way; the call sets the precedent for sources that state only a range and a step.
* **Background:** the source publishes no per-pixel calibration of the grating array, so any nm axis is the nominal one, 960 + 2.86 (p - 1).
* **Options:**

  | | Option | What it does | Pro | Con |
  |---|---|---|---|---|
  | a | Keep bins (implemented) | `unit="bin"`; the fact recorded as a case: the source publishes a range and a pixel width but no per-pixel calibration, so the axis is nominal | no wavelength the source did not tabulate; nothing to rebuild | the axis information the source gives is lost to the container; `bin` is documented as "only a bin number" |
  | b | Declare nm on the nominal axis | columns `nir_<960 + 2.86 (p - 1)>`, `unit="nm"`, the description saying the axis is the source's nominal linear one | keeps what the source states; matches its own 1360-1500 nm window within one pixel; wavelength-aware methods can read it | positions may be off by a pixel or two where the array is not linear |
  | c | Amend the spectrum guide | write the rule for range-and-step sources into spectra.md (one of a or b for every such case) | the next NIR source is decided alike | a rule from one case |

* **Recommendation:** b, with c's line in spectra.md so the next source with a stated range follows it; a if you hold that a nominal axis is not the source's axis.
* **Decision:** a, b or c?

[^c26]: **CLEAN-26** (Should): a spectrum ships as the source publishes it, one numeric column per position on its axis; spectra.md: "When it gives no axis, number the bins (unit="bin", micro_mass)"; the API: `bin` "when the source gives only a bin number". micro_mass, Lennart 2026-11-02: "the m/z of the bins is not published, so the axis is the bin number".

[^use6]: **USE-6** (Must): anything known at the prediction point is a legitimate input; "dropping it changes the task". open_soil_spectral_library, Lennart 2026-11-05: depths and preparation code left out as a choice of actor, the source's service accepting none of them.
```

</details>

<details><summary>Advocate</summary>

```text
ADVOCATE, OPENING BRIEF: milk_nir_composition (2026-11-09)
Position: ship as defined, with the documentation fixes below (no decision needed) and the curator's three
weighing calls plus one prompt left open. No panel agent found a broken Must; the one real P4 finding is a weak
LEAK-30 leak whose rule-preferred remedy keeps the dataset.

1. The task is valid at P1-P4, and an adversary could not break it.
   Evidence: claim auditor, "no validity claim refuted" (43 claims; values array_equal to the deposit). Domain
   practitioner: fit direct, one row = one milking = one decision, inputs held by the robot at milking end.
   Prot/Lact/SCC/Urea dropped as the label's own lab analysis. 0 exact copies across any split. Task gamer: "I could
   not game this task"; no exploit beat the honest model beyond the noise (~0.001 RMSE), including test-window
   centering (0.0961 vs 0.0960), pseudo-labels (0.0962) and cow-history correction (0.0949).
   Rules: USE-1, USE-5, USE-8 (P3); LEAK-10, LEAK-16 (Must, P4). These are the highest-ranked tests the dataset
   faces, and every one holds.

2. The split mirrors the use case; the departure from the source's protocol is forced by a Must.
   Evidence: 4 expanding windows, each one whole trial week (5-8), train 644-1,062 rows (oldest 52.6%), gap 3 d =
   lab delay, removes no row (split auditor). The source's train-week-1 protocol has a 25.8% train side. Cows recur
   (98.8% pooled), as on the farm and in the source's real-time evaluation; recurrence does not inflate the task:
   ridge 0.098 temporal vs 0.087 grouped by cow; cow_id helps only trees (0.268 -> 0.215).
   Rules: SPLIT-14 (Must) outranks SPLIT-19 (Should), so no exception is needed (precedent checker); USE-10 and
   SPLIT-13 make the known herd part of the task. Answers the blind reviewer's window concern 4: the windows are
   already the source's SET weeks.

3. The week-mean referencing (column auditor) is real, weak, and its remedy keeps the dataset.
   Concede: Trans_Tot is normalised with the mean dark/white of the whole trial week (exact to 5e-15 in 4 weeks),
   test rows' later readings included; curation_comments bullet 5, claims 17-18 and the builder's LEAK-27-31 row say
   otherwise and must be rewritten (EV-2) whatever the remedy.
   Weight: no label path (reference blocks alone = train mean, 0.719-0.867 vs 0.720-0.872); no train/test crossing
   (each window is its own week); effect <= 0.003 RMSE with mixed sign per window (window 1 PLS: shipped 0.159, causal
   0.151-0.153); the task gamer's transductive attacks found nothing.
   Rule: LEAK-30 is a Should when weak and "only a strong suspected leak makes it a reason for No". Remedy ladder
   (principles, step 5): repair from the origin first, i.e. the column auditor's option A, rebuild nir_bin_* from the
   deposit's own blocks with the trailing 30-min mean of pairs (ridge 0.0997 vs 0.0983, PLS 0.1097 vs 0.1095).
   Fallback B: keep Trans_Tot with a "Potential leak, kept on purpose:" note (bioresponse precedent). Either ships.

4. It is worth benchmarking (P6).
   Evidence: no task-probe flag; linear beats the dummy 4 of 4 windows (0.098 vs 0.798); cow mean alone 0.575;
   family spread linear - RF +0.090 (SE 0.016); ranking stable per window (LightGBM - ridge 3.5-7 SE). Best
   honest model 0.096 vs the source's RMSEP 0.083: headroom remains.
   Rules: TP-1 to TP-5, TP-9, TP-10. Answers the blind reviewer's concern 1 ("linear nearly saturates"): R2 0.985 is
   not TP-4 (no lookup; best single bin 0.809), and a task where inductive bias for spectra separates families by
   2.5x is what SEL-15/CLEAN-26 admit spectra for. The spectrum is already declared as a Spectrum, as the reviewer
   asked.

5. The metric is the source's and the practitioner's.
   Evidence: PLS selected by RMSECV, RMSEP reported and judged against ICAR limits (preprint, Table 4); domain
   practitioner: "Metric I would use: rmse"; per milking, unweighted, each milking a decision.
   Rules: MET-5, MET-1, MET-17. Uncontested by every agent.

6. The calls are consistent with precedent; the open ones are P7 or weighing calls, not blockers.
   Evidence: 7 of 8 calls consistent (precedent checker): cow_id kept as wisconsin PolicyNum / sendy Rider Id;
   LEAK-10 drops as caracas / open_soil; state raw as open_soil; fresh cows kept as the CLEAN-11 default, now with a
   stronger reason (domain practitioner: protein max 3.88%, not colostrum; FPR > 1.4 in 11.9% vs 2.0%, the cases
   monitoring exists for). The one departure, unit="bin", changes no value and no encoding (P7 metadata); its
   mildest fix is option b (nominal nm axis, within one pixel of the source's 1360-1500 nm window).
   Rules: USE-10, LEAK-10, CLEAN-11, CLEAN-26 (Should, P7). P7 problems are fixed when cheap, else kept with a note
   (principles, step 3); none reaches validity.

7. The blind reviewer's remaining changes are not rule failures.
   Datetimes: encoding is the pipeline's (CLEAN-2 precedent nyc_taxi); previous_milking is no exact copy (CLEAN-5);
   the task gamer found no gain from time features (non-spectral LGBM 0.547 vs dummy 0.798, explained by cow and
   interval). Prior use in arXiv 2605.21544 (and Reiter et al. 2026): an external collection, not a second copy of
   the first publication (PROV-4 to PROV-7 checked by the builder); a contamination note at most.

Changes that need no decision (documentation, EV-2/PROV-13/writing.md):
 - rewrite bullet 5 and the Spectrum description with the measured week-mean referencing; correct bullet 6's
   premise for issue 2 (the blocks hold per-row information Trans_Tot averages away);
 - "%" is the source's percent-transmittance convention, not a slip (claim auditor T2);
 - the sensor-timestamp drop reason: a proxy of yield (r 0.83);
 - "cannot" -> "need not" (week 4), "4 to 13 days apart" scoped to the test weeks; 98.1% (window mean) vs 98.8%
   (pooled);
 - notes: cow 50435's 2.59% reference is 75% of week 7's ridge squared error (kept, as the source did);
   fresh-cow reason strengthened; the source-protocol score (ridge 0.102 on 308/857).
For the curator: issue 1 cow_id (A keep), issue 2 instrument blocks, issue 3 fresh cows (A keep), the LEAK-30
remedy (A rebuild or B note), prompt 1 (axis).

Rebuttal
Overall: the critic and I agree on the outcome (ship after changes; nothing excludes the dataset). Its verdict
"ship after changes" is the right label for my position too, since its changes are fixes, not exclusions. Point by
point:

1. Week-mean referencing (P4/P5). CONCEDE, and I narrow my opening point 3. I offered rebuild (A) and a note (B)
   as equals. PROV-13 is a Must ("values scaled over all rows ... repair or rebuild from the origin when it has
   them"), and the deposit has the per-row Dark/White/Sample counts. So the rebuild is required, and B is a fallback
   only if the rebuild cannot be made. PROV-14 keeps it a repair under this record: same units, same 256 features,
   state raw. What follows: rebuild nir_bin_* in _clean. The only thing left to settle is which variant. The
   trailing 30-min mean of pairs matches the documented session/0.5 h procedure (data paper 3.1; ridge 0.0997, PLS
   0.1097). The row's own pair is the preprint's default (ridge 0.0996, PLS 0.1125). Both are causal and differ by
   less than the noise (task gamer, ~0.001-0.003), so either passes. I lean to the trailing mean because it is the
   documented deployment procedure; the 46 missing pairs make it an approximation, which the notes must say.
   Cost <= 0.003 RMSE.
2. False notes (EV-2). CONCEDE fully. These rewrites were already on my no-decision list: bullet 4 (the "%" is the
   source's percent-transmittance convention, claim auditor T2), bullet 5, bullet 6, the Spectrum description, and
   the builder's checklist row (LEAK-27-31 "no all-row statistic", PROV-13 "slip").
3. Block drop premise (USE-6). CONCEDE the premise. Trans_Tot discards the per-row references, so bullet 6's reason
   is false. After point 1's rebuild the blocks feed the shipped spectrum, so their information reaches every model.
   Whether to also ship the 768 raw columns stays builder issue 2, a weighing call (the blocks alone predict nothing:
   ridge = train mean). One limit: open_soil's "choice of actor" does not carry over, so USE-6 has to sit beside
   option A in the issue, as the critic asks.
4. Window levels hinge on single rows (P6). CONCEDE: add a note, no drop (CLEAN-11/PROV-13 default; SPLIT-17 met;
   rankings stable at 3.5-7 SE). Also add the domain practitioner's point on label richness (about 160 references a
   week vs about one per cow per 4-6 weeks) to fit_reason.
5. unit="bin" (P7). CONCEDE. Option b (nominal nm axis, described as nominal) is the mildest fix that meets
   CLEAN-26's documented meaning of `bin`. The spectra.md line is for the curator. It changes no value.
6. Wording and evidence fixes. CONCEDE all. Each is already on my no-decision list.

Agreed points the critic dropped: datetimes, arXiv 2605.21544, linear near-saturation, cow_id. No dispute remains
open. For the curator: the variant of the rebuild (trailing 30-min mean vs own pair), issue 2 (raw blocks), issue 1
(cow_id A), issue 3 (fresh cows A), prompt 1 (axis, b).
```

</details>

<details><summary>Critic</summary>

```text
CRITIC, OPENING BRIEF: milk_nir_composition (2026-11-09)
Folder: df-large/datasets/_dev/tabarena-v0pt2/milk_nir_composition/dataset.py

Position: ship only after changes. The task is real (USE-1, USE-8 direct, all seven reports agree) and nothing here
excludes it. But the main feature is not what the definition says it is, the definition's own text about it is false,
and the fix the rules ask for is cheap because the deposit holds the raw counts. Points in rank order.

1. P4/P5. The spectrum is referenced with a statistic over the whole week, test rows and later readings included.
   Problem: Trans_Tot = (Sample - mean_week(Dark)) / (mean_week(White) - mean_week(Dark)). The definition says a pair
   "at the start of each session and every 0.5 h" that "cannot be rebuilt".
   Evidence: column auditor a4/a8. I re-ran it on data_table.csv: the rebuild is exact to 5e-15 in weeks 2, 3, 7, 8.
   Weeks 1, 4, 5, 6 are off by 2e-4 to 2.1e-3, because the 46 unlabelled samples' readings were in the source's mean.
   Each test window is one week, so every test row's spectrum depends on the other test rows of its window and on
   readings up to about 45 h later (85 h in week 1). The robot "predicting at once" has none of them. The leak is weak:
   the reference blocks alone predict nothing (ridge = train mean), no train/test crossing, worth <= 0.003 RMSE
   (ridge 0.0983 shipped vs 0.0996 causal; PLS 0.1095 vs 0.1125).
   Rule: LEAK-30 (Should when weak): "Rebuild from the unprocessed values when the source has them". PROV-13 (Must):
   values scaled over rows are damage; rebuild from the origin when it has them. The deposit has the per-row Dark,
   White and Sample counts. P4/P5 outrank CLEAN-26's "as the source publishes it" (P7).
   Remedy: rebuild nir_bin_* in _clean from the row's own pair (the preprint: by default a pair "every time a milk
   sample spectrum was recorded") or from the trailing 30-min mean of pairs. The state stays raw. Fallback only if the
   curator refuses the rebuild: keep Trans_Tot with a "Potential leak, kept on purpose:" note giving the numbers above.

2. P5/evidence. The definition states false facts about its main feature.
   Problem: curation_comments bullet 5 (session/0.5 h referencing, "cannot be rebuilt") is wrong (point 1). Bullet 4's
   "Table 1 gives %, but the values are the plain ratio" is refuted: the source's absorbance of 4-5 at 1450 nm equals
   log10(100/T) (4.00-5.05), not log10(1/T) (2.00-3.05). That is claim auditor T2. Bullet 4's reason for bins rests on
   pixel 163, which sits in noise (S - D about 13 counts). The linear axis puts the source's removed 1360-1500 nm window
   at 1360-1492 nm (T3). The builder's checklist line "no all-row statistic" is wrong.
   Rule: EV-2 (Must): a measurement on the data outranks the page. PROV-13: record the paper/deposit mismatch.
   Remedy: rewrite bullets 4-6, the Spectrum description and the builder's PROV-13 row from the measurements, whatever
   point 1 decides.

3. P3/P4. The instrument blocks were dropped for a reason that is false.
   Problem: bullet 6 drops Trans_Dark/White/Sample (768 columns) as "the inputs of the referencing that Trans_Tot
   already carries". They are not: Trans_Tot uses the week mean and discards the per-row references (column auditor 3;
   claim auditor T1). The robot holds them 39-144 s after milking end. Precedent checker 4: open_soil's "choice of
   actor" does not carry over, because there the actor never received the inputs; here it does.
   Rule: USE-6 (Must): anything known at the prediction point is a legitimate input; "dropping it changes the task".
   Remedy: under point 1's rebuild the blocks become the inputs of the shipped spectrum, which settles most of it.
   Builder issue 2 stays a weighing call, but its premise has to be corrected and USE-6 placed beside option A. I
   accept that the blocks alone carry no label signal (ridge = train mean). So this asks for an honest reason, not
   necessarily wider data.

4. P6. A window's score level hinges on one or a few milkings. A note is needed.
   Problem: one test row (cow 50435, 2017-07-11 21:38, lab fat 2.59% between the cow's 4.3-5.5%) is 75% of week 7's
   squared error under ridge. It lifts the four-window mean from 0.080 to 0.098 (+22%). It is probably the preprint's
   -1.573 error, likely a lab or sample mix-up (split auditor 2, task gamer). The fresh cows hold 39.5% of week 8's
   squared error (precedent checker 5). The top 3 rows carry 38-79% of each window's squared error. Rankings stay
   stable (LightGBM - ridge at 3.5-7 SE).
   Rule: CLEAN-11 / PROV-13: the row stays by default, because the source kept it. SPLIT-17 is met.
   Remedy: a note in splits_comment or the notes naming the row and the numbers. No drop. Add the domain
   practitioner's point: about 160 references per week here against about one per cow per 4-6 weeks on a farm, so
   the benchmark is label-richer than practice (fit_reason).

5. P7. The spectrum is declared with unit="bin" although the source states range and step.
   Problem: spectra.md and the API reserve `bin` for "only a bin number" (micro_mass). The source gives 960-1690 nm at
   2.86 nm/pixel, and the stated reason for not using it is weakened (point 2).
   Rule: CLEAN-26 (Should). A departure needs a fact that sets the case apart, recorded as an exception.
   Remedy: precedent checker prompt 1, option b (nm on the nominal axis, described as nominal) with a line in
   spectra.md. Or keep bins and record the actual reason as an exception. Quality only, so no reason to hold the
   dataset.

6. Process (writing.md, EV-2). Wording and evidence fixes, cheap.
   - splits_comment: "cannot be a test window under SPLIT-14" should read "need not" (claim auditor 35). "Measurement
     weeks 4 to 13 days apart" is true only before the test windows (weeks 1-2: 2.1 d, weeks 2-3: 1.3 d).
   - Known-cow share: say 98.1% is the mean of windows; pooled it is 98.8%.
   - The reason for dropping the sensor timestamps is inaccurate: the offset tracks yield (r 0.83, partial r with fat
     -0.08). Keep the drop and correct the reason.
   - Fresh cows: the identification is now measured (dropping the five cows reproduces the article's Table 3,
     308/857). They are not colostrum (protein max 3.88%), and FPR > 1.4 occurs in 11.9% of them vs 2.0% of the rest
     (domain practitioner). Put this in the _decisions reason in place of "identified by their counts".

Considered and dropped (no rule backs them): the datetimes as features (CLEAN-2 precedent nyc_taxi leaves the
encoding to the pipeline); the published TabPFN result in arXiv 2605.21544 (PROV-15/EV-4: pretraining changes no
decision); linear near-saturation (no TP flag, family spread 3.5-7 SE); cow_id (USE-10, precedents wisconsin and
sendy).

Judgment record:
  Verdict: ship after changes.
  Validity: USE-1/USE-8 hold; LEAK-10 holds; LEAK-30/PROV-13 triggered (week-mean referencing), rebuild asked;
    EV-2 triggered (false notes), fix asked; USE-6 premise of the block drop false, correct it; SPLIT-* hold.
  Value: TP no flags; window levels hinge on single rows, so a note.
  Quality: CLEAN-26 unit="bin" departure, needs nm or an exception.

Rebuttal
I answer the advocate's opening brief. Its own rebuttal already concedes my six points, so most of what is left is
agreement. Three disputes remain, on details. None changes the verdict: ship after changes.

1. Valid at P1-P4, could not be gamed. CONCEDE the task's validity: USE-1/5/8, LEAK-10 and LEAK-16 hold, and the
   task gamer's attacks failed. I dispute "every one holds": LEAK-30 and PROV-13 (Must, P5) are triggered by the
   week-mean referencing. The advocate's point 3 concedes this. The task gamer could not exploit the leak, but that
   shows only that the leak is weak, not that it is absent. LEAK-6 (Must) says a confirmed leak goes even when small,
   and LEAK-30 narrows it to "rebuild when the source has the unprocessed values".

2. Split. CONCEDE. SPLIT-14 (Must) over SPLIT-19 (Should), USE-10/SPLIT-13 for the known herd; the windows are the
   source's SET weeks.

3. Week-mean referencing. CONCEDE the measurement and the weight. DISPUTE presenting A (rebuild) and B (note) as
   equals. PROV-13 is a Must and the deposit holds the per-row counts, so A is required and B is only a fallback if
   the rebuild fails. The advocate's rebuttal accepts this.
   On the variant, the curator's call: I lean to the row's own pair, against the advocate's trailing 30-min mean.
   - The "documented procedure" argument is weak, because the measurement shows the source did not follow its
     documented procedure (it used the week mean; EV-2 ranks the measurement above the paper).
   - The own pair is the preprint's stated default. It needs no other row, so it is exact on every row, while the
     trailing mean lacks the 46 unlabelled samples' readings, which the advocate also notes.
   - Its cost is measured: ridge 0.0996 vs 0.0997, PLS 0.1125 vs 0.1097.
   Either variant is causal and acceptable.

4. Worth benchmarking. CONCEDE the conclusion (no TP flag, spread 3.5-7 SE, not TP-4). DISPUTE one number: "best
   honest 0.096 vs source RMSEP 0.083: headroom remains" compares different protocols. The source trained on week 1
   only, used 1,165 samples and removed the water band. Without the one 2.59% row the shipped four-window ridge mean
   is already 0.080 (split auditor 2). So the gap to 0.083 measures that row, not headroom. Remedy unchanged: the note
   of my point 4. Do not cite 0.083 as headroom in the notes.

5. Metric. CONCEDE: MET-5, MET-1, MET-17.

6. Precedents. CONCEDE: cow_id, LEAK-10 drops, state raw and fresh cows kept are consistent. unit="bin" is P7 and
   fixed by option b. We agree.

7. Blind reviewer's changes. CONCEDE on the datetimes (CLEAN-2, nyc_taxi). DISPUTE "a contamination note at most":
   arXiv 2605.21544 should get no note at all. PROV-15 (Must) and EV-4 say another benchmark's scores and
   pretraining overlap "never" change a decision, and writing.md says to raise only what changes one. The paper may
   be named only for provenance or a duplicate, which the builder already checked (PROV-4 to PROV-7).

The advocate's no-decision list: CONCEDE, with two corrections. The fresh-cow reason should also cite the reproduced
Table 3 (308/857, claim auditor T4). The source-protocol score (ridge 0.102) should go in beside the shipped windows,
not as headroom (my point 4 above).

Settled between us: ship after changes; rebuild nir_bin_* causally (PROV-13); rewrite the false notes (EV-2);
correct issue 2's premise with USE-6 beside option A; note the single-row window levels; axis option b; the wording
fixes.
For the curator: the rebuild variant (own pair vs trailing mean), issues 1-3, prompt 1.
```

</details>
