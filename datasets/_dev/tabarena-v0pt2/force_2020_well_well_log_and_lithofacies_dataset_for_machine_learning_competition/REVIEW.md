# force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition

**Outcome:** added. The lithology (11 classes, log loss) of each depth sample in 118 North Sea wells, from all
three competition files stacked and split by well; GROUP and FORMATION stay as features, as the competition gave
them. Review panel: full tier, 2026-10-20. The AI recommends shipping after changes; the changes that needed no
decision (masks for sentinel remnants and impossible readings, a splits comment, reworded notes) are made.

```text
Verdict: ship after changes.
Validity: SEL-13 holds (well logs are sensor readings per depth, not an image); USE-1 holds; USE-8 not yet met: the
  fit says direct for a newly drilled well while GROUP/FORMATION may postdate that point (issue 2); LEAK-10 not strong
  for GROUP/FORMATION (kept, note reworded); SPLIT-1 holds (grouped by well: random forest log loss 0.315 on
  row-random folds against 0.763 grouped); SPLIT-19 departure kept with its reason, now in the splits comment; PROV
  holds (md5, pinned commit, CC BY 4.0).
Value: TP-1/TP-3 real signal (random forest 0.742 against class shares 1.288, LightGBM 0.872, linear 0.886); no_spread
  gone after the masks; TP-8 fold gap accepted (CC 2026-10-12); TP-6 the penalty matrix declared (amended TP-6).
Quality: CLEAN-10/CLEAN-11 fixed by masking; CLEAN-21 curves on a second scale, kept with a note (issue 8); CLEAN-14
  duplicate formation codes (issue 9).
Weighed: source +, size +, gap + (grouped multiclass), label noise - (reachable accuracy near 80%).
For the curator: issue 2 (a released-well use case or an approximate fit), issues 8
  and 9 (cleaning), issues 10 and 1 (confirmations).
```

**Main points:** Restate the use case as "a newly drilled or a released well" (keeps the fit direct) or mark the fit
approximate (issue 2); the competition's penalty matrix is declared (amended
TP-6); keep, mask or convert the curves on a
second scale (issue 8); merge the duplicate formation codes (issue 9); confirm the Basement drop (issue 10) and no
depth-window features (issue 1).

**Record fields that disagree with the definition:**

- `domain`: record `chemistry & material science`, definition `environmental science & climate`.

**Record judgment:** valid with concerns. Well logs are sensor readings per depth, not a vectorised image, so SEL-13
does not exclude them; the task is the source's own and the split by well mirrors it. The concerns: whether NPD's GROUP and FORMATION exist when a new well is first interpreted (issue 2), and label noise (the organisers put the reachable accuracy near 80%).

**Issues for Lennart:**

2. **Restate the use case so the NPD picks fit, or mark the fit approximate?** GROUP and FORMATION are the official
   stratigraphic picks of the Norwegian register (NPD): the depth where each named rock unit (a group, or a formation
   within it) starts in the well. The definition keeps them as features, as the competition did, and says
   `fit="direct"` for "a newly drilled well". But NPD publishes its picks after the well is reported, from the same
   completion and mud logs the labels were drawn from; at the first interpretation of a new well a geologist has the
   operator's own tops, not NPD's (domain practitioner). The units are defined by their rock, so the picks partly
   encode the label: 14,709 of 14,711 Halite rows lie in the Zechstein group, and 66% of group boundaries sit within
   0.76 m of a lithology change, against 23% of random depths.
   - Effect: for a newly drilled well, a model that gets NPD's picks may score better than one would in practice,
     where the interpreter has only the operator's tops. They are the strongest single features (macro AUC 0.85 for FORMATION, 0.83 for GROUP); dropping both
     raises a random forest's log loss from 0.764 to 0.809. Not a strong leak: with only depth and location they
     reach accuracy 0.44, below the 0.613 of always predicting shale, so dropping them is not required.
   - Implemented: kept as features, `fit="direct"`, the use case "a newly drilled well"; the note now gives the
     alignment numbers and says the timing is not settled.
   - Alternative (a), the advocate's and the mediator's lean: restate `question`, `use_case`, `fit_reason` and the
     split sentence as "a newly drilled or a released well" (USE-9). The labels were built for 118 released wells, and
     the practitioner calls interpreting the backlog of released wells "the larger real use", where "the NPD tops are
     exactly what I would use". The fit stays direct.
   - Alternative (b), the critic's fallback: keep the use case, set `fit="approximate"` and write the note as
     `Potential leak, kept on purpose:` (the kick precedent, USE-8 Cases).
   - Alternative (c): a logs-only task without GROUP and FORMATION.
   - Rule: USE-8 (Must), USE-9 (Should, narrows USE-8), LEAK-10. (a) departs from kick on a named fact (a
     released-well use case the source data were built for, as in 5g_energy_consumption); the factor against it is a
     use case rephrased only to excuse a gap. Keeping them only because the competition gave them would be the third
     such keep, after homesite and kick; a third keep for the same reason triggers a proposal to amend LEAK-38.
   - Recommendation: (a), written into all four text fields.
   - Decision: (a), (b) or (c).

8. **Curves on a second scale: keep, mask or convert?** In a few wells a curve is recorded in another unit than in
   the rest, and the competition files give no units. MUDWEIGHT (the drilling mud's density) has three scales:
   per-well medians of 0.13-0.17 in 19 wells, 1.08-1.80 in 9 and 156 in one (29 of 118 wells carry it). ROP (rate of
   penetration) in 25/6-2 has a median of 17,778 against 0.6-150 elsewhere (2,925 rows); SGR (spectral gamma ray) in
   34/12-1 and 35/11-15 S medians of about 0.01 against 46-106 (8,731 rows); ROPA in 34/4-10 R a median of 0.099
   against 10-82.
   - Effect: one number means different things in different wells. The scale is constant within a well.
     MUDWEIGHT's two main scales (19 and 9 wells) appear on every training side, so a model can learn them. The
     single-well scales (ROP 25/6-2, ROPA 34/4-10 R, MUDWEIGHT 16/10-2) and SGR's two wells do not: when such a well
     is tested, no training well shares its scale, and its readings are taken at face value on the wrong scale.
   - Implemented: kept as published; the notes name the wells.
   - Alternatives: drop MUDWEIGHT (college_scorecard, 2026-10-16: a section without a published conversion was
     dropped); mask the off-scale wells per curve (cheap and safe: it only removes values); convert the 0.13-0.17
     MUDWEIGHT wells from bar/m (x 10.2; the practitioner calls this well founded, but CLEAN-21 asks for a published
     conversion, and the LAS headers in the Zenodo zip, 170 MB, were not read).
   - Rule: CLEAN-21 (Should). Keeping needs an exception with the fact that sets it apart from college_scorecard:
     there the break was in time, so new rows sat on the other scale; here MUDWEIGHT's two main scales are on every training side. The
     advocate and the critic both support keeping.
   - Recommendation: keep MUDWEIGHT's two main scales as an exception to CLEAN-21 with that fact, and mask the
     single-well and two-well off-scale curves (cheap and safe).
   - Decision: the recommendation, keep all (exception), drop MUDWEIGHT, or mask every off-scale well.

9. **Merge the duplicate formation codes?** Three rock units appear under two FORMATION codes, never in the same well:
   Grid Fm. (15 wells) and Grid Mb. (2), Skade Fm. (20) and Skade Mb. (4), Ty Fm. (13) and Ty Mb. (2). The pairs come
   from older and newer NPD naming (the unit ranked as a formation or as a member); their label mixes are similar
   (Skade 86% and 85% shale, Ty 77% and 75% sandstone).
   - Effect: a model sees two levels for one unit, and the rarer code is learnt from 2-4 wells. Small.
   - Implemented: kept as published. Alternative: map Mb. to Fm. for these three, after checking NPD's nomenclature.
   - Rule: CLEAN-14 (Should: one meaning, one code). Only the column audit raised it.
   - Recommendation: map them once the nomenclature check confirms the pairs.
   - Decision: map, or keep with a note.

10. **Confirm the Basement drop, and record it as a case of CLEAN-17?** CLEAN-17 (Should) keeps the rare classes of
   the source's labels. The Basement class has 103 rows, all in well 16/4-1, so no split by well can both train and
   test it; the definition drops it and 11 classes remain. It is the first class dropped for living in one group, so
   it would get a row in CLEAN-17's Cases table (a knowledge-file change).
   - Implemented: dropped, with the fact in the notes. Alternative: keep it; the fold that tests 16/4-1 then holds a
     class no training side has.
   - Recommendation: confirm and add the Cases row.
   - Decision: confirm (with the row), or keep the class.

1. **Depth context: confirm that the rows ship without depth-window features?** A model may use the other depths of
   the same well (`context="all_rows"`: the whole log exists before it is interpreted), but the dataset ships one raw
   row per depth; features over a window of depths (gradients, rolling means), as the winners built, are left to the
   pipeline.
   - Evidence: gradients plus 21-sample means and spreads of 9 logs per well move a random forest's log loss from
     0.776 to 0.764 (better on 2 of 3 folds). Neither side of the debate argued for them.
   - Effect: an interpreter reads curve shapes over metres; a row-wise model sees one 15 cm sample, so it is scored
     on a slightly harder task than the real one (the gain from window features is small, above).
   - Implemented: raw rows, `context="all_rows"`, no window features (as open_university). Alternatives:
     `context="none"` (each depth from its own row), or window features in `_clean`, as electric_motor adds the source
     study's features (set apart: there the features are the publishers' own and the row alone cannot carry the
     state).
   - Rule: a weighing call (CLEAN-2, CLEAN-19, USE-3).
   - Recommendation: confirm.
   - Decision: confirm, or add window features, or `context="none"`.

**Review panel:** ship after changes (mediator). The mediator's issues 1-6 are this file's issues 2, 4, 8, 9, 1 and
10; its issue 7 (TabArena's LightGBM default diverged here) moved to the working copy's REVIEW.md; after the masks the
untuned LightGBM of the task probes no longer diverges (log loss 0.872, was 2.68).
Claim audit: about 50 claims, most hold; refuted and now fixed: the reading of the "10% of group boundaries" figure,
the LAS-null bullet (partly refuted), the 34/5-1 wording, stale probe numbers; untested: the Zenodo LAS files (labels and MUDWEIGHT units).
Blind review: include with small changes; its main concern is GROUP and FORMATION as interpreted stratigraphy.
Debate: agreed on the split, the masks, the splits comment and the domain; disputed: the remedy for the fit (issue
2) and whether TP-6 is triggered (issue 4).

<details><summary>Mediator</summary>

Inputs: the claim, column and split audits, the practitioner, the blind review, the precedents, both briefs and
rebuttals, `dataset.py`, the record and the earlier REVIEW.md. One check run here on the cleaned frame (1,429,591
rows). Issue numbers below are the mediator's own (see the summary line for this file's).

**1. Recommendation (judgment record)**

```text
Verdict: ship after changes.
Validity: SEL holds (well logs are sensor readings per depth, not an image); USE-1 holds; USE-8 not yet met: the
  fit says direct for a newly drilled well while GROUP/FORMATION may postdate that point (issue 1); LEAK-10 not strong
  for GROUP/FORMATION (kept, note reworded); SPLIT-1 holds (grouped by well, IID 0.315 vs grouped 0.763);
  SPLIT-19 departure kept, written in a splits_comment; PROV holds (md5, pinned commit, CC BY 4.0).
Value: TP-1/TP-3 real signal (RF 0.744 vs class shares 1.284, linear 0.880); TP-8 fold gap accepted (CC 2026-10-12);
  TP-6 metric is a rule question (issue 2).
Quality: CLEAN-10/CLEAN-11 fixed by masking (changes 3-4); CLEAN-21 off-scale curves noted, exception or drop for the
  curator (issue 3); CLEAN-14 duplicate formation codes (issue 4).
Weighed: source +, size +, gap + (grouped multiclass), label noise - (reachable accuracy near 80%).
For the curator: issue 1 (fit: released-well use case or approximate), issue 2 (TP-6 against definitions.md).
```

Both sides reach this verdict. No point needs a remedy above "fix the definition".

**2. Changes to make now (no decision needed)**

1. **Reword the GROUP/FORMATION note** (LEAK-10, EV-6, EV-8). Drop the "only 10% of the 574 group boundaries" reading.
   Write instead: boundaries are 4x enriched over the 2.5% base rate (within 0.76 m: groups 65.7%, formations 62.8%,
   against 23.4% at random); the labels and the NPD tops draw on the same post-well material (completion and mud
   logs); 14,709 of 14,711 Halite rows are in Zechstein; four formation names state a lithology (0.66% of rows); every
   top has Interpreter NPD. Effect of dropping both: RF log loss 0.764 -> 0.809. Both sides agree.
2. **Add a `splits_comment`** (SPLIT-19; definitions.md asks for one when the split departs from the source's). Name
   the departure from 98/10/10 and the organisers' reason; say test wells have drilled neighbours (median 8 km, 55-76%
   share a licence block), so the score stands for wells in explored areas (0.763 by well, 0.814 by block, 1.015 by
   quadrant). Agreed.
3. **DRHO: mask the curve in 36/7-3 and 31/4-10 only**, plus a bullet (CLEAN-11, impossible as a correction). Both
   sides proposed `|DRHO| > 1` "about 5.7k rows"; measured here, that threshold masks **9,021** rows: the two wells
   (5,682) plus 3,339 rows in 28 other wells, median -1.16, 0.7-8% of each well's DRHO rows. Those are bad-hole
   readings (unusual, not impossible; CLEAN-11 keeps them). So mask the two wells by name; the one -7,429.3 value is
   caught by change 4.
4. **Mask sentinel remnants and impossible values, and fix the bullet** (CLEAN-10, CLEAN-11; precedents sdss_17,
   heart_disease_va_long_beach, churn_telco_south_asia). Values below -900 in the log curves, not Z_LOC (DRHO 1, RXO 2,
   ROPA 2 rows); negatives of RMED 7, RXO 131, SGR 39, ROP 52, ROPA 20 (ROPA's 20 were not in the briefs); DCAL > 100
   (2). The bullet must say the LAS nulls are masked in all 20 curves, not "in RXO, SP and ROPA" (also the `LAS_NULLS`
   docstring). Agreed.
5. **Name the off-scale wells in a note** (CLEAN-21): ROP 25/6-2 (median 17,778, 2,925 rows), SGR 34/12-1 and
   35/11-15 S (median about 0.01, 8,731 rows), ROPA 34/4-10 R (median 0.099), next to the MUDWEIGHT anomaly. Keep or
   mask is issue 3. Agreed.
6. **Write the metric facts in the notes** (TP-6, interim; both sides agree): the penalty matrix scores hard labels,
   and the top three trained on multiclass log loss (retrospective p. 3-4).
7. **Correct stale or refuted text** (EV-8): `no_spread` bullet to linear 0.880, gap 0.107 skill, LightGBM 2.678; name
   the forest behind 0.31/0.78/0.84 (the audits reproduce 0.274-0.315 / 0.763-0.764 / 0.809); 34/5-1 A and S "share
   2,273 MD values but no identical readings, 1.5-1.9 km apart at equal MD", both in one fold.
8. **Name the known gap in `fit_reason`** (USE-8): the labels were drawn with mud logs and in-house data the model
   does not get, which caps accuracy near 80% (practitioner; blog p. 3, p. 9). Undisputed.
9. **Domain to "environmental science & climate"** in definition and record (treat like cases alike: covertype,
   forest_fires; the current value is imported, not a curator decision). Both sides and the practitioner agree.
10. **Record**: replace "no known risk" with the GROUP/FORMATION timing (issue 1); "all 13 finalists used tree
    ensembles" -> "12 of 13 used only tree ensembles" (DapoA also used a tensorflow network).

**3. Issues for the curator, ranked**

1. **GROUP/FORMATION timing and the fit (P3/P4; USE-8 Must, USE-9 Should narrows USE-8, LEAK-10).**
   - Problem: the text says "a newly drilled well" and `fit="direct"`; for a new well the interpreter has the
     operator's tops, not NPD's (practitioner). As written it does not meet USE-8: kick, with fields of uncertain
     timing kept on purpose, is `approximate`.
   - Effect: GROUP/FORMATION are the strongest single features (macro AUC 0.85/0.83); dropping both costs RF log loss
     0.764 -> 0.809. Not a strong leak (on their own with depth and location: accuracy 0.44 below majority 0.613), so
     dropping is not required.
   - Advocate: (a) restate as "a newly drilled or a released well" with `direct` (USE-9): the labels were built for
     118 released wells; the practitioner calls the backlog "the larger real use", where "the NPD tops are exactly
     what I would use".
   - Critic: (a) is acceptable only if `question`, `use_case`, `fit_reason` and the split sentence ("wells never
     interpreted") change; otherwise (b) `fit="approximate"` with `Potential leak, kept on purpose:`.
   - Weigh against (a): "a use case rephrased only to excuse a gap" (USE-9 factor). For (a): the restatement follows
     how the source assembled the data, not the gap.
   - Decision: (a), (b), or (c) a logs-only task. Mediator leans (a), applied in all four text fields. What would
     settle it for new wells: when NPD publishes tops relative to the first lithology interpretation.
2. **Metric: TP-6 against definitions.md (P6, Must; rule question).**
   - TP-6 says a source's "scoring it uses" replaces ours when it is the better version; definitions.md says a
     competition keeps our default. Same commit, no dated curator precedent either way (amex, allstate, porto, 5g,
     sepsis ship competition metrics; african_credit keeps the default).
   - Advocate: TP-6 is not triggered; the matrix scores argmax labels, cannot rank probabilities, the winners trained
     on log loss, the practitioner wants probabilities. Critic: the texts contradict; a Must has no exceptions, so it
     needs an amendment.
   - Both are right in part: on these facts log loss passes TP-6's "better version" test, but the two texts still
     contradict. Decision: amend TP-6 or definitions.md so they agree; for this dataset, log loss (default) or an
     11 x 11 expected-penalty metric. Ships either way.
3. **Curves on a second scale (P7; CLEAN-21 Should).** MUDWEIGHT (three scales; 29 of 118 wells), ROP, SGR, ROPA
   (change 5).
   - Both sides: keep, as an exception: the scale is constant per well and every fold trains on each scale, unlike
     college_scorecard's break in time.
   - Alternatives: drop MUDWEIGHT (college_scorecard: no published conversion, dropped); mask the off-scale wells per
     curve; convert the 0.13-0.17 MUDWEIGHT wells as bar/m (practitioner: well-founded; CLEAN-21 asks for a published
     conversion).
   - What would settle the conversion: the LAS headers in the Zenodo zip (170 MB, not read; claim untested).
   - Decision: exception with that fact, or drop/mask.
4. **Duplicate formation codes (P7; CLEAN-14 Should).** Grid Fm./Mb. (15/2 wells), Skade Fm./Mb. (20/4), Ty Fm./Mb.
   (13/2), never in one well, similar label mixes. Only the column audit raised it. Decision: map Mb. to Fm. after
   checking NPD's nomenclature, or keep with a note.
5. **Close the earlier REVIEW.md issue 1 (depth context; Weigh).** Neither side argued it; keep `context="all_rows"` with no
   window features (open_university; window gain small, 0.776 -> 0.764). Decision: confirm.
6. **Confirm the Basement drop as a CLEAN-17 Cases row** (first class dropped for living in one well; 103 rows,
   16/4-1). Decision: confirm.
7. **Not a dataset change:** check TabArena's LightGBM default here (default `min_child_weight` 0.001 diverges, log
   loss 2.68; with 1, 0.81). And the record's "update GitHub issue" follow-up (TabArena/tabarena_dataset_curation#2).

**4. Agreed facts**

- 118 wells (98/10/10), 1,429,591 rows after dropping Basement, 11 classes, one sample every 0.152 m; md5 and pinned
  commit match; CC BY 4.0, logs NLOD 2.0.
- Grouped by well: 37/40/41 test wells, no well on both sides; RF log loss 0.763 grouped vs 0.315 row-random; another
  well assignment 0.759; no log vector shared across wells.
- Signal: RF 0.744 vs class shares 1.284 and linear 0.880; `no_spread` is untuned LightGBM diverging.
- Halite (4 wells) and Anhydrite (10) absent from test fold r0f2; every train side holds all 11 classes.
- GROUP/FORMATION: NPD picks (Interpreter NPD on all tops), reproduced from the Zenodo tables on 100%/99.95% of rows;
  4x boundary enrichment; given as inputs by the competition; not a strong leak; keep them.
- Confidence column recorded with the label, dropped correctly; Basement only in 16/4-1.
- DRHO holds RHOB in 36/7-3 and a density curve in 31/4-10; sentinel remnants and impossible negatives remain (counts
  in change 4); ROP/SGR/ROPA/MUDWEIGHT wells on other scales.
- The penalty matrix scores hard labels; the top three trained on log loss.
- Stale text: probe numbers, 34/5-1 wording, "13 finalists", "no known risk".

**5. Consistency with precedent**

- Split: follows superconductivity (SPLIT-4) and the source's held-out wells. Consistent.
- Context, no window features: follows open_university; electric_motor set apart (source's own features, real-time
  use). Consistent.
- GROUP/FORMATION: option (b) follows kick; option (a) departs from kick on a named fact (a released-well use case
  the source data were built for; USE-9, as 5g_energy_consumption). Recording the keep only as "the host gave them"
  would be the third such keep after homesite and kick (amendment watch, LEAK-38).
- Masks: follow sdss_17, heart_disease_va_long_beach, churn_telco_south_asia (CLEAN-10/11). Masking DRHO by well and
  not by threshold follows CLEAN-11's "unusual values stay".
- MUDWEIGHT: departs from college_scorecard; the distinguishing fact (constant per well, every scale on both sides)
  is stated, but the exception is the curator's (issue 3).
- Metric: no dated precedent on either side; rule-level contradiction (issue 2).
- `no_spread`: follows mice_protein (SPLIT-27). Fold gap: follows micro_mass, asp_potassco; the register's pair with
  alvin_smart_money_management is not a real pair (8 rows vs 14,711).
- Domain: follows covertype, forest_fires (change 9).

</details>

<details><summary>Claim audit</summary>

Adversary of the definition. The frame and splits were rebuilt from the definition (1,429,591 x 28, 3 grouped
folds). Claim numbers follow the panel's claim list.

**Table**

| # | Claim | Source | Test | Result | Evidence | Rule |
|---|---|---|---|---|---|---|
| 3, 15 | One depth sample every 0.152 m of one of 118 wells | D task_summary, curation_comments | count wells, median step | holds | 118 wells; step p01-p99 0.152 m | EV-1 |
| 4 | 11 classes | D | value counts after clean | holds | 11 | USE-5 |
| 5, 12, 17 | Every feature is known once a well is logged | D | read the sources on how GROUP/FORMATION and the label are made; boundary alignment | **untested at the moment the claim is about; implied independence refuted** | Labels: Explocrowd "hand crafted lithology interpretation using inhouse data, completion logs, mud logs, and of course the wireline curves" (blog p. 3). NPD tops come from the same post-well material (completion reports). Lithostratigraphic units are defined by lithology. GROUP boundaries on a lithology change at the same sample 10.1% vs base rate 2.5% (4.0x); within +-5 samples (0.76 m, the whole-metre rounding of NPD MD) 65.7% vs 23.4%. FORMATION: 10.2% / 62.8% vs the same base rates. | USE-3, LEAK-1, LEAK-10, EV-6 |
| 6, 46, 47 | The same well's other depths may be used; starter-notebook quote | D task_summary, Grouping | read starter notebook | holds (quote verbatim, except the notebook says 83 wells) | "The `WELL` column is included so the data can be separated per well. This will be necessary for any \"windowed\" approaches ..." | SPLIT-24 |
| 7, 66 | Whole wells held out in 3 folds, about 39 per fold | D | fold of every well | holds | 37 / 40 / 41 test wells; each well in exactly one fold | SPLIT-1 |
| 8, 20, 77 | Three files pooled, split by well across 118 | D, R | load | holds | 98+10+10 wells, no well in two files | SPLIT-5 |
| 9, 24, 64 | Confidence recorded with the label, dropped | D | starter notebook | holds | "FORCE_2020_LITHOFACIES_CONFIDENCE: confidence in lithology interpretation (1: high, 2: medium, 3: low)", listed under "the interpretation" | LEAK-10 |
| 10, 27, 65, 67 | Basement: 103 rows all in 16/4-1; others at least 4 wells | D | facts.txt | holds | 103 rows, 1 well; Halite min 4 wells | TP-8 |
| 13, 32, 79 | GROUP/FORMATION are NPD's picks, not the FORCE interpreters' | D fit_reason, comments | read Zenodo NPD tables | holds literally | Interpreter = NPD on 855/855 group tops and 1914/1914 formation tops, whole-metre MD. But see claim 5: "not the interpreters'" does not make them independent of the lithology (completion-log sources shared, 4x boundary enrichment). | PROV-1, EV-2 |
| 14 | Four files, 98 / 10 / 10 wells, hidden_test has labels | D | load | holds | facts.txt | |
| 16 | Competition task: logs, NPD lithostratigraphy, X/Y (GitHub readme) | D | read top-level readme | holds | "predict lithology labels for provided well logs, provided NPD lithostratigraphy and well X, Y position" | USE-1 |
| 18, 19, 63 | 1,429,694 rows stacked; open-test features and labels aligned | D | load (asserts pass) | holds | rebuild succeeded | |
| 21, 66 | Organisers found the blind set too small to represent the lithologies | D | blog post | holds | blog p. 3: "With hindsight we should have chosen a larger blind dataset since we are not fully representing the lithology distribution of the train dataset with the blind dataset" | SPLIT-5 |
| 22 | Neighbouring depths nearly identical | D | lag-1 correlation within wells | holds | GR 0.9945, RHOB 0.9938, NPHI 0.9914, RDEP 0.9926, DTC 0.9974; label changes on 2.8% of consecutive samples | SPLIT-29 |
| 23 | RF log loss 0.31 row-random vs 0.78 grouped | D | own RF (100 trees, leaf 5, 200k train / 100k test rows per fold) | holds in direction and size; source forest not named | row-random 0.274, grouped 0.764 (0.782/0.798/0.713) | SPLIT-29, EV-8 |
| 25 | Confidence missing for open-test wells | D | facts.txt | holds | column absent from open-test files | |
| 26, 60 | Code-to-name map from the starter notebook | D | read notebook | holds | `lithology_keys` identical, 12 pairs | |
| 28 | The LAS nulls become missing in RXO, SP, ROPA | D | raw values below -900 per curve; neighbours of leftovers | **partly refuted** | The exact nulls are masked (RXO -999.0 x18,172 and -999.9 x16,309; SP -999.0 x402; ROPA -999.25 x24). Interpolation ramps from a null into real data survive: RXO 15/9-15 -995.86, -861.23 then 0.594; RXO -968.05, -69.02; ROPA 35/8-4 a ramp -720, -876, -966, -809, -653; ROPA -948.95 next to NaN; DRHO 25/9-1 -7429.3 next to NaN. Also impossible negatives: RXO 131 rows, SGR 39 (a -196.87 plateau in 15/9-17), ROP 52 (26/4-1), RMED 7 (16/11-1 ST3). | CLEAN-10, CLEAN-11 |
| 29, 30 | Spikes stay (Zenodo quote); only WELL, DEPT, GR guaranteed | D | Zenodo API, starter notebook | holds | "slightly cleaned up and partially despiked"; "The only log columns that are **guaranteed** to be present are WELL, DEPT, and GR"; GR missing 0.000 | |
| 31 | WELL, GROUP, FORMATION categorical | D | dtypes | holds | 3 categorical, 24 float; WELL is the group column, not a feature (report.py) | |
| 33 | Only 10% of 574 group boundaries fall on a lithology change at the same sample | D | c_bound.py | **number holds, the inference it is offered for is refuted** | 58/574 = 10.1%; the base rate at a random sample is 2.5%, so boundaries are 4x enriched; within +-0.76 m 65.7% vs 23.4%. The sentence reads as weak alignment; the data show strong alignment. | EV-6, LEAK-10 |
| 34 | The competition gave GROUP/FORMATION as features | D | readme, starter notebook | holds | "GROUP: NPD lithostratigraphy group" in the starter notebook's metadata | TP-6, USE-4 |
| 35, 89 | Without both, RF log loss 0.78 to 0.84 | D, the earlier REVIEW.md | d_rf.py | holds in direction; size 0.764 to 0.809 here | per fold 0.813/0.845/0.769; without X/Y 0.790 | EV-8 |
| 36 | 34/5-1 A and S share no depth sample and lie 1.1-1.9 km apart where depths overlap | D | b_345.py | **wording refuted, conclusion holds** | They share 2,273 MD values (3544-3899 m), but no identical readings (GR corr -0.26, label agreement 0.54). Horizontal distance at equal MD 1.51-1.87 km; at equal TVD 1.89-2.15 km: neither is 1.1-1.9. Both wells are in fold 2, so they never straddle the split. No other parent has two wellbores. | SPLIT-23, EV-8 |
| 37 | no_spread: LightGBM 2.77; RF 0.744; dummy 1.284; linear 0.989; gap 0.19 skill | D | task probe JSON | **refuted (stale)** | today: LightGBM 2.678 (+-2.51), RF 0.744, dummy 1.284, linear 0.880 (skill 0.313), RF-linear gap 0.107 skill | EV-8 |
| 38 | MUDWEIGHT on three scales, no unit | D | facts.txt | holds for scales; the LAS-header part untested (LAS zip 170 MB not fetched) | medians 0.132-0.174 (19 wells), 1.078-1.797 (9), 155.77 (1) | PROV-13, CLEAN-21 |
| 39 | Reachable accuracy near 80% (blog p. 9) | D | blog | holds | p. 9: "no team managed to get much above the 80% score on the blind dataset. The 80% may represent the combined uncertainty in the input labels..." | USE-5 |
| 40, 93 | Log loss, not the competition's penalty matrix | D | retrospective, Zenodo | holds as a description; TP-6 open | retro p. 1-4: penalty matrix scored hard labels; top three trained on log loss ("relied on a standard multiclass log-loss"); the matrix ships in the Zenodo record | TP-6 |
| 41 | No duplicate rows or (WELL, DEPTH_MD) pairs | D | facts.txt | holds | 0 and 0 | LEAK-16 |
| 44 | Blog quote p. 3 | D Grouping | blog | holds | verbatim on p. 3 | |
| 45 | Scored per sample as in the competition | D | starter notebook formula | holds | S = -(1/N) sum A over samples | |
| 48-52 | Halite/Anhydrite wells, rows and per-fold counts | D accepted warning | facts.txt | holds | 4 / 14,711; 10 / 1,807; r0f2 tests none; train sides hold both | TP-8 |
| 53 | domain chemistry & material science | D | compare with peers | untested (judgment); covertype, the nearest geoscience peer, uses environmental science & climate | | PROV-9 (weigh) |
| 54, 80 | CC BY 4.0; logs NLOD 2.0 | D, R | Zenodo API | holds | license cc-by-4.0; description "provided by a NOLD 2.0 license" (sic) | EV-4 |
| 55, 56, 58 | Pinned commit; files unchanged since 2020-11-13; md5 | D | gh api commit history per file | holds | each of the four files has one commit, 319a6fba7e 2020-11-13; md5 matched in checklist | |
| 57, 78 | Zenodo LAS files hold the same 118 wells and labels | D, R | | untested (170 MB zip not downloaded) | | EV-7 |
| 59, 87 | bibtex authors in Zenodo order | D | Zenodo API | holds | Bormann, Aursand, Dilib, Manral, Dischington | PROV-10 |
| 61 | LAS nulls left in RXO, SP, ROPA | D | raw scan | holds for exact nulls; DRHO's -7429 is a different spike | | |
| 62 | float32 nulls -999.9000244, -999.2501221 | D | raw read as float64 | holds | RXO -999.9000244, ROPA -999.2501221 | |
| 75 | XGBoost first and second, RF third | R | retrospective p. 3-4 | holds | Olawale and GIR XGBoost, ICA RandomForest | SEL-12 |
| 76 | All 13 finalists used tree ensembles | R | grep the 13 code folders | mostly holds, not quite | 12 folders import XGBoost/LightGBM/CatBoost/RF/ExtraTrees; DapoA also imports tensorflow (Sequential/Dense) next to LightGBM and RF; JiampiersC loads a pickle (XGBoost per blog p. 17) | SEL-12 |
| U1 | No row is a copy across the split | implied | sidetracks, exact copies, nearest wells | holds | one parent with two wellbores, same fold; leak probe exact copies 0.0%; nearest other well at least 686 m (34/5-1 pair), next 1.85 km | LEAK-16 to LEAK-21 |
| U2 | The split is the one the use case needs | implied | | holds | new wells, whole wells held out; the source held out whole wells | SPLIT-1 |
| U3 | The target is the real-world target | implied | blog | holds with stated noise | hand interpretation is what the geologist produces; the blog finds wrong labels (p. 8: "the limestone label supplied by FORCE is entirely wrong") | USE-5 |
| U4 | Position X/Y always known | implied | missing share | holds | 0.8% missing; dropping X/Y raises RF loss 0.764 to 0.790 | |

**Refuted and untested, ranked (principles.md: validity first, Must first)**

1. **P4, LEAK-10 / USE-3 (Must when strong): claims 5, 12, 17, 13, 33, "every feature is known" and the independence the
   NPD note implies.** Literal statements hold (NPD interpreted the tops), but the reasoning that this separates them from
   the label does not: the labels were built from completion logs and mud logs (blog p. 3), the same post-well material NPD
   tops come from, lithostratigraphic units are defined by lithology, and group boundaries sit on lithology changes 4x more
   often than chance (66% within 0.76 m vs 23%). The 10% figure in the definition reads the other way. Whether the tops exist
   when a new well's lithology is interpreted remains a domain question (maybe a leak, EV-6). What it changes: the fit may
   be `approximate`, not `direct`, and the `fit_reason` and the GROUP/FORMATION note overstate independence. Mildest
   remedy: keep the features (the source's task lists them, TP-6/USE-4), reword the note to give the 4x enrichment and the
   shared sources, and let the curator decide the fit on REVIEW issue 2; the cost of dropping them is 0.764 to 0.809 log
   loss (own RF).
2. **P3/P6, TP-6 (Must), claim 40: untested as a decision.** The source defines a scoring (penalty matrix, in the Zenodo
   record). Remedy: register an expected-penalty metric or write the fact that sets the case apart (the matrix scores hard
   labels; the top three trained on log loss, retro p. 3-4).
3. **P5, claims 57/78 untested**: the Zenodo LAS labels equal the CSV labels; MUDWEIGHT units absent from LAS headers
   (claim 38). Remedy: download the LAS zip once and diff; harmless if skipped since the CSVs are the competition's files.
4. **P7, CLEAN-10/CLEAN-11 (Should), claim 28 partly refuted**: interpolation ramps from LAS nulls (RXO -995.86/-861.23,
   -968.05; ROPA ramp to -965.88; ROPA -948.95; DRHO -7429.3) and impossible negatives (RXO 131, SGR 39, ROP 52, RMED 7
   rows) survive. Effect tiny (a few hundred of 1.43M rows). Remedy: mask values below -900 and negative values of the
   resistivity, gamma-ray and ROP curves with one bullet, or keep them under the "spikes stay" note and say so.
5. **Procedure, EV-8, claim 37 refuted (stale)**: linear 0.989 / gap 0.19 / LightGBM 2.77 vs 0.880 / 0.107 / 2.678 today.
   Remedy: update the numbers; name the forest behind 0.31 / 0.78 / 0.84 (this audit reproduces 0.274 / 0.764 / 0.809).
6. **Procedure, claim 36 wording refuted**: the two wellbores do share 2,273 MD values and lie 1.5-1.9 km apart at equal
   MD (1.9-2.1 km at equal TVD); the conclusion (two groups) stands and both sit in one fold. Remedy: "share no readings"
   and the measured distances.
7. **Record, claim 76**: one finalist (DapoA) also used a tensorflow network; "all 13 used tree ensembles" overstates.
   Remedy: "12 of 13 used only tree ensembles". Domain (claim 53) is a weigh call: geoscience peers use environmental
   science & climate.

</details>

<details><summary>Column audit</summary>

Frame: rebuilt from the definition, 1,429,591 rows x 28 columns (26 features, the group column WELL, the
target). Prediction point (first `curation_comments` bullet): a well has been drilled and logged,
and a geologist interprets its lithology from the wireline logs, the NPD lithostratigraphy and the well position.
Codebook: there is no formal data dictionary. Meanings come from the curve mnemonics (LAS conventions), the starter
notebook, as the definition quotes it, and the Zenodo description. Units
are not stated anywhere in the competition files.

**Column table**

| column | meaning | known at prediction? | dtype and cleaning | verdict | rule |
|---|---|---|---|---|---|
| WELL | wellbore name (NPD) | yes | category, 118 levels; the group column and not a feature (`report.py`: "the target and the group columns are not features") | fine | LEAK-33 holds, SPLIT-29 |
| DEPTH_MD | measured depth along the hole, m | yes | float; 136-5,437 m; no gaps or sentinels | fine | |
| X_LOC, Y_LOC | well position (UTM easting / northing, m) | yes | float; 0.8% missing in 18 wells. In 16/11-1 ST3, the lower half (1,833-2,953 m, 7,374 rows) has no position, and this holds 4,294 of the 14,711 Halite rows. Missing X_LOC therefore means 39.6% Halite, against 1.0% overall. This is a recording artefact, not missingness the outcome causes. Under grouped folds no other well repeats it, so a test fold cannot profit from it | fine, note | LEAK-10 not triggered; probe 3 did not flag it |
| Z_LOC | true vertical depth below sea level, m (negative) | yes | float; -5,396 to -111. The LAS-null mask is (correctly) not applied, because about 1.29M rows lie legitimately below -900 m | fine | CLEAN-10 n/a |
| GROUP | NPD lithostratigraphic group pick | **open**: see problem 1 | category, 14 levels, 0.09% missing | question for the curator | LEAK-10 / USE-3, USE-8 |
| FORMATION | NPD lithostratigraphic formation or member pick | **open**: see problem 1 | category, 69 levels, 10.7% missing. Three units appear under two codes, never in the same well: Grid Fm. (15 wells) / Grid Mb. (2), Skade Fm. (20) / Skade Mb. (4), Ty Fm. (13) / Ty Mb. (2). The codes come from older and newer NPD nomenclature. Four names state a lithology ("Intra ... Fm. Sst.", "Ran Sst Mb."; 0.66% of the rows, 11-66% Sandstone). BASEMENT has 143 rows, all labelled Shale | question (problem 1), cleaning note (problem 6) | LEAK-10; CLEAN-12 / CLEAN-14 (one meaning, one code) |
| CALI | caliper, hole diameter, in | yes | float; 2.3-28.3 | fine | |
| RSHA, RMED, RDEP | shallow / medium / deep resistivity, ohm.m | yes | float. Tool-saturation values stay (RSHA 2000: 345 rows, RMED 1950: 756), which is correct because they are real capped readings. RMED has 7 negative rows, which is impossible | fine, plus impossible negatives (problem 5) | CLEAN-11 |
| RHOB | bulk density, g/cm3 | yes | float; 0.72-3.46, per-well medians 2.04-2.65 | fine | |
| GR | gamma ray, API | yes | float; 0.1-1,141, 5 rows above 1,000 (spikes, kept on purpose) | fine | CLEAN-11 (unusual, keep) |
| SGR | spectral gamma ray, API | yes | float; 95% missing (14 wells). **Two wells are on a different scale**: 34/12-1 (median 0.012) and 35/11-15 S (0.020), 8,731 rows, against 46-106 elsewhere. There are also 39 negative rows (down to -778) | cleaning problem | CLEAN-21, CLEAN-11 |
| NPHI | neutron porosity, v/v | yes | float; -0.036 to 1.0. Small negatives are physically possible (salt, anhydrite) | fine | |
| PEF | photoelectric factor, b/e | yes | float; 2,176 rows above 100 (barite-mud effect or spikes), kept under the "spikes stay" note | fine | |
| DTC | compressional slowness, us/ft | yes | float; per-well medians 67-148 | fine | |
| SP | spontaneous potential, mV (per-well baseline) | yes | float; -999.0 masked (402 rows), negatives are real | fine | CLEAN-10 applied |
| BS | bit size, in | yes (planned before drilling) | float. float32 noise splits single values (26.000001907 / 25.999998093, 9.87 / 9.875), which is harmless for trees | fine | |
| ROP | rate of penetration while drilling | yes (recorded while drilling) | float. **25/6-2 has a per-well median of 17,778** (2,925 rows, up to 47,015), against 0.6-150 in the other wells. 30/6-5 has a median of 365. There are also 52 negative rows | cleaning problem | CLEAN-21, CLEAN-11 |
| DTS | shear slowness, us/ft | yes | float; per-well medians 134-373 | fine | |
| DCAL | differential caliper (CALI - BS within 0.01 on 89% of the rows) | yes | float. A partial derivative of two columns, not an exact copy, so it stays. One impossible value of 10,006.8, and 2 rows above 100 | fine, plus impossible value (problem 5) | CLEAN-5 n/a, CLEAN-11 |
| DRHO | density correction, g/cm3 (normally about ±0.2) | yes | float. **In 36/7-3, DRHO equals RHOB on 100% of its 3,474 rows. In 31/4-10, it holds a density curve** (median 2.38, 2,208 rows). Both are mislabelled curves, impossible as a correction. One more row reads -7,429.3 | cleaning problem | CLEAN-11 (CLEAN-1) |
| MUDWEIGHT | drilling-mud density | yes (drilling data) | float; three scales, per-well medians 0.13-0.17 (19 wells), 1.08-1.80 (9) and 155.8 (16/10-2, 1,275 rows). Kept with an anomaly note. The 0.13-0.17 group fits bar/m (sg x 0.0981 gives sg 1.35-1.77, the range of the sg wells), but no header confirms it | cleaning problem, documented; question on the conversion | CLEAN-21, PROV-13 |
| RMIC | micro-resistivity, ohm.m | yes | float; 2000 (134 rows) and 10,000 (3 rows) are tool caps or saturation | fine | |
| ROPA | average rate of penetration | yes | float. -999.25 masked. 2 rows remain at -965.9 / -948.9. 34/4-10 R has a median of 0.099 against 10-82 elsewhere | cleaning problem (minor) | CLEAN-10, CLEAN-21 |
| RXO | flushed-zone resistivity, ohm.m | yes | float. -999.9 and -999.0 masked (34,483 rows). 2 rows remain at -995.9 / -968.1, plus 131 negative rows | cleaning problem (minor) | CLEAN-10, CLEAN-11 |
| lithology (target) | hand-interpreted lithology, 11 classes | target | category. Mapped from the starter notebook's codes; Basement dropped (103 rows, one well); no missing values (asserted) | fine | CLEAN-15, CLEAN-17 (TP-8 departure documented) |
| dropped: FORCE_2020_LITHOFACIES_CONFIDENCE | the interpreter's confidence in the label | no (recorded with the label) | dropped | correct drop | LEAK-10 |

There are no untyped object columns (CLEAN-9). The framework shuffles the rows (seed 42; the checklist's row-order
check passed, CLEAN-23). No feature is computed over all rows (CLEAN-7): `_clean` only stacks, drops, maps and masks.

**Problems, ranked (principles.md: P4 before P7, Must before Should, then effect size)**

1. **P4, GROUP and FORMATION: the timing is not settled, and the fit says direct (question for the curator; LEAK-10
   "another encoding of the target", USE-3, USE-8).**
   - What they are: lithostratigraphic units, and these are defined by their lithology. A Zechstein pick means
     evaporites: 14,709 of 14,711 Halite rows are in it.
   - Where they come from: NPD makes its official picks after the well, from the composite log, which carries the
     cuttings description.
   - What the definition argues: `fit_reason` says the picks are not the FORCE interpreters' own. That is true and
     measured. It does not say they exist before the lithology interpretation.
   - Evidence: FORMATION alone has macro AUC 0.849 and GROUP 0.827 (leak probe). Without both, random-forest log loss
     goes from 0.776 to 0.836 (the earlier REVIEW.md). Only 10% of group boundaries fall on a lithology change, so they are
     not a copy of the label.
   - Case for keeping them: the competition gave them as inputs, and the operator's preliminary tops exist when the
     well is completed (LEAK-37 / USE-6, if the curator accepts that).
   - Mildest remedy: keep them with a `Potential leak, kept on purpose:` note on the timing, and set `fit` to
     approximate, as USE-8 lists "a potential leak kept on purpose". The alternative is a logs-only task. A strong
     leak is not shown, so retiring is not on the table.
2. **P7, DRHO holds another curve in two wells (CLEAN-11, Should).**
   - 36/7-3: DRHO equals RHOB on all 3,474 rows.
   - 31/4-10: DRHO is a bulk-density curve (median 2.38, 2,208 rows).
   - One more row reads -7,429.
   - Mildest remedy: mask DRHO where |DRHO| > 1 g/cm3. This catches both wells and the outlier, about 5.7k rows. Add
     a bullet.
3. **P7, curves on a second scale (CLEAN-21, Should).**
   - ROP: 25/6-2, median 17,778, 2,925 rows; 30/6-5 is borderline at a median of 365.
   - SGR: 34/12-1 and 35/11-15 S, medians around 0.01, 8,731 rows.
   - ROPA: 34/4-10 R, median 0.099.
   - MUDWEIGHT: the three scales the definition already documents.
   - None of the sources publishes a unit, so the mildest remedy is the definition's own approach for MUDWEIGHT: a
     note naming the wells and rows. Masking the off-scale wells per curve is the cheap alternative, and it is safe
     because it only removes values.
   - For MUDWEIGHT, check whether the 0.13-0.17 group is bar/m before converting it (PROV-13). Converting on a guess
     is not allowed (CLEAN-21 asks for a published conversion).
4. **P7, leftover sentinels (CLEAN-10, Should).** RXO -995.9 / -968.1 and ROPA -965.9 / -948.9 survive the
   ±0.01 match. Remedy: mask values below -900 in the log curves (not Z_LOC). Also correct the bullet "become missing in
   RXO, SP and ROPA": the code masks all 20 curves, but not these values.
5. **P7, impossible values (CLEAN-11, Should).** Negative readings: RXO 131 rows, ROP 52, SGR 39, RMED 7. DCAL has one
   value of 10,006.8. Remedy: mask the negative values of the resistivity, GR and ROP curves and DCAL > 100, or name
   them under the "spikes stay" note. This is a few hundred values in 1.43M rows.
6. **P7, duplicate formation codes (CLEAN-12 / CLEAN-14, Should; a question).** Grid, Skade and Ty each appear as
   both Fm. and Mb., never in the same well, with similar label mixes (Skade 86% / 85% Shale, Ty 77% / 75%
   Sandstone). A model sees two levels for one unit across wells. Remedy: map Mb. to Fm. for these three, after
   checking against the NPD nomenclature, or keep them with a note.
7. **Note only.** In 16/11-1 ST3, X_LOC, Y_LOC and Z_LOC are missing over its lower half, which holds 29% of all
   Halite rows. This is a recording artefact that grouped folds cannot exploit on a test well. Mention it in a bullet
   if problem 3's note is written.

</details>

<details><summary>Split audit</summary>

Verdict: **right with notes.** Grouped by wellbore (WELL, 118 groups), default 3-fold, 1 repeat, `labels="per_sample"`,
`prediction_unit="row"`, `context="all_rows"`. No repository file edited.

Data: the definition's frame and split plan rebuilt (1,429,591 rows, 28 columns). Model numbers: one random forest (150 trees, min_samples_leaf 5, sqrt features), every 10th depth
sample (1.5 m) of each side, WELL dropped, GROUP/FORMATION as codes; log loss and macro OVR AUC over the classes a test
fold holds, mean of 3 folds (EV-8).

**Regime (SPLIT-1, SPLIT-3, USE-10): holds**

* Use case: a geologist interprets the lithology of a newly drilled and logged well. The entity (the well) is new: a
  cold start, so grouped by well. Not a stream: the wells have no drill date in the data and the label is an
  interpretation of the logs, not an outcome over time; no temporal regime applies (SPLIT-3: one regime).
* Source: the organisers held out 10 open-test and 10 blind wells (blog p. 3); the grouped folds match that design.
* Group id (SPLIT-24, SPLIT-26): WELL is the source's own wellbore name, a true id, not a cluster or hash. Only one
  well has two wellbores in the data (34/5-1 A and S); they share no depth sample, 1.33 km apart at their median
  positions (closest pair of all 118). Grouping on the wellbore, as the source does, is fine. Putting both in one group
  would cost nothing; optional.
* Prediction unit (SPLIT-23): each depth sample scored, as in the competition. Right.
* Context `all_rows`: the whole log of a well exists before its interpretation (starter notebook quote); right.
  The harness drops WELL as a feature (LEAK-33 / definitions.md); window features then need WELL and DEPTH_MD in the
  harness, a harness item, not a split fault.

**Shipped folds**

| fold | train rows | test rows | test wells | wells on both sides | Halite test wells | Anhydrite test wells |
|---|---|---|---|---|---|---|
| r0f0 | 973,462 | 456,129 | 37 | 0 | 1 | 6 |
| r0f1 | 954,627 | 474,964 | 40 | 0 | 3 | 4 |
| r0f2 | 931,093 | 498,498 | 41 | 0 | 0 | 0 |

Within the 1M / 500k caps. Class mix per test fold otherwise close (Shale 59-63%, Sandstone 14-15%).

**Alternative splits (same model)**

| split | log loss (per fold) | macro AUC |
|---|---|---|
| shipped, well-grouped | 0.763 (0.773, 0.786, 0.731) | 0.912 |
| well-grouped, another random assignment | 0.759 (0.806, 0.714, 0.758) | 0.920 |
| row-random 3-fold (IID) | 0.315 (0.313, 0.316, 0.316) | 0.987 |
| grouped by licence block (54 blocks) | 0.814 (0.856, 0.848, 0.736) | 0.905 |
| grouped by quadrant (14) | 1.015 (0.836, 1.331, 0.879) | 0.844 |

* IID would be badly wrong (SPLIT-29): neighbouring depths let a model recognise the well; 0.315 against 0.763
  reproduces the definition's 0.31 / 0.78.
* No near copies across wells: of 1,395,874 rows with at least 4 of 7 main logs, no rounded log vector is shared by two
  wells.
* The group probe ran on a 22-well, 204k-row subsample with ROC AUC, and its LightGBM
  diverged (0.582 across groups), so its numbers are no reference (EV-3); the forest above stands in.

**Problems, ranked (P4 first, then by strength and effect)**

1. **P4, SPLIT-1 / SPLIT-31 (weigh, no fix): the well-grouped test sits near training wells.** Median distance from a
   test well to its nearest training well 8.0-8.6 km (10% within 3.1-3.6 km); 55-76% of test wells have a training
   well in the same licence block, 95-100% in the same quadrant. Holding out whole blocks raises log loss 0.763 to
   0.814; whole quadrants to 1.015 (14 groups, partly a class-mix shift: the few-groups factor). This matches the
   source: 14 of the competition's 20 held-out wells (8 open, 6 blind) are in a block with a training well (70%, inside
   our 55-76%), and most new wells on the shelf are drilled near earlier ones. Keep the well split. Mildest remedy: a
   sentence in a `splits_comment` (or the `Grouping.definition`) that the test wells have drilled neighbours, so the
   score stands for wells in explored areas, not frontier wells; a block-grouped variant is a candidate, not a fix.
2. **P4 / P6, TP-5 and the accepted `splits_test_class_missing`: Halite rests on 4 wells.** Test folds hold 1, 3 and 0
   Halite wells (Anhydrite 6, 4, 0), and there is one repeat, so the Halite part of fold r0f0 is one well. Accepted
   in the definition with correct counts; another random well assignment changed the mean log loss by only 0.004.
   Mildest remedy: none needed; if the curator wants every fold to see the evaporites, assign the 10 evaporite wells
   to folds by hand (stratified group assignment).
3. **P4, SPLIT-19 (Should, departure documented): the competition's 98/10/10 split is replaced.** Reason given (the
   organisers found 10 blind wells too few) and the pooled folds keep the source's regime (whole wells held out, the
   same share of neighbours, see 1). Holds. Mildest remedy: state it in a `splits_comment`, since the definition has
   none and the default text says "Default splits." (definitions.md asks for a comment when the split deliberately
   differs from the source's protocol).
4. **Note: the group probe is not evidence here** (EV-3, EV-8): subsample of 22 wells, diverged LightGBM. Cite the
   forest numbers instead when the README reports the split gap.

Not triggered: SPLIT-9/10/14 (no temporal regime), SPLIT-24/25 (true id), SPLIT-28 (classification, real signal
across wells: macro AUC 0.91).

</details>

<details><summary>Domain practitioner</summary>

Reviewer role: a petrophysicist / well-correlation geologist on the Norwegian shelf who has to produce a lithology
column for wells (new wells after logging, and the backlog of released wells in Diskos for regional work).

**Fit**

**Direct (agree with the definition, USE-8).** One row is one depth of a well I have to interpret, every input is on my
desk once the well is logged, the label is the interpreted lithology column I would otherwise draw by hand, and whole
held-out wells are the wells I have not yet interpreted (USE-10 cold start, grouped split).

The most realistic use is the backlog of released wells (the organisers' labels were built for 118 released NCS wells
from logs, mud logs and completion logs), not only "a newly drilled well". Under USE-9 that use case fits the shipped
data at least as well and removes the timing question about the NPD tops (gap 3); the task_summary could say "a newly
drilled or a released well". This rephrasing is not done to excuse a gap; it is how the source data were assembled.

**1. Inputs at the prediction point (USE-3, USE-6)**

Have, and in the data: the wireline curves (GR, RHOB, NPHI, DTC, PEF, resistivities, CALI, ...), BS, ROP, MUDWEIGHT,
DEPTH_MD, X/Y/Z, and the formation and group tops. All known once the well is logged. Nothing recorded after the
interpretation; the dropped FORCE_2020_LITHOFACIES_CONFIDENCE is part of the label (correctly dropped).

Would not have / would not use:
- **WELL as a categorical feature.** For a new well it is an unseen level and carries nothing; a practitioner would not
  feed it. Harmless under the grouped split (no level is shared between train and test), so only a hygiene remark.
- **NPD's GROUP / FORMATION for a just-drilled well.** NPD publishes its lithostratigraphy after the well is reported;
  at the first interpretation I would have the operator's own tops (picked from the same logs plus biostratigraphy),
  which agree with NPD's for most wells. For released wells the NPD tops are exactly what I would use. Low impact.

Missing that I would always have:
- **The mud log / cuttings descriptions** and the operator's completion log. The labels themselves were drawn with them
  ("hand-crafted lithology interpretation using inhouse data, completion logs, mud logs", GeoExPro); one disputed label
  traces to "the wrong lithology symbol used on the mudlog". Every drilled well has a mud log, so the model sees less
  than the person who made the label. This is the main reason the reachable accuracy sits near 80% and why the
  thin carbonate stringers and evaporites are hard. It cannot be fixed from the competition files (the mud logs are
  scanned documents), so it is a stated gap, not a defect.
- **The rest of the well's log as a sequence.** No interpreter reads one 15 cm sample alone; I look at the curve shapes
  over metres (bed boundaries, coarsening-upward trends, a density spike for a calcite stringer). The definition allows
  it (`context="all_rows"`) but ships raw per-depth rows; a row-wise model never sees context. Measured in
  the earlier REVIEW.md: window features move RF log loss 0.776 -> 0.764 (small), so it changes the task less than I expected.
- **Offset-well interpretations.** I always have my neighbours' lithology columns; the pooled training wells stand in
  for that, which the grouped split preserves.

**2. Target (USE-5)**

The target is the interpreter's lithology at each sample: what I would act on (draw on the composite log, feed into
net-to-gross, sand counts, rock-physics templates). It is a proxy for true rock type, with known label noise
(organisers: ~80% reachable; 80-95% "solution" in the GeoExPro commentary), and 'Sandstone/Shale' is an interpretive
mixed class rather than a rock. I accept the human label as the target; the truth is not available anywhere.

Output: I want the class per depth for the log display and a probability per class for QC (flag the intervals where
the model is unsure for me to check). So the probabilistic scoring (log loss) fits my use better than the competition's
hard-label penalty matrix for model ranking, though the penalty matrix encodes the geological cost of confusing, say,
sandstone with shale versus sandstone with sandstone/shale.

**3. Row vs decision, test data (USE-10)**

One row = one depth sample: I decide a lithology per interval, and the samples are the resolution of that column, so
the match is close. The scoring weights each well by its length and each class by its thickness: shale is 61% of the
rows, so per-sample log loss is dominated by shale/sandstone, while my value lies in reservoir sands, coal, thin
carbonates and evaporites. This is a weighting choice, not a mismatch.

Test data: whole held-out wells drawn at random over the same quadrants (15-36/x and 7/x). New wells in a mature
basin usually lie near existing wells, so a random well split is what I would face; a spatially blocked split (a new
area) would be harder and is not the main use. The organisers' blind wells had a different lithology mix, which the
pooled 3-fold split averages out. Halite and Anhydrite missing from one test fold is real (four halite wells).

**4. Would I use it?**

Yes, as a first pass and QC tool: it gives an 80%-ish column in minutes for a backlog of hundreds of wells. I would
trust it on shale / sandstone / chalk and on Zechstein evaporites (GROUP pins them); I would distrust it on thin
limestone/dolomite stringers, coal, tuff, and wells with missing density/neutron curves (only GR is guaranteed), and on
wells with odd unit conventions (MUDWEIGHT). I would trust a model more if it showed per-class recall on whole new
wells and used curve context; I would distrust one that leans on WELL or on X/Y to memorise areas.

**Gaps between the dataset and the real decision, ranked by how much they change the task**

1. **The label was drawn with mud logs and in-house data the model does not get** (USE-5, USE-3). Caps accuracy and makes
   part of the label unexplainable; unfixable from these files; already summarised in the curation_comments as the
   ~80% anomaly. Worth naming in the fit_reason as the known gap of a direct fit.
2. **No depth context in the rows** (USE-3 / grouping context). Interpreters always use the curve sequence; measured
   gain small (0.776 -> 0.764). Leaving windows to the pipeline is defensible.
3. **NPD tops vs operator tops at first interpretation** (USE-3, USE-6). Disappears under the released-well use case
   (USE-9); low impact either way.
4. **Per-sample log loss vs the geological cost of confusions** (USE-5). Ranking choice; the penalty matrix is in the
   source if a custom metric is wanted.
5. **WELL as a feature** and **MUDWEIGHT on three scales**: hygiene, not use case.

**What a domain expert would change**

- Say in the use case "a newly drilled or a released well" (USE-9): the backlog of released wells is the larger real
  use and matches NPD tops as inputs.
- Name the missing mud-log/cuttings input as the known gap in `fit_reason` (keep fit direct; the inputs a model can
  get are all there).
- MUDWEIGHT: the 19 wells with medians 0.13-0.17 are consistent with bar/m (1.3-1.7 s.g. equivalent), the 9 wells at
  1.08-1.80 with g/cm3 (s.g.); converting the bar/m group (x 10.2) would be a well-founded unit fix, not a guess. The
  one well at 156 has no obvious unit and could be set missing. Low priority: MUDWEIGHT is in 29 wells and is a weak
  lithology signal.
- Domain: "earth science / geoscience" rather than "chemistry & material science" if the vocabulary allows; of the
  listed alternatives, "environmental science & climate" is closer.
- Optional: keep the interpreter confidence out of the features but consider it for evaluation weighting (not needed).

**Sources**

- Definition and record: datasets/_dev/tabarena-v0pt2/force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition/dataset.py,
  curation/records/force_2020_well_well_log_and_lithofacies_dataset_for_machine_learning_competition.md
- Rules: .claude/skills/knowledge-curation/references/use_case.md (USE-3, USE-5, USE-6, USE-8, USE-9, USE-10)
- https://github.com/bolgebrygg/Force-2020-Machine-Learning-competition (inputs: logs, NPD lithostratigraphy, X/Y;
  penalty-matrix scoring)
- https://geoexpro.com/and-the-winner-is-the-human-with-the-machine/ (labels from in-house data, completion logs, mud
  logs; mud-log symbol error; 80-95% solution; label disputes)
- https://www.sodir.no/force/Previous-events/2020/results-of-the-FORCE-2020-lithology-competition/ (blind set had a
  different lithology distribution)
- https://zenodo.org/records/4351156

</details>

<details><summary>Blind review</summary>

**Verdict**
Include, with small changes. It is a real, well-known, openly licensed (CC BY 4.0) task. The split by well matches how the model would be used. There is clear but not trivial signal, and the shift between wells makes it a useful hard case.

**Task and use**
A petrophysicist or geologist interprets the lithology (rock type) of each depth sample in a newly drilled well from its wireline logs. This normally takes skilled people time. An ML model gives a first-pass interpretation that experts then review. The FORCE 2020 competition was built for exactly this use. The labels are "hand crafted using skilled geoscientists" (Zenodo 4351156), so they are expert interpretations, not ground truth from cores.

**What I checked**
- 200k-row sample: 118 wells, which is all 118 in the Zenodo release (train, open test and blind test combined). There are 27 features and 11 classes.
- Class counts in the sample: Shale 61.3%, Sandstone 14.5%, Sandstone/Shale 12.7%, Limestone 4.9%, Marl 2.8%, Tuff 1.2%, Halite 1.0%, Chalk 0.9%, Coal 0.3%, Dolomite 0.16%, Anhydrite 0.13%.
- No duplicate feature rows. The coordinates are almost constant within each well (mean within-well std is about 30 m), so they act as a well location.
- LightGBM with GroupKFold(3) by WELL (my own folds, not the task's folds):
  - Majority-class baseline: accuracy 0.613.
  - Regularized LightGBM (15 leaves, min_child_samples 200, subsampling), all features: accuracy 0.758 (0.750 / 0.767 / 0.758 per fold), macro-F1 0.486, log loss 0.72.
  - Same without X_LOC / Y_LOC: accuracy 0.747. Without the locations and without GROUP / FORMATION: 0.733.
  - GROUP + FORMATION + depth + location only: accuracy 0.44. So these columns do not carry the target on their own.
  - A less regularized LightGBM (63 leaves, 300 trees): accuracy 0.633, log loss 3.48. It overfits badly to the training wells. The scores depend strongly on how well a method handles the shift between wells, which is good for a benchmark.
- My scores are below the competition winners (about 0.80 accuracy), who used feature engineering and context along the well. That is plausible.

**Concerns (most to least serious)**

1. **GROUP and FORMATION are interpretations, partly based on lithology.** Formation tops are picked by geologists, often from the same logs and at the same stage as the lithology interpretation. Several formations are defined by their lithology (for example Utsira Fm. is sand, Ekofisk Fm. is chalk). The competition gave these columns for its test wells too, so including them is faithful to the source. They are only a moderate help (+1.3 accuracy points in my test), and on their own they score below the majority baseline. FORMATION is missing in 10.7% of rows.
   Change: keep both, but document that they are interpreted stratigraphy that is available at prediction time only if formation tops have already been picked. Optionally offer a variant without them. Not a blocker.

2. **Rows inside a well are strongly autocorrelated, and the context along the well is lost.** Samples are about 0.15 m apart. The grouped split by WELL correctly stops neighbouring depth samples from leaking across train and test, which is the most important thing here. But treating each row as independent drops the neighbouring-depth context that practitioners use (for example rolling-window features). As a per-row tabular benchmark this is acceptable. The effective sample size is closer to 118 wells than to 1.4M rows, so 3 folds over about 118 wells will give somewhat noisy scores.
   Change: none required. More repeats of the grouped split would help if the budget allows.

3. **The evaluation metric differs from the source.** The competition scored with a custom penalty matrix between geologically similar classes (I did not open the scoring file). A benchmark using log loss or accuracy is fine, but the class imbalance is heavy: 61% Shale, and the rarest classes are about 0.15%. Halite appears in only 4 of 118 wells and Anhydrite in 9, so some test folds may hold very few wells with these classes.
   Change: check that every class appears in every training fold. Use a metric that is robust to rare classes in held-out groups.

4. **Classes and columns may have been dropped.** The source label set has 12 classes, including Basement. The sample has 11. Basement is very rare and was likely dropped or simply not sampled; I could not confirm which. The FORCE_2020_LITHOFACIES_CONFIDENCE column is absent, which is correct, because it is a label-quality column. Having no lithology-code column is also correct.
   Change: state in the README how Basement and the confidence column were handled.

5. **Values have outliers and are heavily missing.** Logs were only "partially despiked" (Zenodo). Examples: ROP up to 43,065, RMIC up to 9,925, MUDWEIGHT up to 427, PEF up to 374. Several columns are mostly missing: SGR 95%, RMIC 86%, DTS 80%, ROPA 78%, RXO 77%, MUDWEIGHT 77%, DCAL 75%. Which logs were run varies by well and vintage. This is realistic and should be kept as NaN; no change needed. ROP, ROPA and MUDWEIGHT are drilling parameters, which are known while drilling, so they are fine.

6. **Data types.** WELL is a category column and must be used only as the group, never as a feature. Worth confirming that the pipeline drops it from the features; a category with 118 levels and no overlap between train and test would be useless anyway. GROUP has 14 levels and FORMATION 70, both categorical, which is sensible.

**What I could not check**
- The full 1.43M rows and the task's own fold assignment; I only had the 200k sample and used my own GroupKFold.
- Whether Basement was dropped on purpose.
- The exact competition penalty matrix and the derivation of GROUP / FORMATION. The Zenodo page does not define them, though it ships NPD lithostratigraphy sheets.
- Whether the 118 wells include the hidden-test wells with their released labels. The count suggests yes.

</details>

<details><summary>Precedent check</summary>

Consistency check (AI, 2026-10-20), review panel. K = `.claude/skills/knowledge-curation/references/`, W =
`datasets/_dev/tabarena-v0pt2/`. "Issue N" means the earlier REVIEW.md's numbering, kept in this file.

**Summary**

| # | Decision | Rule(s) | Verdict |
|---|---|---|---|
| 1 | Grouped by WELL, `labels="per_sample"`, `prediction_unit="row"` | SPLIT-1, SPLIT-23, SPLIT-29 | consistent |
| 2 | Pool all 118 wells, replace the 98/10/10 competition split | SPLIT-19 (Should), SPLIT-5 | departs with a stated reason |
| 3 | 34/5-1 A and S stay two groups | SPLIT-24, SPLIT-26 | consistent |
| 4 | `context="all_rows"`, no depth-window features built (issue 1) | CLEAN-2, CLEAN-19, USE-3 | consistent (electric_motor set apart) |
| 5 | GROUP and FORMATION kept as features, `fit="direct"` (issue 2) | LEAK-10, USE-3, USE-6, USE-8, LEAK-38 | consistent on the facts stated; open fact; a fit/note mismatch against kick if the fact stays open |
| 6 | FORCE_2020_LITHOFACIES_CONFIDENCE dropped | LEAK-10 | consistent |
| 7 | Basement class dropped (one well) | CLEAN-17 (Should), TP-5, TP-7, LEAK-4 | departs with a stated reason (reasonable) |
| 8 | LAS nulls masked; sentinel remnants and impossible negatives left | CLEAN-10, CLEAN-11 (Should) | departs without a reason |
| 9 | MUDWEIGHT left on three scales | CLEAN-21 (Should), PROV-13 | departs with a stated reason; the closest precedent took another remedy |
| 10 | Log loss, not the competition's penalty matrix (issue 4) | TP-6 (Must) against definitions.md "Field mapping" | follows the house rule, departs from TP-6's wording without a reason; rule-level contradiction |
| 11 | `splits_test_class_missing` accepted; CC 2026-10-12 keep on `few_minority` | TP-8, TP-5 | consistent (register flag 1 is not a real pair) |
| 12 | `no_spread` read as LightGBM divergence (issue 3) | TP-1, TP-3, SPLIT-27 | consistent |
| 13 | Domain "chemistry & material science" | metadata (Weigh) | departs from sibling labels; imported value, not a curator decision |
| 14 | Record: AI assessment 2026-10-20 "no known risk", priority 5 | records/priority | inconsistent with the open issues; AI-only |

No drift (the curator's decisions on this dataset are one CC line, 2026-10-12) and no third exception of one kind is
reached yet; decision 5 would be the third if recorded as "kept because the host gave it" (see there).

**Per decision**

**1. Grouped split by well (SPLIT-1, SPLIT-23, SPLIT-29) - consistent**

Follows superconductivity (SPLIT-4, 2026-10-06: new entities must be new in test) and the source's own protocol (whole
wells held out, blog p. 3). Group probe: IID 0.841 against grouped 0.639 macro AUC, the
SPLIT-29 reading. `labels="per_sample"` with `prediction_unit="row"` matches micro_mass (`W/micro_mass/dataset.py`,
one prediction per spectrum within held-out strains).

**2. Pooling the 118 wells (SPLIT-19 Should, SPLIT-5) - departs with a stated reason**

SPLIT-19 says follow a split the source defines; SPLIT-5 says the source's split is a claim to check. The definition
names the fact: the organisers themselves found 10 blind wells too few to represent the lithologies, and the default
grouped 3-fold protocol tests 37-41 wells per fold. That serves P4 (an honest test) and P6 (scorable folds). SPLIT-19
sits under "The training history" (temporal), so its reach for a grouped task is itself loose. Reasonable; no prompt.
If the curator wants it on file, it is an exception to SPLIT-19 with that fact.

**3. Two wellbores of 34/5-1 as two groups (SPLIT-24, SPLIT-26) - consistent**

SPLIT-26: the group key from the source's own data at the resolution the features see (superconductivity, 2026-10-06).
The wellbores share no depth sample and lie 1.1-1.9 km apart where depths overlap (not re-measured, checklist P4 row).
Consistent; the checklist's open verification is a fact check, not a consistency point.

**4. `context="all_rows"`, no window features (issue 1) - consistent**

Closest precedents:

* open_university_learning_analytics_dataset (`W/open_university_learning_analytics_dataset/dataset.py`, Grouping):
  `context="all_rows"` because all rows of the running presentation are known, and no cohort features built. Same
  pattern as force: declare the context, leave the features to the pipeline (CLEAN-2).
* amex_non_iid_1m (`W/amex_non_iid_1m/dataset.py`): `all_rows`, all statements past at prediction time.
* electric_motor_temperature_prediction (`W/electric_motor_temperature_prediction/dataset.py`): `context="none"` and
  EWMA/EWMS features built in `_clean`. What sets it apart: a real-time estimate where only the past exists (the row
  alone cannot carry the thermal state), and the features are the data publishers' own (Kirchgässner et al.), so CLEAN-19
  bullet 3 ("the raw data cannot be used as it is") applies. In force the raw per-depth rows are usable (RF log loss
  0.776; windows 0.764, better on 2 of 3 folds) and the windows are the winners' choice, not the source's.
* alfa_battle_2_0_task_2 (CLEAN-19, 2026-10-13, Lennart): top-solution features adopted because the data is a
  transaction log that must be aggregated. Not the force situation.

So shipping raw rows is like open_university and unlike electric_motor for a stated reason. The alternative
`context="none"` (the earlier REVIEW.md issue 1) would contradict the definition's own use case (the whole log exists before
interpretation, USE-3); the precedents do not favour it. No prompt; the curator's call on issue 1 is a weighing one.

**5. GROUP and FORMATION as features, `fit="direct"` (issue 2) - consistent on the stated facts; one open fact**

Precedents that bear on it:

* sdss_17 (LEAK-10 Mechanisms row "Fitted from the same measurement that gives the label"; CHANGELOG): `redshift`
  dropped. Set apart: there the measurement (the spectrum) is not an input of the photometric task and the redshift is
  fitted together with the class. Here the logs are themselves inputs, the picks are NPD's not the label interpreters'
  (Interpreter NPD on every top), and only 10% of 574 group boundaries fall on a lithology change. The definition states
  these facts.
* eryhemato_squamous_disease (USE-4, TP-6; K/use_case.md Cases): features from a later stage are dropped. Whether NPD's
  picks exist when a new well's lithology is interpreted is exactly the fact that would put force on the eryhemato side.
  The definition asserts they are known ("Every feature is known then"); the checklist says no probe or page settles it
  (EV-2).
* brazilian_ecommerce (USE-6, 2026-10-15): an input fixed before the outcome stays. Applies if the picks precede the
  interpretation.
* kick and homesite (LEAK-38, USE-8 Cases "kick: approximate: a potential leak kept on purpose"): host-designed fields
  of uncertain timing stay with a `Potential leak, kept on purpose:` note and the fit becomes approximate.

Finding: the keep follows the stated facts. But the reason the definition gives first is "the competition gave them as
features" (SPLIT-5 logic: a source's framing is a claim to check). If the timing stays unsettled, the kick precedent
says the fit is `approximate` with a kept-on-purpose note, while force ships `fit="direct"` with no such note. That is a
real pair decided differently only if the fact stays open. Third-exception watch: homesite and kick were kept because
the host designed the fields; recording force's keep on "the host gave them" would be the third keep on that reason,
and LEAK-38 covers only anonymised fields, so it would need an amendment to reach named fields.

**Consistency check (AI, 2026-10-20):** the keep of GROUP and FORMATION with `fit="direct"` (USE-8) differs from kick
(USE-8 approximate, a potential leak kept on purpose with a note), whose kept fields also have an unverified timing and
were kept because the host designed them. What sets force apart?
(a) NPD publishes formation tops while or right after a well is drilled, before the detailed lithology interpretation,
so they are known at the prediction point (USE-6, like brazilian_ecommerce's promised date); recorded as the fact behind
`direct`; (b) treat force like kick: keep them with a `Potential leak, kept on purpose:` note and `fit="approximate"`;
(c) treat force like eryhemato: drop them and ship a logs-only task (RF log loss 0.776 -> 0.836); (d) amend LEAK-38 to
cover named host-given fields of uncertain timing.

**6. Label confidence dropped (LEAK-10) - consistent**

A value recorded with the label, as sdss_17's redshift (fitted with the class) and qsar_bioconcentration's measured BCF
the class is read from (`W/qsar_bioconcentration/dataset.py`). Also absent for the open-test wells. Consistent.

**7. Basement dropped (CLEAN-17 Should; TP-5, TP-7, LEAK-4) - departs with a stated reason**

CLEAN-17 keeps rare classes of the source's labels. The stated fact: all 103 rows are in one well (16/4-1), so no grouped split can train and test it; in the TP-5 unit count that is one unit in
total. Serves P4/P6 (every fold scorable). Precedents of dropping a class: biogeographical_ancestry_prediction (LEAK-14,
an assay artefact), hepatitis_c (LEAK-13), lung_cancer (6 samples, an older drop that TP-8 would now question). None
dropped a class for living in one group, so force is the first case of this kind; reasonable. Small gap: TP-7/LEAK-4
ask to run the probes on the source's labels too when a class is dropped; 103 of 1.43M rows makes that immaterial, but
the notes do not say it was considered. No prompt; worth a Cases row under CLEAN-17 or TP-5 if the curator confirms.

**8. Sentinel remnants and impossible negatives (CLEAN-10, CLEAN-11 Should) - departs without a reason**

After cleaning: DRHO -7429.34 (1 row), RXO -995.86 and -968.05, ROPA -965.88 and
-948.95 (sentinel-like, 3 wells); RXO 131, ROP 52, SGR 39 (down to -777.99), RMED 7 negative rows (impossible for
resistivity, gamma ray, penetration rate). Negative SP, DCAL, DRHO in their normal range and NPHI to -0.036 are
physically possible and are not counted. The definition's bullet says "-999.0, -999.25 and -999.9 become missing" and
"spikes stay"; it does not address these values. Precedents under CLEAN-11 (K/cleaning_features.md Cases): sdss_17
`-9999` -> missing; heart_disease_va_long_beach `chol == 0` -> missing; churn_telco_south_asia negative network age ->
missing; thyroid_discordant `age = 455` -> missing. All took the mild fix. A few hundred values in 1.43M rows: a P7
quality point, cheap and safe to fix.

**Consistency check (AI, 2026-10-20):** leaving DRHO -7429, RXO/ROPA values near -950 to -996 and negative
resistivity, gamma-ray and ROP readings (CLEAN-10, CLEAN-11) differs from sdss_17, heart_disease_va_long_beach and
churn_telco_south_asia, where impossible values became missing. What sets force apart?
(a) they are interpolation smears of the LAS null and despiking leftovers, covered by the source's "partially despiked"
note, so they stay as published; recorded as an exception with that fact; (b) treat force like the precedents: mask
values below -900 in every log and negatives in RSHA/RMED/RDEP/RXO/RMIC/GR/SGR/ROP/ROPA, with a bullet; (c) reopen the
precedents (no); (d) amend CLEAN-11 so a source's "spikes kept" note covers impossible values.

**9. MUDWEIGHT on three scales (CLEAN-21 Should, PROV-13) - departs with a stated reason; precedent chose another remedy**

The definition's reason: no unit in any LAS header, so a conversion would rest on guessed units. Closest precedent:
college_scorecard (CLEAN-21, 2026-10-16, Lennart; `W/college_scorecard/dataset.py`): converted with the measuring
body's published table, and "a section without a conversion table stays dropped". Force has no table and keeps the
column as it is, the opposite remedy. Facts that may set force apart: the scale is constant within a well, and the
grouped split puts wells of each scale on both sides, while in college_scorecard the break is in time, so new rows sat
on the other scale; and 89 of 118 wells have no MUDWEIGHT at all. The checklist also notes the "no unit in any LAS
header" claim was not re-read (PROV-13 step). The medians 0.13-0.17 match bar/m for 1.3-1.8 g/cm3 mud, which would make
two of the scales convertible; that is an inference (EV-2 last rank), not a published conversion.

**Consistency check (AI, 2026-10-20):** keeping MUDWEIGHT on three scales (CLEAN-21) differs from college_scorecard
(2026-10-16), where a column without a published conversion was dropped. What sets force apart?
(a) the scale is constant per well and both sides of every grouped fold hold wells of each scale, so a model sees each
scale in training, unlike a scale break in time; recorded as an exception to CLEAN-21 with that fact; (b) treat force
like college_scorecard: drop MUDWEIGHT (29 of 118 wells carry it); (c) reopen college_scorecard to keep its unconverted
section; (d) amend CLEAN-21 to say when an unconvertible column stays.

**10. Log loss rather than the penalty matrix (issue 4; TP-6 Must vs definitions.md) - rule-level contradiction**

The definition follows `.claude/skills/knowledge-data-foundry/references/definitions.md` ("A competition with its own
metric keeps our default, and the notes name the original metric"), and names the original metric. TP-6 (Must), added
in the same commit (58ee235, 2026-10-20), lists "the scoring it uses" among the source-defined versions that replace
ours. The two texts contradict each other; per principles.md a precedent or rule that contradicts a rule is flagged,
not followed.

Precedents:
* Default kept, original named: african_credit_scoring_challenge (F1 on hard labels -> ROC AUC; definition only, no
  curator line found), zillow_prize (MAE -> RMSE, open issue 1 of its REVIEW.md, undecided), nyc_taxi (RMSLE = RMSE on
  log1p; not a departure).
* Competition metric used: amex_non_iid_1m (`amex_metric`), allstate_claims_severity (`mae`), porto_seguro (gini),
  5g_energy_consumption (`mape`), sepsis_prediction_1m (utility; LEAK-9 asks for a scorer fix). These are migrated
  definitions; no dated curator decision found for them.

So neither side has a dated curator precedent. Force is closest to african_credit: a hard-label competition score
(argmax plus a cost matrix), which a probability metric cannot reproduce. The definition does not give that reason.

**Consistency check (AI, 2026-10-20):** scoring log loss rather than the FORCE penalty matrix departs from TP-6's "the
scoring it uses", while amex, allstate, porto, 5g and sepsis ship their competitions' metrics. What sets force apart?
(a) the penalty matrix scores hard labels and none of the top three trained on it, so it is a metric quirk rather than a
better version of the task; recorded as an exception to TP-6 (and the same note for african_credit_scoring_challenge);
(b) treat force like amex: register an expected-penalty metric (11 x 11); (c) reopen the five definitions with custom
metrics to the default; (d) amend TP-6 or definitions.md so the two texts agree (which one wins for metrics).

**11. `splits_test_class_missing` accepted; CC 2026-10-12 keep (TP-8, TP-5) - consistent**

The register's flag 1 (opposite outcomes on `few_minority`) pairs force with alvin_smart_money_management (retired
`Too Small`, 2026-10-12, Lennart). Not a real pair: alvin's rarest classes are 8 rows carrying 51-54% of a window's log
loss; force's are 14,711 and 1,807 rows that a grouped split leaves out of one fold (fold r0f2). TP-8 now names force
as its own example, and micro_mass / asp_potassco (2026-10-12, uneven grouped folds, kept) are the like cases. The CC
line and `accepted_check_warnings` agree (same fold, same counts). Force is the only definition accepting this slug.

**12. `no_spread` as LightGBM divergence (issue 3; TP-1, TP-3, SPLIT-27) - consistent**

Follows mice_protein (SPLIT-27: untuned LightGBM 2.53 against a 2.07 baseline, RF 1.12) and TP-8 Cases row for force
(2026-10-12). TP-1 asks for a check against tuned methods; none exist in the cache (checklist). Writing point, not a
consistency one: the bullet's numbers (linear 0.989, gap 0.19, LightGBM 2.77) are stale against today's probes (0.880,
0.107, 2.678), EV-8.

**13. Domain (metadata, Weigh) - inconsistent with siblings; imported value**

"chemistry & material science" holds molecules and materials (qsar_*, melting_point, musk, forensic_glass, clock_protein).
Geoscience siblings use "environmental science & climate" (covertype, forest_fires); an oil-and-gas record uses
"industry & manufacturing" (pipeline_dataset_in_oil_and_gas_sector_fertilizer). The force value is imported, not a CC
decision, so no prompt; the like-cases reading points to "environmental science & climate" (the earlier REVIEW.md issue 7's
alternative).

**14. Record assessment 2026-10-20 (AI) - inconsistent with the open issues**

"no known risk" and priority 5 while the earlier REVIEW.md lists issues 1-4 (GROUP/FORMATION is a P4 question). AI-only, not a
curator decision; the next assessment should name issue 2 as a risk.

</details>

<details><summary>Advocate</summary>

Position: ship, after small definition and wording changes. No finding of phase A needs a remedy above "fix the
definition" on the ladder, and none is a Must that fails.

**1. A real task with the split its use case needs (P3, P4: USE-1, USE-8, SPLIT-1, SPLIT-29; Must)**

* Evidence: the source's task is exactly this ("predict lithology labels for provided well logs, provided NPD
  lithostratigraphy and well X, Y position", GitHub readme; claim audit 16). The organisers held out whole wells
  (blog p. 3); the definition holds out whole wells, 37/40/41 per fold, no well on both sides (split audit).
* Row-random would be badly wrong: RF log loss 0.315 IID against 0.763 grouped (split audit), reproducing the
  definition's 0.31/0.78. No shared log vector across wells; the one two-wellbore parent (34/5-1) sits in one fold.
* The practitioner (a Norwegian-shelf petrophysicist) calls the fit direct; the blind reviewer says "include" and that
  the split "matches how the model would be used". Three independent agents agree on the core.
* Answers: the spatial-neighbour point (split audit 1). It is a Weigh with no fix; 70% of the source's own held-out
  wells share a block with a training well, and new wells on the shelf are drilled near old ones (practitioner). The
  mildest remedy is a `splits_comment` sentence ("test wells have drilled neighbours"), which also covers SPLIT-19's
  ask to document the departure from 98/10/10 (organisers: "we should have chosen a larger blind dataset").

**2. GROUP and FORMATION: keep them; at worst a note and a fit label, never retirement (P4: LEAK-10 graded, USE-12 Must, USE-6, USE-9; TP-6)**

* Concede: the definition's "only 10% of the 574 group boundaries fall on a lithology change" reads as weak alignment;
  the base rate is 2.5%, so boundaries are 4x enriched (66% within 0.76 m vs 23%; claim audit 33). The sentence must
  be reworded with the enrichment and the shared source material.
* But it is not "another encoding of the target": GROUP + FORMATION + depth + location alone give accuracy 0.44,
  below the majority baseline 0.613 (blind review); dropping both moves RF log loss only 0.764 -> 0.809 (claim audit).
  Every top has Interpreter NPD (855/855, 1914/1914), not the FORCE label makers. Neither audit shows a strong leak;
  the column audit says "retiring is not on the table". LEAK-10 is a Must only when strong; USE-12 (Must) says a
  leak is no reason to reject a real task.
* Timing: USE-9 (Should, narrows USE-8) asks for the use case the data mirrors. The labels were built for 118
  released wells, and the practitioner names the backlog of released wells as "the larger real use", where "the NPD
  tops are exactly what I would use". Under that use case the tops are known and the fit stays direct, without any
  rephrasing to excuse a gap (the source assembled the data that way).
* Dropping them would remove what the source's task defines as an input (TP-6 Must, USE-4: the source's version wins
  over one of our invention).
* Mildest remedy: reword the note and the use case to "a newly drilled or a released well". If the curator doubts the
  timing for new wells, the kick precedent's remedy (`fit="approximate"` plus `Potential leak, kept on purpose:`) is
  the next rung, still a ship.

**3. Worth benchmarking (P6: TP-1, TP-3, TP-8; Must for scorable folds)**

* RF 0.744 against class shares 1.284 and linear 0.880 (claim audit 37, today's probes): a real signal, and the
  families spread. Macro AUC 0.91 across wells (split audit).
* `no_spread` is untuned LightGBM diverging (min_child_weight 0.001, log loss 2.68); with min_child_weight 1 it gives
  0.81. Same reading as mice_protein (SPLIT-27). The blind reviewer counts the sensitivity to between-well shift as a
  benchmark virtue.
* Every fold is scorable: every train side holds all 11 classes; Halite/Anhydrite absent from one test fold is
  accepted with correct counts and TP-8 names this dataset as its own example (precedents 11). Another random well
  assignment moves log loss by 0.004.

**4. Log loss over the penalty matrix (TP-6 Must vs definitions.md "Field mapping")**

* The precedents agent shows the two texts contradict each other; no dated curator precedent exists on either side.
  That is a rule-level question for the curator, not a defect of this dataset.
* Facts that set it apart: the matrix scores hard labels; none of the top three trained on it ("relied on a standard
  multiclass log-loss", retrospective p. 3-4); the practitioner wants per-class probabilities for QC. So log loss is
  not a worse version of the task.
* Mildest remedy: record an exception to TP-6 with these facts (or register an 11 x 11 expected-penalty metric if the
  curator prefers). Either way the dataset ships.

**5. Cleaning gaps are real, cheap and P7 (CLEAN-10, CLEAN-11, CLEAN-21; Should)**

* Concede: DRHO holds RHOB in 36/7-3 (3,474 rows) and a density curve in 31/4-10 (2,208); one -7,429 value; RXO/ROPA
  leftovers near -950 to -996; negatives in RXO 131, ROP 52, SGR 39, RMED 7; ROP/SGR/ROPA wells on another scale. The
  bullet "become missing in RXO, SP and ROPA" also misdescribes the code (it masks all 20 curves).
* Rank: principles step 3, a quality problem is fixed when cheap and safe; it does not reach validity. Mildest fix in
  `_clean`: mask log values < -900, |DRHO| > 1, DCAL > 100 and negatives of resistivity/GR/ROP curves (the sdss_17,
  churn_telco_south_asia precedents); a note naming the off-scale ROP/SGR/ROPA wells.
* MUDWEIGHT: keep with the existing note as an exception to CLEAN-21 (scale constant per well, every fold trains on
  each scale, 89 of 118 wells lack it), or drop it as college_scorecard did; a guessed bar/m conversion is not allowed.

**6. The other choices are consistent (LEAK-10, CLEAN-17, SPLIT-24)**

* Confidence dropped: recorded with the label, absent in open test (claim audit 9, 25).
* Basement dropped: 103 rows in one well, so no grouped split can train and test it (CLEAN-17 departure with the
  fact, P4/P6). WELL is the group column and not a feature (LEAK-33), which answers the blind reviewer's concern 6.
* No duplicates, no copies across folds, md5 and pinned commit match, license CC BY 4.0.

**7. Stale numbers and wording (EV-8; procedure)**

* Concede: the probe numbers (linear 0.989, gap 0.19, LightGBM 2.77) are stale; 34/5-1 does share 2,273 MD values
  and lies 1.5-1.9 km apart; "all 13 finalists used tree ensembles" should be 12 of 13; domain should be "environmental
  science & climate" (covertype, forest_fires). All are text edits.

Judgment record (proposed):
Verdict: ship after changes.
Validity: SEL holds; USE-1 holds (direct fit, released-well use case per USE-9); LEAK-10 not strong for GROUP/FORMATION,
note reworded; SPLIT-1 holds (grouped by well), SPLIT-19 departure documented.
Value: TP-1/TP-3 real signal (RF 0.744 vs 1.284); TP-8 accepted fold gap; TP-6 metric exception for the curator.
Quality: CLEAN-10/11 fixed by masking; CLEAN-21 MUDWEIGHT kept with a note (exception) or dropped.
For the curator: issue 2 (fit direct vs approximate), issue 4 (TP-6 vs definitions.md).

**Rebuttal**

Both briefs reach the same verdict: ship after changes, no exclusion. Most of the critic's points are conceded. Two
are disputed in part, and on those the dispute is about which remedy to use, not whether to ship.

**1. GROUP/FORMATION and the `direct` fit: concede the problem, dispute part of the effect, prefer remedy (a)**

* Conceded: the 10% sentence has to go. The note should give the 4x enrichment (66% vs 23% within 0.76 m), the shared
  post-well sources and the lithology-named formations. With the use case as written ("a newly drilled well"),
  `direct` is not yet backed.
* Disputed: calling them "the strongest single features" overstates what they add. Univariate AUC is not the gain in
  a model. On their own, with depth and location, they reach accuracy 0.44, below the 0.613 majority baseline (blind
  review). Dropping them moves log loss 0.764 to 0.809, about 6%. LEAK-10 is graded, and at this size it is not
  strong. So the remedy does not have to be the kick rung.
* Which remedy: (a) the use case "a newly drilled or a released well", with `direct` kept. USE-9 (Should, narrows
  USE-8) puts this rung before approximate. It rests on facts, not on rephrasing: the labels were built for 118
  released wells, and the practitioner names the backlog as "the larger real use", where "the NPD tops are exactly
  what I would use". This sets force apart from kick, where no such use case was shown. Option (b) stays the fallback
  if the curator rejects (a). This is a weighing call for the curator.

**2. TP-6 and the penalty matrix: concede my wording, dispute that TP-6 is broken**

* Conceded: "an exception to TP-6" was the wrong form. A Must has no exceptions (principles.md).
* Disputed: TP-6 is not triggered. Its first sentence keeps two questions apart: is the task valid, and is it the
  best version. A source version replaces ours only when it is the better version. The matrix scores argmax labels,
  so it cannot rank probabilistic predictions. The top three teams trained on log loss instead (retrospective
  p. 3-4), and the practitioner wants probabilities for QC. On these facts the matrix is not a better version, so
  log loss is consistent with TP-6.
* What follows: write those facts in the notes (the critic's interim remedy, agreed). The contradiction between TP-6
  and definitions.md is about the rules, not this dataset. It goes to the curator as an amendment question and does
  not block the ship.

**3. No `splits_comment`: concede**

Add a `splits_comment`. It names the departure from 98/10/10 with the organisers' reason, and says the score stands
for wells in explored areas (0.763 well, 0.814 block, 1.015 quadrant).

**4. DRHO: concede**

Mask |DRHO| > 1 g/cm3 (about 5.7k rows) and add a bullet.

**5. Second scales: concede the note, dispute masking as the default**

Name the ROP (25/6-2), SGR (34/12-1, 35/11-15 S) and ROPA (34/4-10 R) wells in a note. Unlike DRHO, these look like
real readings in another unit, not impossible values. Masking would throw away signal that every fold can learn
per well, for the same reason given for MUDWEIGHT (scale constant per well, every scale on both sides of each fold).
Record that fact as the CLEAN-21 exception, which sets the case apart from college_scorecard (a scale break in
time). Masking stays the curator's alternative.

**6. Sentinels and negatives: concede**

Mask values below -900 in the log curves (not Z_LOC), the negatives of the resistivity, GR and ROP curves, and
DCAL > 100. Then fix the bullet to say the code masks all 20 curves.

**7. Stale statements: concede all**

Update the probe numbers, the 34/5-1 wording and distances, name the forest, set the domain to "environmental
science & climate", and correct the record's "no known risk".

Net: one weighing call (issue 1, (a) or (b)) and one rule question (TP-6 vs definitions.md) for the curator. The rest
are definition and text fixes.

</details>

<details><summary>Critic</summary>

Position: **ship only after changes.** The task is real (whole new wells, interpreted lithology, the practitioner
agrees), so nothing here asks for exclusion. But the definition claims a `direct` fit on a reading of the
GROUP/FORMATION evidence that the data contradicts, it does not address the source's own scoring (TP-6), and the text
carries refuted numbers. Points in rank order.

**1. GROUP/FORMATION: the definition calls them independent of the label, but the data shows they are not, and the fit is still `direct` (P3/P4; USE-3, LEAK-10, USE-8, all Must)**

- Problem: `fit_reason` and the GROUP/FORMATION note say every feature is known once the well is logged, and that
  "only 10% of the 574 group boundaries fall on a lithology change". The note uses that figure to suggest the picks are
  only loosely tied to the label. The data says the opposite. The base rate of a lithology change at a sample is 2.5%,
  so boundaries are 4x enriched. Within +-0.76 m (NPD's whole-metre rounding), 65.7% of group boundaries and 62.8% of
  formation boundaries sit on a change, against 23.4% at random (claim_audit #33, c_bound.py). The labels were drawn
  from completion logs and mud logs (blog p. 3), the same post-well material NPD picks from. Lithostratigraphic units
  are defined by lithology: 14,709 of 14,711 Halite rows are in Zechstein. Four FORMATION names state a lithology
  ("Intra ... Fm. Sst.", "Ran Sst Mb."; 0.66% of rows, column_audit). Whether NPD's tops exist when a newly drilled
  well is first interpreted is unsettled. The practitioner says that at that stage you have the operator's tops, not
  NPD's.
- Effect: GROUP and FORMATION are the strongest single features (macro AUC 0.85 / 0.83). Without them the RF log loss
  goes 0.764 to 0.809 (claim audit) or 0.776 to 0.836 (the earlier REVIEW.md). Part of the score comes from an interpretation
  that may postdate the prediction point.
- Rule: USE-8 lists "a potential leak kept on purpose" under approximate. The kick precedent was decided that way
  (precedents #5). That leaves force `direct` while kick is `approximate` on the same open fact.
- Remedy, the mildest that resolves it (not a drop; the source lists them as inputs, TP-6/USE-4). Either
  (a) restate the use case as "a newly drilled **or released** well" (USE-9, the practitioner's backlog use, where NPD
  tops do exist) and record that as the fact behind `direct`; or (b) set `fit="approximate"` with a
  `Potential leak, kept on purpose:` note. In both cases rewrite the note: give the 4x / 66%-vs-23% alignment and the
  shared sources instead of the 10% sentence.

**2. The source's scoring is not addressed (P6; TP-6, Must)**

- Problem: TP-6 says a better version the source defines, including "the scoring it uses", replaces ours. FORCE
  defines a 12x12 penalty matrix (`penalty_matrix.npy`, Zenodo). The definition only notes "we score log loss". It
  gives no fact that sets this case apart. Amex, allstate, porto, 5g and sepsis ship their competitions' metrics
  (precedents #10). definitions.md says the opposite of TP-6 ("keeps our default"), so the rules contradict each
  other.
- Effect: the ranking ignores the geological cost of confusions (sandstone vs shale against sandstone vs
  sandstone/shale). The practitioner rates this as small.
- Remedy: the curator settles the contradiction (a Must has no exceptions, so this needs an amendment of TP-6 or
  definitions.md). Until then, write the fact in the notes: the matrix scores hard labels, and the top three trained
  on log loss (retrospective p. 3-4). The other option is to register an 11x11 expected-penalty metric.

**3. The departure from the competition split is not written where the split is described (P4; SPLIT-19, Should)**

- Problem: there is no `splits_comment`, so the README says "Default splits." for a deliberate departure from
  98/10/10. Test wells sit near training wells: median 8 km to the nearest one, 55-76% share a licence block, 95-100%
  a quadrant. Log loss is 0.763 for the shipped well split, 0.814 grouped by block and 1.015 grouped by quadrant
  (split_audit).
- Remedy: a `splits_comment` that names the departure and its reason, and says the score stands for wells in explored
  areas, not frontier wells. The split itself is right.

**4. DRHO holds another curve in two wells (P7; CLEAN-11, Should)**

- 36/7-3: DRHO equals RHOB on all 3,474 rows. 31/4-10: DRHO is a density curve (median 2.38, 2,208 rows). One more
  row reads -7,429.3. A density correction of about 2.4 g/cm3 is impossible (column_audit #2).
- Remedy: mask |DRHO| > 1 g/cm3 (about 5.7k rows) and add a bullet. Cheap and safe.

**5. Wells on a second scale beyond MUDWEIGHT (P7; CLEAN-21, Should)**

- ROP in 25/6-2 has a per-well median of 17,778 (2,925 rows), against 0.6-150 elsewhere. SGR in 34/12-1 and
  35/11-15 S has a median of about 0.01 (8,731 rows), against 46-106. ROPA in 34/4-10 R has a median of 0.099. Only
  MUDWEIGHT is documented. Precedent: college_scorecard dropped what it could not convert.
- Remedy: a note naming these wells and curves, or mask the off-scale wells per curve. For MUDWEIGHT, record the fact
  that sets it apart from college_scorecard: the scale is constant per well, and both sides of every fold hold every
  scale.

**6. Leftover sentinels and impossible values; the bullet misdescribes the code (P7; CLEAN-10, CLEAN-11, Should)**

- Leftover sentinels: RXO -995.9 and -968.1, and ROPA -965.9 and -948.9. These are interpolation ramps from the LAS
  null.
- Impossible negatives: RXO 131 rows, ROP 52, SGR 39 (down to -778), RMED 7. DCAL has one value of 10,006.8.
- The bullet says the nulls become missing "in RXO, SP and ROPA". The code masks all 20 curves.
- Precedents sdss_17, heart_disease_va_long_beach and churn_telco_south_asia all set such values to missing.
- Remedy: mask values below -900 in the log curves (not Z_LOC), and the negatives of the resistivity, GR and ROP
  curves. Then fix the bullet.

**7. Refuted or stale statements in the definition (procedure; EV-8, EV-1)**

- `no_spread` bullet: it gives linear 0.989, gap 0.19 and LightGBM 2.77. Today's values are 0.880, 0.107 and 2.678.
- 34/5-1 A and S: the definition says they "share no depth sample" and lie "1.1-1.9 km" apart. They share 2,273 MD
  values and lie 1.5-1.9 km apart at equal MD (1.9-2.1 km at equal TVD). The two-groups conclusion stands.
- The random forest behind 0.31 / 0.78 / 0.84 is not named.
- Domain "chemistry & material science": the geoscience peers use "environmental science & climate".
- Record: "no known risk" contradicts the open point 1.
- Remedy: correct the text.

Not argued: depth-window features (the measured gain is small, 0.776 to 0.764; leaving it to the pipeline follows
open_university). Basement dropped (one well, stated). Halite/Anhydrite missing from fold r0f2 (accepted with correct
counts).

**Rebuttal**

We agree on the verdict: ship after changes, with no case for exclusion. Two points stay disputed: (2), only in part,
and (4).

**A1. A real task and a grouped split: concede**

The `splits_comment` remedy is the one I asked for in my point 3. It names the departure from 98/10/10 and says the
test wells have drilled neighbours.

**A2. GROUP/FORMATION: concede in part, dispute in part**

- Concede:
  - Keep both columns. I never asked to drop them.
  - Reword the 10% sentence with the 4x enrichment and the shared sources.
  - If the use case is restated as "a newly drilled or a released well" (USE-9), the fit can be `direct`, because NPD
    tops exist for released wells (practitioner).
- Dispute 1: the restatement has to be made in the definition, not assumed.
  - Today `question`, `use_case` and `fit_reason` all say "a newly drilled well", and the split says it "stands for
    wells never interpreted".
  - For a newly drilled well the practitioner says you would have the operator's tops, not NPD's.
  - So `direct` holds only after the text changes. Until then the kick precedent applies (USE-8, Must): `approximate`
    with a `Potential leak, kept on purpose:` note.
- Dispute 2: the "0.44 accuracy, below majority" argument does not show the columns are free of the target.
  - Accuracy below the majority baseline is what any rare-class signal looks like when shale is 61% of the rows.
  - FORMATION alone has macro AUC 0.85 (leak probe).
  - 14,709 of 14,711 Halite rows lie in Zechstein.
  - Four formation names state a lithology ("Intra ... Fm. Sst.", "Ran Sst Mb."; 0.66% of rows, column_audit).
  - I accept the advocate's point that this is not a strong leak. But the note must state these facts, not the
    accuracy figure.

**A3. Worth benchmarking: concede**

RF 0.744 against 1.284, the LightGBM divergence reading and the accepted fold gap all hold.

**A4. Metric: dispute the remedy**

- The advocate proposes "an exception to TP-6". TP-6 is a Must, and principles.md says: "A Must has no exceptions:
  only a higher-ranked Must overrides it, and anything else is an amendment."
- Rule that wins: principles.md, Exceptions and amendments.
- Remedy: the curator amends TP-6 or definitions.md so the two texts agree, or registers an 11x11 expected-penalty
  metric. The facts the advocate gives (hard labels; the top three trained on log loss) belong in that amendment and
  in the notes.
- The dataset ships either way.

**A5. Cleaning: concede**

I accept the same masks and the note on the off-scale wells. For MUDWEIGHT, I accept an exception to CLEAN-21 with the
per-well-scale fact. CLEAN-21 is a Should, so an exception is allowed.

**A6. Other choices: concede**

**A7. Stale numbers and wording: concede**

I add one item: the record's "no known risk" should name point 2.

</details>
