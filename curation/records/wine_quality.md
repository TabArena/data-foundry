---
unique_name: wine_quality
name: wine_quality
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
- WIP (DF)
claimed_by: Andrej
suggestion: 'Yes'
priority: 3
tags:
- 'Samples: Over Time'
- 'Time: Inferred'
- Non-IID (Temporal)
original_source: UCI
year: '2009'
domain: chemistry & material science
required_split:
- Temporal (NON-IID)
problem_type: Regression
source_links:
- https://www.openml.org/search?type=data&id=287
- https://doi.org/10.24432/C56S3T
notebook_path: datasets/beyond_iid/old_iid/wine_quality/wine_quality.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/wine_quality/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

CC (2026-09-30, Lennart): **Leak fixed by deduplication, split stays IID.** 1,177 of 6,497 rows (18%) are exact copies of another row (all 11 lab values, colour and the median score; 992 sets of up to 8 copies; no set has conflicting scores), so under the random split a row's twin often sits in train. Cortez et al. 2009 (Decision Support Systems 47(4)), Sec. 2.1: the data come from the CVRVV certification system (iLab, May 2004 - February 2007), "Each entry denotes a given test (analytical or sensory)", and the database "was transformed in order to include a distinct wine sample (with all tests) per row"; duplicates are not mentioned. The copies are most likely repeated records from that export, so we drop them (6,497 -> 5,320 rows) instead of grouping, which would only reproduce the deduplication. The paper itself evaluates with 20 runs of random 5-fold CV (Sec. 3) on the data with copies. TabArena v0.1 dataset: results on the old container are not comparable with the deduplicated one.

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Originally two datasets with red and white wine. They are diszinguishable by features such as sulfur dioxide. But still unsure whether it makes sense to use them together. Also there are many duplicates, might need to account for that.

Potential issue: Omitted variable bias? Grouped data

Lennart: use UCI version with indicator

Andrej: Add red/white wine indicator

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source mae — MAD of Cortez et al. 2009 (scored metric changed from rmse to mae).

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship after dropping 49 near-copies the exact deduplication missed (same wine, one value re-entered, grade equal in 49 of 49 pairs; 1.3% of test rows) and noting density's two recording precisions (about 0.1 grade apart). Priority 3: gap 0, use case 1, source 1, shape 1, risk -1.

CC (2026-11-11, Andrej): `domain` set to the definition's `chemistry & material science` (review page field mark "update"; the record had none).

CC (2026-11-13, Andrej): split by file position instead of random wines (Review issue 3, B), a judgement call, documented in the definition's notes:
- Problem: the release has no dates (May 2004 to February 2007 only), but the raw file order is very likely the order of entry, and a random split trains on wines entered next to the test wines.
- Evidence for entry order, against five other readings (requests entered together, sorted by producer, by a column, by a dropped attribute, shuffled): both colour files write density with 5 decimals in the same stretches; they drift alike (grade per tenth of each file r = 0.78, at most 0.48 shifted) with a wave of about a year; on equal test wines and training size, untuned LightGBM MAE 0.528 random, 0.535 neighbours left out, 0.546 earlier wines only.
- Change: `file_position`, a row's share of its colour file (no date; assumes a steady pace in both files), orders nine windows of 295 wines over the newest half, each trained on all earlier wines (50% to 94%). It is no model input (`Temporal(..., feature=False)`): a row's place in an exported file is not something the grader holds.
- Would overturn it: CVRVV sample numbers or dates showing another order, such as a sort by producer.
- Not changed: rows (5,320), features, target, metric. Issues 1, 2 and 4 are still open.

CC (2026-11-13, Andrej): density's two recording precisions kept as published, with a curation note (Review issue 2, B):
- Recording batch: density has 5 decimals in 2,443 rows and 4 or fewer in 2,877, and the 5-decimal rows grade about 0.1 higher in both colours (red 5.68 against 5.57, white 5.90 against 5.81); instrument or period is undocumented.
- Kept, not rounded: a model reads the batch only through an engineered count of decimals, and whether it is an artefact or a real effect of time is unknown.
- Not changed: rows, features, values, split, metric.

CC (2026-11-13, Andrej): the pairs of wines analysed twice stay as they are, no group key (Review issue 4, A):
- Why kept: 115 pairs of one colour share 5 to 8 of the 11 lab values and sit next to each other in the file; each row has its own analysis and grade (same grade in 76%), and the nine windows by file position keep a pair on one side (2 of 2,655 test rows have a partner in training).
- Why not grouped: the key would be rebuilt from the values and the file order, a judgement call, for 2 rows.
- Not changed: rows, features, values, split, metric.

CC (2026-11-13, Andrej): the 49 near-copies dropped, keeping the first row of each pair in file order (Review issue 1, B):
- Near-copies: 49 pairs of one colour agree on 10 (47 pairs) or 9 (2 pairs) of the 11 lab values.
- Double entries, not retests: 1 value differs (fixed acidity, alcohol, residual sugar or total SO2 only), against 3 to 6 in the 115 pairs analysed twice (kept, issue 4); the same grade in 49 of 49 pairs, against 76%; alcohol off by exactly 1/60 or 1/30; 1 to 17 rows apart like the exact copies.
- Change: 5,320 -> 5,271 wines (41 white, 8 red rows leave); grade shares move by at most 0.04 points (mean 5.796 -> 5.794). `file_position` is computed before the drop, so positions stay those of the raw file; the nine windows keep 295 test wines each, trained on 2,616 to 4,976 wines.
- Not changed: features, target, split definition, metric.

## Review

**Outcome:** added. Red and white Vinho Verde wines certified by the CVRVV between May 2004 and February 2007 (Cortez
et al. 2009, Decision Support Systems 47(4):547-553, https://doi.org/10.1016/j.dss.2009.05.016; UCI
https://doi.org/10.24432/C56S3T): the median of at least three tasters' grades (0 to 10) from eleven lab measurements
and the colour; 5,320 wines after the 1,177 exact repeated rows were dropped (Lennart, 2026-09-30), 5,271 since the 49 near-copies left on 2026-11-13 (issue 1); nine windows by
file position since 2026-11-13 (issue 3); MAE, the paper's measure. The AI recommended shipping it after dropping the near-copies the exact deduplication missed
(issue 1, done 2026-11-13). Reviewed on 2026-11-04 without a panel, from the gathered evidence (the record, the CHANGELOG, the
model runs on the shipped data and on TabArena v0.1's copy) and two checks on the v0.2 frame. Validity: the
certification body's own lab tests and tasting grades, a decision the source names (supporting the tasters); 49 pairs
of rows were one wine with one value re-entered, now dropped (issue 1), and density was recorded at two precisions whose rows
differ by about 0.1 grade (issue 2). Value: on the shipped data (with the copies, random splits) the 40 benchmark
methods
spread from RMSE 0.580 (Kumo, TabPFN 3.5) to 0.730 (linear models), median 0.600, so the methods separate, though the
best are close. Quality: the grade takes only 7 values, modelled as regression as in the paper (accepted). Weighed: a
certification body's real data and decision +, clear separation from linear models +, residual re-listed wines -, a
recording batch in one column -.

**Main points:** All four issues resolved (2026-11-13), the definition changed, nothing rebuilt: the 49
near-copies dropped as double entries, 5,271 wines (issue 1, B); nine windows by file position, a judgement call
documented in the definition, the position no model input (issue 3, B); density's two precisions kept with a note
(issue 2, B); the pairs analysed twice kept, the windows hold them together (issue 4, A). Open: the rebuild (the
shipped container still has 5,320 wines and random splits), and the file order as time, which CVRVV sample numbers or
dates could overturn.

**Record judgment:** valid. The record carries the deduplication (CC 2026-09-30) and the metric (Assessment
2026-10-21).

**Issues for Andrej:**

1. **Drop the 49 near-copies that the exact deduplication missed?**

   * **Problem:**
     - After the 1,177 exact copies left, 49 pairs of wines of one colour still agree on 10 of the 11 lab values (47
       pairs) or on 9 (2 pairs), and every one of the 49 pairs carries the same grade, against 32% for random pairs of
       one colour.
     - They are the same wine listed twice with one value re-entered (fixed acidity off by 0.1, alcohol by 0.017,
       total sulphur dioxide or residual sugar), the same kind of repeated record that was dropped on 2026-09-30.
     - Drop one row of each pair, or keep them?
   * **Background:** the paper turned per-test entries into "a distinct wine sample (with all tests) per row" (Cortez et
     al. 2009, Sec. 2.1); the exact copies were judged repeated records of that export and dropped[^1a]. A copy with
     one value retyped is the same wine and the same tasting, so its grade gives its twin away.
   * **Effect on the task:** small: under the shipped random splits 1.3% of the test rows have such a twin in
     training, and they are scored by look-up.
   * **Experiments:** v0.2 frame, the 9 shipped splits, untuned LightGBM: MAE 0.541 on all test rows, 0.546 on the
     test rows without a twin in training. Simple models on the shipped data looked up these
     re-listings ("a test wine sharing 10-12 of 12 recorded values with training wines ... takes their grade") and
     were flagged as leaks.
   * **Consistency:** follows the curator's deduplication of 2026-09-30 (exact copies dropped, not grouped); a
     confirmed leak goes even when small[^1b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | 5,320 wines | no further change | 1.3% of test rows answered by a re-listed twin |
     | B | Drop one row of each pair | 49 rows leave, 5,271 wines | the same rule as the exact copies; no wine twice | 0.9% fewer rows |
     | C | Group the pairs | each pair shares a fold | all rows kept | a group column for 49 pairs; the curator chose dropping over grouping for the exact copies |

   * **Recommendation:** B, the deduplication of 2026-09-30 carried to the copies it missed. **Decision:** keep (A),
     drop (B) or group (C)?

   **Notes for the AI:** on B, after the exact deduplication in `_clean`, drop the later row of every pair of the same
   colour that agrees on at least 9 of the 11 lab values (49 pairs, 98 rows in pairs; grade equal in all); extend the
   deduplication bullet and the task summary's `changes`; `dataset check`; CHANGELOG; record CC.

   [^1a]: **LEAK-19** (Should): exact copies with the same label: drop them rather than group on the duplicate key;
     wine_quality (1,177 rows) is the rule's case.
   [^1b]: **LEAK-6** (Must): measure before acting; a slight optimism with a known cause can stay with a note, a
     confirmed leak goes even when small. **LEAK-17** (Must): repeated entities in different rows leak the target
     across the split even when the rows differ.

   **Answer (AI, 2026-11-06):** the new entity-leakage rules applied to the near copies; the recommendation (B) stays.

   * **Verdict: entity fix, copies of one record.** Each pair is one wine entered twice with one value retyped, so it
     goes down to one row[^1e].
   * **Is the link real?** With each lab value shuffled within colour, no pair of rows shares 9 of the 11 values in
     200 draws, against 49 pairs in the file.
   * **Does the grade travel with the link?** The grade agrees in 49 of 49 pairs; a wine and its nearest wine in
     chemistry elsewhere in the file share the grade in 45% of cases, random pairs of one colour in 33%.
   * **Is there an order?** The two rows of a pair sit 1 to 17 rows apart in the raw file (median 4), as close as only
     0.85% of random pairs of one colour: entered together, not tasted later, so the split needs no time fix.
   * **What the drop does to the grade:** 49 rows (0.9%; 41 white, 8 red), all of grade 5, 6 or 7 (14, 24 and 11).
     - Grade shares before and after: grade 5, 32.9% and 33.0%; grade 6, 43.7% and 43.6%; grade 7, 16.1% and 16.0%;
       the other grades rise by at most 0.04 points; mean grade 5.796 and 5.794.
     - Does the target still stand for the use case? The AI reads yes: the grade's distribution moves by at most a
       tenth of a point.
   * **A second link, a separate decision:** 111 more pairs, entered next to each other, share 5 to 8 values and
     differ in the rest by small amounts, and their grade differs in a quarter of them: one wine analysed and graded
     twice. Each row has its own grade, so the rules group such rows rather than drop them: issue 4.

   **Notes for the AI:** the dropped row is the later row of each pair in the
   frame's order (white file first), as in the notes above.

   [^1e]: **LEAK-41** (Must; draft PR #62): repeats of a unit the data does not record get one of four verdicts:
     natural, entity fix, temporal fix or not recoverable; an entity fix takes copies of one record down to one row
     per unit and groups several observations of one unit that each carry their own label; every drop gives the
     label shares before and after and asks whether the target still stands. **LEAK-42** (Should; draft PR #62):
     three tests set the verdict: a link far above a chance rate that keeps the data's structure, a label that
     travels with the link beyond what the shared features predict, and an order.

   **Andrej (2026-11-13, discuss):** Now with a temporal split, is the problem solved?

   **Answer (AI, 2026-11-13):** The leak, mostly: under the nine windows 2 of 2,655 test rows have their copy in
   training, against 1.3% under random splits. The repeated record itself is untouched.

   | 49 copies, 5,320 wines, no model | Random split (before) | Nine windows by file position |
   |---|---|---|
   | Test rows whose copy is in training | 1.3% | 2 of 2,655 (0.08%), both in the newest window |
   | Pairs with both rows in one test window (one wine scored twice) | | 37 |
   | Pairs with both rows in a window's training (one wine weighted twice) | | 10 to 37 per window |

   * The copies sit 1 to 17 rows apart and a window holds 295 wines, so a pair almost always lands on one side.
   * What stays: each pair is one wine and one tasting entered twice, the case the exact deduplication of
     2026-09-30 dropped whatever the split. In the test half 37 wines count twice in the MAE.
   * Status: reduced (look-up on 2 rows); the duplicate record unchanged.
   * C (group) no longer does anything the windows do not; it drops out.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | A | Keep (implemented) | 5,320 wines | no change; the windows remove almost all the look-up | 37 test wines scored twice, 2 test rows answered by their copy |
   | B | Drop one row of each pair | 49 rows leave, 5,271 wines | the exact-copy rule carried to the copies it missed; no wine twice | 0.9% fewer rows |

   **Recommendation:** B, now as consistency with the deduplication rather than as a leak fix. **Decision:** keep
   (A) or drop (B)?

   **Notes for the AI:** measured with the shipped `TemporalSplits` built on the frame `_clean` returns; copies = same colour, at least 9 of 11 lab values
   equal.

   **Andrej (2026-11-13, re: answer of 2026-11-13):** But this is an assumption, what if it was indeed a retest of
   the same wine in those cases?

   **Answer (AI, 2026-11-13):** The evidence says double entry, not retest: in a real retest (issue 4's pairs) 3 to
   6 values differ and the grade differs in a quarter of the pairs; in the 49 copies 1 value differs, never one of
   the noisy measurements, and the grade agrees in all 49.

   | Pairs of one colour, at most 17 rows apart | 49 near-copies (issue 1) | 115 pairs analysed twice (issue 4) | 1,177 exact copies (dropped 2026-09-30) |
   |---|---|---|---|
   | Lab values that differ | 1 (47 pairs) or 2 | 3 to 6 | 0 |
   | Which ones | fixed acidity, alcohol, residual sugar, total SO2 only | any; volatile acidity in 72%, free SO2 in 70%, chlorides in 64% | |
   | Same grade | 49 of 49 | 76% | all |
   | Rows apart: median; next to each other | 4; 8% | 1; 62% | 3; 21% |

   * Two populations, no continuum: pairs with 5, 6, 7, 8 equal values number 58, 32, 20, 5; then 2 with 9 and 47
     with 10. Retest noise does not produce a second peak at 10 of 11.
   * Noise: with issue 4's per-value agreement rates, a retest agrees on 10 or more values with chance 0.4%;
     volatile acidity, free SO2, chlorides and density, which differ in 43% to 72% of the retests, never differ in
     the copies.
   * The differences are arithmetic, not measurement: alcohol differs by exactly 1/60 or 1/30 (9.2333 against 9.25,
     15 pairs), below the 0.1 a retest's alcohol moves; fixed acidity by 0.1 to 0.4, once 14.2 against 7.4.
   * Grade: at issue 4's 76% agreement (80% for pairs with 8 equal values), 49 agreements in 49 have a chance of 2 in
     a million (2 in 100,000). If the lab was repeated, the tasting was not: the grade was copied.
   * Position: the copies sit 1 to 17 rows apart like the exact copies (median 3, 99% within 17), not side by side
     like the retests.
   * If they were retests after all, they are issue 4's case, which you kept (A): consistency would then be keep (A)
     here, and B's argument (the exact-copy rule carried on) would fall. Under the windows the two differ by 49 rows,
     2 test rows answered by their copy and 37 test wines counted twice.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | A | Keep (implemented) | 5,320 wines | treats them like issue 4's pairs, if retests; no change | the evidence reads double entry; 37 test wines scored twice, 2 answered by their copy |
   | B | Drop one row of each pair | 49 rows leave, 5,271 wines | the exact-copy rule for what the evidence shows are copies of one record | if some are retests, an analysis lost (0.9% of rows) |

   **Recommendation:** B: the copies match the exact copies on every test (values, grade, position) and the retests
   on none. **Decision:** keep (A) or drop (B)?

   **Notes for the AI:** measured on
   the raw UCI files, pandas only; "issue 4's pairs" = same colour, 5 to 8 of 11 values equal, at most 17 rows apart,
   on the frame before issue 1's drop (115 pairs).

   **Andrej (2026-11-13, re: answer of 2026-11-13):** Reply (B): Drop one row of each pair

   **Resolved (2026-11-13, Andrej):** B: in `_clean`, after the exact deduplication, rows of one colour that agree on
   at least 9 of the 11 lab values with an earlier row are dropped, keeping the first in file order; `file_position`
   is computed before, so positions stay those of the raw file. 49 rows leave (41 white, 8 red): 5,320 -> 5,271
   wines, grade shares move by at most 0.04 points (mean 5.796 -> 5.794).

   | Nine windows by file position | Before | After |
   |---|---|---|
   | Wines | 5,320 | 5,271 |
   | Test wines per window | 295 | 295 |
   | Training wines, oldest to newest window | 2,665 to 5,025 | 2,616 to 4,976 |

   Curation note with the evidence (1 value differs against 3 to 6 in retests; the same grade in 49 of 49; alcohol
   off by 1/60 or 1/30), task summary `row` and `changes` updated, `dataset check` passed; record CC line. Not rebuilt.

2. **Keep density's two recording precisions as published, with a note?**

   * **Problem:**
     - Density is written with 5 decimals in 2,443 rows and with 4 or fewer in 2,877, about half of each colour, and
       the 5-decimal rows grade higher in both colours (red 5.68 against 5.57, white 5.90 against 5.81).
     - The precision marks a recording batch (an instrument or a period of the certification system) that carries
       about 0.1 grade, a signal that does not come from the wine's chemistry.
     - Keep it with a note, or round density to 4 decimals so the batch cannot be read?
   * **Background:** the release has no date or laboratory per row. A model sees the batch only through the number of
     decimals, so a method has to build that feature to use it; one model did (a 0/1 flag for 5 decimals) and
     gained 0.23% RMSE on held-out splits of the shipped data. Density varies by about 0.003 between wines, so a fifth
     decimal (0.00001) carries almost no chemistry.
   * **Unknown:** whether the batches are periods whose wines were graded differently (a real effect of time) or two
     instruments; the source does not say.
   * **Consistency:** recording conventions that let a model tell outcomes apart are harmonised when the fix is
     measured[^2a]; gallstone_disease's class-specific formats were. Here the convention is not tied to a class but
     to a 0.1 grade shift, and no shipped feature reveals it without engineering.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep as published (implemented) | values as published, no note | the published values | the batch and its 0.1 grade are undocumented |
     | B | Keep with a note | as A, plus a `curation_comments` bullet naming the batches and the 0.1 grade | the published values; only an engineered digit count reads the batch | a method that counts decimals can use it |
     | C | Round density to 4 decimals | every density at the coarser precision | the batch cannot be read; the lost decimal is far below the spread between wines | changes published values; if the batches are periods, a real effect is hidden |

   * **Recommendation:** B: the shift is small, reaching it needs an engineered feature, and whether it is an
     artefact is unknown. **Decision:** as published (A), with a note (B) or rounded (C)?

   **Notes for the AI:** on B, a bullet: "Density is recorded with 5 decimals in 2,443 rows and 4 or fewer in 2,877;
   the 5-decimal rows grade about 0.1 higher in both colours (a recording batch, kept)". On C, `df["density"] =
   df["density"].round(4)` before the deduplication (check that it creates no new copies), and rerun the checks.

   [^2a]: **LEAK-13** (Must): class-specific recording conventions are harmonised: write every row at the precision of
     the measured values; first measure how much the fix removes.

   **Andrej (2026-11-13, change):** Option B: Keep with a note.

   **Resolved (2026-11-13, Andrej):** B: kept as published, with a note.
   - `curation_comments` bullet: 5 decimals in 2,443 rows, 4 or fewer in 2,877 (counted again on the 5,320 wines);
     the 5-decimal rows grade about 0.1 higher in both colours (red 5.68 against 5.57, white 5.90 against 5.81); a
     recording batch of unknown cause, read only through an engineered decimal count, kept.
   - Record: CC line, `Andrej` in `checked_by`.
   - `dataset check`: 0 errors, 0 warnings, 0 info; README regenerated (the new bullet only); not rebuilt.

3. **Split by time, or keep the random split as forced, the file order not counted as time?**

   * **Problem:**
     - The source dates the wines only as May 2004 to February 2007, but the raw file order is very likely the order of
       entry: along the file the mean grade, alcohol and acidity follow the same pattern in the red and the white file
       (grade per tenth of each file, r = 0.78 between the colours, against at most 0.48 for any shifted pairing).
     - The certification body grades later wines, so the order is information for the split; the random split can
       carry the forced tag, with the undocumented order not counted as time[^3a], and gives up 3% of the MAE for
       LightGBM, in every window.
     - Split by file position, or keep the random split as forced?
   * **Background:** the two files share no row key, so the time key is a row's position as a share of its own file (0
     for the first row, 1 for the last), which puts both colours on one axis if both were entered at a steady pace over
     the same period. The shared pattern holds at 10, 20 and 30 bins (grade r = 0.78, 0.72 and 0.74 against shifted
     maxima of 0.48, 0.50 and 0.58; alcohol 0.87, fixed acidity 0.91 at 10 bins). Density switches from 4 to 5
     decimals in the middle of both files (between 40% and 55% of the rows), and exact copies sit next to each other
     (91 red, 235 white), as in an export in entry order. Two files exported in date order from one certification system would show
     this; the source does not say so.
   * **Experiments:** the 5,320 shipped wines and 12 features, untuned LightGBM and ridge regression, MAE (Slurm job
     1365901):
     - Shipped random split (3 x 3): LightGBM 0.541 (0.526 to 0.550), ridge 0.566.
     - Nine windows of 295 wines over the newest half by file position, each trained on all earlier wines (50% to 94%
       of the rows): LightGBM 0.486 to 0.611, 0.499 on the newest; ridge 0.507 to 0.613.
     - Same test wines and same training size (each window in 3 folds, 3 seeds; earlier wines only against wines drawn
       from all positions): LightGBM 0.5455 against 0.5290 pooled over the nine windows (+0.017, +3.1%) and worse in
       every window (+0.009 to +0.026); ridge 0.5485 against 0.5442 (+0.004). Three wider windows give +0.023 for
       LightGBM. Without the 98 rows of issue 1's near-copies the LightGBM gap is +0.014 (0.5479 against 0.5337).
   * **Effect on the task:** a random split trains on wines entered next to the test wines, graded in the same weeks
     and close in alcohol and acidity, which a body grading new wines does not have.
   * **Consistency:** a raw file order kept as time without a timestamp follows seismic_bumps and california[^3b]; if
     the order is time, the density precision of issue 2 marks a period.
   * **Unknown:** whether the file order is the order of entry; Cortez et al. or the CVRVV would settle it.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, forced from temporal (implemented) | 3 x 3 random folds; the definition gets the tag `ForcedIIDFromTemporal` and a `Time basis:` line: the file order is the likely entry order, not counted as time because the source does not document it, and a split by position costs +0.017 MAE (LightGBM, 3%) at equal training size | rests only on what the source documents | trains on wines graded alongside the test wines; a measured cost in every window, so the order, if it is time, does not show a stationary relation |
     | B | Nine windows by file position | a time key from each row's share of its colour file; the newest half in nine windows of 295 wines, each trained on all earlier wines (50% to 94%) | tests later wines, as the certification body meets them; keeps the raw file order as time, as seismic_bumps and california do | the time rests on an undocumented file order and on equal pace in both files |

   * **Recommendation:** B: the two files share their pattern along the file far beyond chance, which only a common
     order of entry explains well, and leaving it unused costs LightGBM 3% in every window. If you want the order
     documented before it counts as time, A with that reason, forced since no usable time is then left. **Decision:**
     A or B?

   **Notes for the AI:** on B, in `_clean` give each colour file `file_position = np.arange(len(df)) / len(df)` before
   the concatenation, compute the exact-copy filter over the original columns only (`df.duplicated(subset=[all but
   file_position])`, keep first), and declare `Temporal(on="file_position", splits=TemporalSplits(window=295,
   unit="rows", n_windows=9))`; `file_position` is the time column and, as in the other temporal tasks, a feature;
   `split`, `fit_reason` and `splits_comment` say the order is inferred and why (the shared pattern, the precision
   switch, the adjacent copies); record `required_split` Temporal, tag `Non-IID (Temporal)`, and the tags `Samples:
   Over Time` and `Time: Dated`; `dataset check`. On A, `data_tags = ("ForcedIIDFromTemporal",)`, the record gets the
   tag `Samples: Over Time` without `Time: Dated` (the order not counted as a recoverable time), and the curation
   bullet on the IID split ends with `- Time basis: ForcedIIDFromTemporal: the wines arrived May 2004 to February 2007, and the raw file order is very likely the
   order of entry (both colour files share the grade, alcohol and acidity pattern along the file, r = 0.78 for the
   grade at 10 bins); not split by file position, because the source does not document the order; nine windows by
   position cost +0.017 MAE at equal training size (untuned LightGBM 0.546 against 0.529; ridge +0.004).` The frame
   has no date column, so no warning to accept. Results: Slurm job 1365901.

   [^3a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record's collection
     facts and, where one fits, the definition's use-case prototype with its `Time basis:` line. **SPLIT-8** (Must): a
     task temporal by its use case whose release cannot give the windows (dates lost, too few periods) ships in the
     closest regime, tagged as forced from temporal. **SPLIT-14** (Must): at least 3 windows,
     none training on less than half of the data. **SPLIT-15** (Should): as many windows as a random split of that
     size gets folds.
   [^3b]: **SPLIT-22** (Should): the raw file order can be the time order without a timestamp; keep it (seismic_bumps,
     california).

   **Answer (AI, 2026-11-06):** The record's collection facts no longer change with the option.

   - You accepted "Tell dated time from an inferred order in the `Time:` fact?": a record's collection facts follow the
     evidence, never the split option chosen[^3t].
   - The record now carries `Samples: Over Time` and `Time: Inferred`: the file position is an order that tracks time,
     without a calendar. It stays under A and under B, so the notes' record edits (`Time: Dated` on B, no time fact on
     A) drop out; the choice between A and B is unchanged.

   [^3t]: **SPLIT-32** (Should): the collection facts are true whatever task is built on the source and do not change
     with the split a definition chooses; `Time: Inferred` when only an order that tracks time survives, with no
     calendar.

   **Andrej (2026-11-12, discuss):** What could be alternatives what the file order means? Give me a table trying to
   argue for different versions of what the file order means

   **Answer (AI, 2026-11-12):** of six readings, the data rule out a shuffled file and a file sorted by one of its
   columns; of the rest, only the order of entry (time) explains the three things both colour files share: density's
   fifth decimal comes and goes at the same places in both, a common drift with a wave of about a year, and a cost
   that comes mostly from training on earlier wines only.

   | Measurement along the raw UCI file (copies included) | Red, 1,599 rows | White, 4,898 rows | Same file shuffled |
   |---|---|---|---|
   | Neighbour correlation (lag 1): grade; highest column | 0.14; 0.36 | 0.17; 0.28 | at most 0.08 |
   | The same after removing the trend: lag 1; lag 10 | 0.04 to 0.17; about 0 | 0.11 to 0.17; about 0 | about 0 |
   | Variance explained by 20 position bins, highest column | 31% (density) | 15% (fixed acidity) | at most 2% |
   | Neighbours in ascending order, any column; longest ascending run | 52-57%; 7 to 16 rows | 53-57%; 8 to 25 rows | 50% plus ties |
   | Runs of equal grade | 885 | 2,878 | 1,029; 3,311 |
   | Repeated rows within 17 rows of their earlier copy | 240 of 240 | 925 of 937 | 2.1%; 0.7% of pairs |
   | Density written with 5 decimals | none before 12%, a burst at 12-20%, none at 35-46%, 82% from 46% on | none before 14%, a burst at 14-20%, almost none at 33-46%, 83% from 46% on | |
   | Period of a wave on top of the trend (grade, alcohol, citric acid) | 40-42% of the file | 36-46% | no wave above chance |

   | Reading of the order | For | Against | For the split |
   |---|---|---|---|
   | 1. Order of entry in the CVRVV's iLab system (about the request date) | both colours drift alike (bin means r = 0.65 to 0.91 for 8 of 12 columns, grade 0.78); the density precision changes at the same places in both files, as a change in the lab's recording would; a wave of 36-46% of the file is 12 to 15 months if the 33 months are spread evenly, like a vintage; iLab "manages the process of wine sample testing from producer requests" (Cortez et al. 2009, Sec. 2.1) | no date or sample number ships; the paper never says the order was kept through the export and the pivot to one row per sample; equal pace in both files is assumed | later wines: windows by position (B) |
   | 2. A producer's request entered together, within that order | repeated rows sit 1 to 21 rows from their copy; issue 4's 111 pairs analysed twice side by side; neighbours alike for 5 to 10 rows only | explains the short range only, not the drift both colours share | adds to 1: windows keep a request together; a random split needs issue 4's grouping |
   | 3. Sorted by producer (or a sample code that starts with the producer), not by time | the short-range likeness | a recording change in time would then scatter over the file, not fall in two stretches at the same places in both files; likeness dies within 10 rows, not over producer-sized blocks; the colours would align only if every producer sent red and white in the same share | grouped by producer; windows would test new producers, not later wines |
   | 4. Sorted by one of the file's columns | none | no column is sorted (first table) | random; windows would extrapolate that column |
   | 5. Sorted by an attribute removed for privacy (grape, brand, price) | would give blocks of alike wines | as 3, and a sort gives no repeating wave | random or grouped; windows would test unseen kinds of wine |
   | 6. Shuffled or arbitrary | the paper scores random 5-fold CV and never uses the order | neighbours correlate, grades run, position explains up to 31% (first table) | random |

   | Training wines for the same test wines (nine windows of the newest half, equal size, 3 folds x 3 seeds; Slurm job 1380067) | LightGBM MAE | Ridge MAE |
   |---|---|---|
   | Random, the test wines' neighbours included (the shipped regime) | 0.528 | 0.544 |
   | Outside the window, before and after it | 0.535 | 0.545 |
   | Before the window only | 0.546 | 0.549 |

   - Losing the neighbours costs LightGBM 0.006 (worse in 7 of 9 windows): readings 1 and 2.
   - Losing the later side costs 0.011 more (worse in 6 of the 8 windows that have later wines): earlier wines predict
     a window worse than wines from both sides, as drift in time does; under a sort by producer (3) both sides would be
     equally new.
   - The source settles nothing: Cortez et al. give the period and the iLab export, not the row order, and the UCI
     notes are silent; only the CVRVV's sample numbers would.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | a | Random split, forced from temporal (the issue's A, implemented) | as in the issue | rests only on what the source writes | readings 1 and 2, the ones the data leave, both put wines of the same weeks on both sides |
   | b | Nine windows by file position (the issue's B) | as in the issue | the reading that explains every shared fact; also keeps reading 2's requests together | the order is inferred, not documented, and equal pace is assumed |

   **Recommendation:** b (the issue's B): the data leave only readings 1 and 2, and both call for wines entered
   together to stay on one side; the windows also test what reading 1 predicts, later wines[^3u]. **Decision:** A or
   B?

   **Notes for the AI:** measured on a fresh download of the UCI zip (files identical to the earlier copy).

   [^3u]: **SPLIT-22** (Should): the raw file order can be the time order without a timestamp; keep it.
     **SPLIT-32** (Should): how the data was collected is information for the split.

   **Andrej (2026-11-13, discuss):** Reply (b): Nine windows by file position (the issue's B). Document this very well
   since it is a judgement call.

   **Resolved (2026-11-13, Andrej):** B: nine windows by file position.
   - `_clean` gives each colour file `file_position` (row number over file length) before the concatenation; the
     exact-copy filter ignores it (keep first), so the frame stays 5,320 wines.
   - `Temporal(on="file_position", splits=TemporalSplits(window=295, unit="rows", n_windows=9), feature=False)`: nine
     windows of 295 wines over the newest half, each trained on all earlier wines (2,665 to 5,025, 50% to 94%).
   - The position is no model input, a change from the notes (written before `feature=False` existed): a row's place
     in an exported file is not something the certification body holds when it grades a wine.
   - Documented as a judgement call: a curation bullet names the six readings weighed, the evidence for entry order
     (density's 5-decimal stretches shared by both files, the common drift with a yearly wave, MAE 0.528 random /
     0.535 neighbours left out / 0.546 earlier only), that the position is no date and assumes a steady pace, and what
     would overturn it (CVRVV sample numbers or dates showing another order). `splits_comment`, the task summary's
     `split`, `changes` and `fit_reason` rewritten; the deduplication bullet no longer says the split stays IID.
   - Record: `required_split` `Temporal (NON-IID)`, tag `Non-IID (Temporal)`, CC line. The collection facts
     (`Samples: Over Time`, `Time: Inferred`) were already set, so nothing goes to PR #50.
   - `dataset check`: 0 errors, 0 warnings, 0 info; README regenerated (12 features, `time_is_feature: false`); not
     rebuilt. Issue 4's recommendation under B is to keep its A (the windows hold the pairs together, 1 of 2,655 test
     rows); it stays open for your mark.

4. **Group the wines analysed twice, pairs of near-identical chemistry entered next to each other?**

   * **Problem:**
     - Besides issue 1's copies, 111 pairs of wines of one colour share 5 to 8 of the 11 lab values exactly, differ in the rest by small amounts, and sit at most 17 rows apart in the raw file (most often next to each other), far more often than chance or nearby wines allow.
     - They read as one wine analysed and graded twice, each time with its own grade, which agrees in 76% of the pairs against 45% for a wine and its nearest wine in chemistry elsewhere in the file.
     - Under the random split 2.5% to 2.8% of the test rows have such a partner in training: group each pair into one fold, or keep the split as it is?
   * **Background:**
     - Issue 1's copies carry one value retyped and always the same grade. These pairs differ in several values by
       small amounts (total sulphur dioxide 158 against 157, chlorides 0.172 against 0.173, sulphates 0.36 against
       0.34) and in the grade in 27 of 111 pairs, so each row is an analysis and a tasting of its own: two samples
       of one wine, or two lots of one producer's wine, submitted together.
     - Several observations of one unit, each with its own label, are grouped rather than dropped, on a key rebuilt
       from the data when no id records the unit[^4a]. Here the key is: same colour, at least 5 of the 11 values
       equal, at most 17 rows apart in the raw file. It gives 103 groups (99 pairs, 3 of three wines, 1 of four),
       211 rows (4.0%; 159 white, 52 red).
   * **Experiments:** the v0.2 frame after issue 1's drop (5,271 rows), counted without a model:
     - Chance: with each lab value shuffled within colour (20 draws), 12.8 pairs per draw share 5 to 8 values, and
       0.85% of the pairs of one colour sit within 17 rows, so about 0.1 such pairs are expected against 111.
     - Nearby wines: within 17 rows, 15.5 of every 10,000 pairs share 5 to 8 values; 18 to 50 rows apart, 0.21; so
       wines entered near each other being alike explains about 2 of the pairs.
     - Grade: the same in 84 of 111 pairs, one point apart in 26, two in 1. A wine and its nearest wine in
       standardised chemistry more than 17 rows away share the grade in 45% of cases; random pairs of one colour in
       33%.
     - Overlap: under random 3-fold splits (3 seeds) 2.5%, 2.8% and 2.7% of the test rows have such a partner in
       training. Under issue 3's nine windows by file position, 1 of 2,655 test rows, as the pairs sit side by side.
   * **Effect on the task:** under the random split a test wine's second analysis in training gives its grade away
     more often than its chemistry does; the certification body grades both samples in one session, without either
     grade.
   * **Consistency:** grouping on a link rebuilt from the recording follows concrete_compressive_strength (a mix
     tested at several ages) and frempl_french_motor_personal_line (a policy's records joined day to day); it departs
     from issue 1's drop because each row here carries its own grade[^4b].
   * **Unknown:** whether a pair is one wine sampled twice or two lots of one wine; the CVRVV's sample ids would
     settle it, and either way the second grade is not known when the first sample is graded.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep (implemented) | random split as now | no key built from the features | 2.5% to 2.8% of test rows have a second analysis of their wine in training |
     | B | Group the pairs | a `wine_group` key from the link (103 groups of 2 to 4 wines, 211 rows); folds keep a group together | no wine's second analysis across the split; every row and grade kept | the key is rebuilt from the values and the file order, so it is a judgement call |

   * **Recommendation:** B while the split stays random (issue 3, A): the link is far above chance, even against
     nearby wines, and carries the grade well beyond what chemistry predicts. If issue 3 splits by file position (B),
     keep A here: the windows already hold the pairs together (1 of 2,655 test rows). **Decision:** group the pairs
     (B) or keep (A)?

   **Notes for the AI:** on B, in `_clean` after issue 1's drop: keep each colour file's raw row number before the
   concatenation; per colour, link pairs with at least 5 of the 11 lab values equal and at most 17 raw rows apart;
   connected components as `wine_group` (single wines their own group); declare `Grouping(on="wine_group",
   labels="per_sample", prediction_unit="row", context="none")`; a curation bullet with the counts (111 pairs, 103
   groups, 211 rows; same grade 76% against 45%; about 0.1 pairs by chance); task summary `split`; record
   `required_split`; `dataset check`; CHANGELOG. The 49 copies of issue 1 are a subset of the same pattern (9 or more
   values equal, 1 to 17 rows apart); under issue 1's C they would join these groups.

   [^4a]: **LEAK-41** (Must; draft PR #62): repeats of a unit the data does not record get one of four verdicts; an
     entity fix groups several observations of one unit that each carry their own label, and a key rebuilt from the
     features is a discussion point, decided by how certain the evidence is. **LEAK-42** (Should; draft PR #62):
     three tests set the verdict: a link far above a chance rate that keeps the data's structure, a label that
     travels with the link beyond what the shared features predict, and an order. **SPLIT-24** (Must; draft PR #62):
     group on a true group id, or on one constructed from the data exactly or by a calibrated link whose match rule
     comes from how the data were recorded and whose chance rate shows most links are real; never on a
     similarity-threshold cluster.
   [^4b]: **SPLIT-24** cases: concrete_compressive_strength (428 mixes behind 1,030 tests),
     frempl_french_motor_personal_line (a calibrated link, 68,857 policy components). **LEAK-19** (Should): exact
     copies with the same label are dropped rather than grouped.

   **Andrej (2026-11-13, discuss):** Now with a temporal split, is the problem solved?

   **Answer (AI, 2026-11-13):** Yes: under the nine windows 2 of 2,655 test rows have the wine's second analysis in
   training, against 2.5% to 2.8% under random splits.

   | Pairs analysed twice, 5,320 wines, no model | Random 3-fold (3 seeds) | Nine windows by file position |
   |---|---|---|
   | Pairs (same colour, 5 to 8 of 11 values equal, at most 17 rows apart) | 115 | 115 |
   | Test rows whose partner is in training | 2.5% to 2.8% | 2 of 2,655 (0.08%), in the two oldest windows |
   | Pairs with both rows in one test window | | 44 |

   * 115 rather than 111: this frame still holds issue 1's 49 copies, and 4 pairs involve them.
   * The two rows of a pair sit side by side in the file, so the windows keep them on one side, as the issue's
     recommendation expected.
   * Pairs inside one test window are two analyses with their own grades, scored as two wines; no grade crosses the
     split.
   * Status: solved (2 rows left).

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | A | Keep (implemented) | the windows as they are | no key rebuilt from the values; the windows already hold the pairs together | 2 test rows keep a partner in training |
   | B | Group the pairs inside the windows | a `wine_group` key; a group stays on one side of each cut | the last 2 rows covered | a key rebuilt from the values and the file order, a judgement call, for 2 rows |

   **Recommendation:** A. **Decision:** keep (A) or group (B)?

   **Notes for the AI:** same script as issue 1's answer of 2026-11-13.

   **Andrej (2026-11-13, re: answer of 2026-11-13):** Reply (A): Keep

   **Resolved (2026-11-13, Andrej):** A: kept; no `wine_group` key. The nine windows by file position (issue 3, B)
   hold the pairs analysed twice on one side (2 of 2,655 test rows keep a partner in training). No change to
   dataset.py; record CC line.

## Reference

Modeling wine preferences by data mining from physicochemical properties
By P. Cortez, A. Cerdeira, Fernando Almeida, Telmo Matos, J. Reis. 2009

Published in Decision Support Systems
