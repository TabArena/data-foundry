---
unique_name: aps_failure
name: APSFailure
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
priority: 2
decision_markers:
- Anonymized
tags:
- Non-IID (Grouped)
- 'Samples: Over Time'
- 'Time: Lost'
- 'Entities: Recur'
original_source: Other
year: '2016'
domain: industry & manufacturing
required_split:
- Grouped (NON-IID)
problem_type: Binary Classification
source_links:
- https://web.archive.org/web/20161011/http://ida2016.blogs.dsv.su.se/
- https://www.openml.org/search?type=data&id=41138
- https://doi.org/10.24432/C5V60Q
notebook_path: datasets/beyond_iid/old_iid/aps_failure/aps_failure.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/aps_failure/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Comes with a cost matrix. Originally comes with custom train/test split. Last 16k are test. Strongly imbalanced task. Might originally be time-series. Error very close to zero on TabRepo - might indicate a leak; data from daily usage indicates temporal relationship as well and potentailly future failures per seasons; data contains histograms; missing values must be nan-ed

Update: Error is close to zero because it is trivial to classify the negative cases due to the high class imbalance. However meaningful learning is possible. One paper about challenge: https://link.springer.com/chapter/10.1007/978-3-319-46349-0_33. D

Potential issue: maybe temporal, heavily preprocssed

Lennart: verify split

Andrej: need to verify that original provided split was also random

CC (2026-10-06, Lennart): Kept in TabArena v0.2 after the task-probe review (flag `one_feature`: `ck_000` alone +0.944 skill against +0.982 for LightGBM). Not trivial: the best single feature chosen on each split's training side (`ci_000` or `aa_000`) ranks the test rows at ROC AUC 0.970, below all 20 BeyondArena configurations (TabPFN-3 0.994 to a default linear model 0.988) on every fold; the methods cut the remaining error (1 - AUC) from 0.031 to 0.006. The flag comes from AUC near its ceiling, where the methods differ in the third decimal; the original challenge scored a cost (500 per missed failure, 10 per false alarm). Still open from the earlier triage: the source ships a train/test split (the last 16,000 readings) that may be temporal; there are no timestamps to check it, so the random folds stay.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: source cost_matrix {"labels": ["neg", "pos"], "matrix": [[0, 10], [500, 0]], "prediction": "proba"} — Total cost = Cost_1 * #false positives + Cost_2 * #false negatives (IDA 2016 Industrial Challenge) (https://web.archive.org/web/20161011/http://ida2016.blogs.dsv.su.se/ ; UCI https://doi.org/10.24432/C5V60Q (aps_failure_description.txt)).

CC (2026-10-21, Lennart): the declared metric stays as it is (`cost_matrix`: a false alarm costs 10, a missed failure 500, as the IDA 2016 challenge scored; cross-dataset item "Metrics still to settle").

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `scania_component_x` (TBD -> Yes, priority 4). Each is screened in its own record; this record's verdict stays the curator's.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship after keeping one row per truck: 30% of rows have a near copy (140-169 of 170 counters equal) that always shares the label, and the random split puts one in training for 21% of test rows. Priority 2: gap 0, use case 0, source 1, shape 1, risk -1.

CC (2026-11-10, Andrej): ok (review issue 2, A): the random split keeps `ForcedIIDFromTemporal`, now with its `Time basis:` line in `curation_comments`.
- Failures are undated, and the challenge's two files are not shown to be two periods (near copies across them go either way, 2,237 against 2,220 pairs).
- `fit_reason` and the split summary no longer call the challenge's test rows later readings.

CC (2026-11-11, Andrej): record field set from the definition (review page field mark): `domain` industry & manufacturing.

CC (2026-11-12, Andrej): copies of one read-out dropped and the same truck held out together (BeyondArena v0.2 review page, issue 1, cg); the input data changed: 76,000 to 63,937 rows, a random split to one by truck.

**Changes made:**

1. **Problem:** 30% of the rows have a near copy, another row equal in at least 140 of the 170 counters (106 non-zero values equal at the median, one differs, where an unrelated row matches at most about 19), always with the same label; a random split put such a copy in training for 21% of the test rows, so a model could recognise the truck instead of judging its counters. **Change:** one row of each set of copies stays, the first in file order: 12,063 rows go (115 failures), 63,937 rows with 1,260 failures remain (failure share 1.81% to 1.97%).
2. **Problem:** looser links (60 to 139 of the 170 counters equal, always the same label) are probably the same truck read again, not copies of one read-out. **Change:** they stay and are held out together: the split groups on these clusters, 61,466 trucks (2,200 with 2 to 5 rows), so 0.05% of the test rows keep a linked row in training instead of 25% (untuned LightGBM cost per row 1.145 on random folds of all rows, 1.625 split by truck). The record's split is `Grouped (NON-IID)` with the tag `Non-IID (Grouped)`, and the definition's tag for a forced split of undated data becomes the grouped one (`ForcedGroupedFromTemporal`).

**Problems found, not changed:**

- No time order hides in the copies: the one counter that changes between them, `bx_000`, is a usage counter that moves by a small step either way, so a split by time cannot be rebuilt (issue 2 stands).
- 368 rows with 100 or more blank counters agree with each other on blanks only: look-alikes, not copies, kept.

## Review

**Outcome:** added. The IDA 2016 Industrial Challenge (Scania, via UCI): 76,000 heavy trucks with a component failure,
170 anonymised operating counters and histogram bins each, and whether the failure is in one component of the air
pressure system (1,375 trucks, 1.8%), scored by the challenge's cost (10 per needless check, 500 per missed failure).
The AI recommends shipping it after one change (issue 1). Reviewed on 2026-11-04 without a review panel, from the
gathered evidence (the record, model runs on the TabArena v0.1 task of the same 76,000 rows) and two checks of
today on the UCI files. Validity: a workshop's call whether to check the air pressure system, an approximate fit (no
dates; when the counters were read relative to the failure is not stated); the challenge's split is replaced by a forced
grouped one, by truck (issue 1). Our experiments found that the same truck appears more than once, and today's checks confirm it on the v0.2
rows: 30% of the rows have a near copy that agrees on 140 to 169 of the 170 counters and always carries the same label,
and a random split puts such a copy on the training side for 21% of the test rows (issue 1). Value: the `one_feature`
flag is settled (the best single counter, ROC AUC 0.970, stays below every tuned method; Lennart, 2026-10-06); on the
shipped splits the benchmark methods spread from 1 - AUC 0.0048 to 0.0085 at the median and 0.010 to 0.013 for linear
models. Quality: nothing open beyond issue 1. Weighed: an industrial challenge with a stated cost +, methods that
separate +, repeated trucks across the split -, anonymised counters and no dates -; a newer Scania release
(`scania_component_x`) is screened in its own record.

**Main points:** Applied on 2026-11-12 (issue 1, cg): one row per copied read-out (63,937 of 76,000 rows), then a
split by truck (61,466 trucks from the links at 60 counters), so 0.05% of the test rows keep a linked row in training
instead of 25%; the forced tag is now the grouped one. `dataset check` 0 errors; not rebuilt. Record `domain` set
(2026-11-11). Nothing open.

**Record judgment:** valid task; the split, damaged by copies of one truck, is repaired (issue 1). The description file in UCI's zip carries a GNU GPL v3 notice from
Scania CV AB, while the definition states CC BY 4.0, UCI's licence for the page; the licence line should name both.

**Issues for Andrej:**

1. **Keep one row per truck, dropping the near copies?**

   * **Problem:**
     - 22,889 rows (30.1%) have a near copy: another row equal in 140 to 169 of the 170 counters, most often in all
       but `bx_000`, and in 13,409 such pairs the two rows always carry the same label, failures included.
     - A random split places a copy on the training side for 21.1% of the test rows, 148 of the 1,375 failures among
       them, so a model can recognise the truck instead of judging its counters.
     - Keep the rows, drop the exact copies only, or keep one row per truck?
   * **Background:** the near copies look like the same truck read more than once: in 8,326 pairs a single counter
     differs (in one example `bx_000` reads 21,772 and 24,060, everything else equal), and looser pairs differ in a few
     more counters. 4,458 pairs have one row in the challenge's training file and one in its test file, so the
     challenge's own split had the problem too. A repeated entity leaks its label across a split even when the rows
     differ, and is kept once when the use case acts once per entity, here once per failed truck[^1a]; near-exact
     copies over many columns are dropped rather than grouped[^1b], and a group key built from a similarity threshold
     is not allowed[^1c].
   * **Experiments:** today's checks, untuned LightGBM on 3 stratified folds of all 76,000 rows:
     - Clusters of near copies: 10,826 of 2 to 6 rows, none with both labels; label agreement stays 100% down to 100
       equal cells, so the cut at 140 is not fitted to the labels. If failures paired at random, 1.8% of a failure's
       copies would be failures; here 133 of 133 pairs are.
     - Failures with a copy are missed at the challenge's cost threshold 2.8% of the time under the random split and
       11.3% when their copies are held out together, the rate of the other failures (11.4% to 12.0%).
     - Mean cost per truck: random split 0.982 (ROC AUC 0.9916); copies held out together 1.142 (0.9897); one row per
       cluster, 63,937 rows with 1,260 failures, 1.223 (0.9899).
     - The exact key "all counters but `bx_000`" joins 15,239 rows into 7,400 groups (97 failures), 62% of the pairs;
       grouping on it still leaves a looser copy on the training side for 7.8% of the test rows.
   * **Effect on the task:** a workshop meets each failed truck once; with its copy in training the benchmark rewards
     remembering a truck, which favours methods that retrieve near neighbours (LimiX-2 uses it).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep all rows (implemented) | 76,000 rows, random split | the challenge's rows as published | 21% of the test rows find their own truck's copy in training |
     | B | Drop the exact copies on all counters but `bx_000` | one row per group of the exact key; 7,839 rows go | an exact rule, no threshold | looser copies stay for about 8% of the test rows |
     | C | Keep one row per near-copy cluster | rows equal in at least 140 of 170 counters are one truck; one row each stays, 12,063 rows (115 failures) go | no truck on both sides; one row per failed truck, the unit the workshop acts on | the cut at 140 counters is ours; which reading of a truck stays is arbitrary without dates |

   * **Recommendation:** C: the copies always share the label, so they are one truck's readings, and one row per
     truck is the unit of the decision. **Decision:** keep all rows (A), drop the exact copies (B), or keep one row per
     truck (C)?

   **Notes for the AI:** on C, in `_clean` (after the concat): candidate pairs share a value held by at most 5 rows
   in some column; a pair whose 170 cells agree in at least 140 (two missing cells count as equal) is joined; keep the
   first row of each connected cluster in file order (training file first). Expected: 63,937 rows, 1,260 failures.
   Write the counts and the 100% label agreement into `curation_comments`, re-run `dataset check` and the probes, and
   name the challenge files' shared trucks in the notes. The check script of 2026-11-04 is the reference
   implementation (pairs from rare values, then exact agreement counts).

   [^1a]: **LEAK-17** (Must): repeated entities in different rows leak the target across the split even when the
     rows differ: keep one row per entity when the use case is that row, or group.
   [^1b]: **LEAK-18** (Should): many degrees of freedom and an exact match point to a collection artefact: drop it and
     give the share. **LEAK-19** (Should): exact copies with the same label are dropped rather than grouped on the
     duplicate key.
   [^1c]: **SPLIT-24** (Must): group on a true group id or one constructed exactly from the data, never on a
     similarity-threshold cluster.

   **Answer (AI, 2026-11-06):** the time framing, from today's review of how each dataset's data arrives.

   * The copies are not one truck read at two moments. In today's re-run (13,450 near-copy pairs, the same rule),
     the counter that behaves like operating time, `aa_000`, differs in only 71 pairs, while `bx_000` differs in
     13,283; a truck read months apart would show more operating time.
   * Across the challenge's two files (4,467 pairs), the copy in the test file has the larger differing counters in
     2,237 pairs and the smaller in 2,220, so the test file is not a later reading of the same trucks.
   * So option C's "first row in file order" drops no later or earlier reading in any sense the data shows, and the
     time basis (issue 2) does not change this issue: a truck's outcome on both sides of a forced random split is
     the leak such a split is tested for[^1d].

   [^1d]: **SPLIT-8** (Must): a split forced from temporal gets a leak test across the split: does a row share its
     outcome, its unit's outcome or its period's outcome with the other side.

   **Answer (AI, 2026-11-06):** Under the new entity-leakage rules the near copies are one truck's read-out copied,
   and the cut at 140 counters misses looser copies: keep one row per truck over every link the data shows?

   * **Problem:**
     - Option C joins two rows when they share at least 5 values that are rare in their column and agree on 140 of the 170 counters, and the rare values carry the link: about 30,000 pairs of nearly blank records also agree on 140 cells, on blanks alone.
     - Rows that share those rare values but agree on only 60 to 139 counters behave like the close copies: the label agrees in every pair, 133 failure pairs among them, and most share the operating counter `aa_000`.
     - After C, 5.1% of the test rows still have such a looser copy in training, and one row per cluster of every link at 60 counters or more leaves 0.05%.
   * **Verdict: entity fix, copies of one record, one row per truck**[^1e]:
     - Is the link real? With every counter shuffled within its class (10 draws), no pair of rows shares 5 rare values
       and none agrees on more than 68 counters; in the data 17,461 pairs share 5 rare values, 13,409 of them agreeing
       on 140 counters or more.
     - Does the label travel with the link? All 133 pairs with a failure at 140 counters or more are pairs of two
       failures. A model that never sees a truck's copies gives the partner of a failure a mean failure probability of
       0.70 from the partner's own counters, so the counters predict about 93 of these 133 partners, not all.
     - Is there an order? No: `aa_000` is equal in 13,340 of the 13,409 pairs, and the two rows sit as far apart in
       the file as random rows (median 17,611 rows against 17,602): one read-out copied with a few counters changed,
       not a later reading.
   * **The looser links**, among pairs that share 5 rare values, by how many counters agree:
     - 100 to 139: 2,769 pairs, the label the same in all (69 failure pairs), `aa_000` equal in 93%.
     - 60 to 99: 1,197 pairs, the label the same in all (64 failure pairs), `aa_000` equal in 84%.
     - Below 60: 86 pairs, one with two labels, `aa_000` equal in 67%; left apart.
   * **Blank records:** 368 rows have 100 or more of the 170 counters blank (4 failures). They agree with each other on
     blanks only, share no rare value, and stay: look-alikes, not copies.
   * **What the drop does to the target:**
     - c (140 counters): 12,063 rows go (15.9%): 115 failures (8.4% of them) and 11,948 other trucks (16.0%); the
       failure share moves from 1.81% to 1.97%.
     - d (60 counters): 14,476 rows go (19.0%): 194 failures (14.1%) and 14,282 other trucks (19.1%); the failure
       share moves from 1.81% to 1.92%.
     - Does the target still stand for the use case? The AI reads yes: the label means the same, the failure share
       moves by about a tenth of a point, and a workshop meets each failed truck once.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep all rows (implemented) | 76,000 rows, random split | the challenge's rows as published | 21% of test rows find a copy in training, 24% with copies at 100 counters or more |
     | b | Drop the exact copies on all counters but `bx_000` | 7,839 rows go | an exact rule | 7.8% of test rows keep a looser copy in training |
     | c | One row per cluster at 140 counters | 63,937 rows, 1,260 failures | the closest copies only; 15.9% of rows go | 5.1% of test rows keep a looser copy in training |
     | d | One row per cluster at 60 counters | pairs sharing 5 rare values and 60 counters or more; 61,524 rows, 1,181 failures | 0.05% of test rows keep a copy in training; every band joined has the same label in every pair | 19.0% of rows go; the cut sits where the label stops agreeing in every pair |

   * **Recommendation:** d: the looser links pass the same tests as the close ones (none by chance, the same label in
     every pair, mostly the same operating counter), so they are the same read-outs, and one row per truck should
     cover them[^1f]; c stays the fallback if a cut placed by the label agreement is a step too far. **Decision:** d,
     c, b, or keep a?

   **Notes for the AI:** on d, in `_clean` (after the concat): candidate pairs share at least 5 values held by 2 to 5
   rows in their column (the issue's notes say "a value"; the counts above and there come from at least 5 such
   values); a pair whose 170 cells agree in at least 60 (two missing cells count as equal) is joined; keep the first
   row of each connected cluster in file order (training file first). Expected: 12,112 clusters, 61,524 rows, 1,181
   failures. On c, the issue's notes (63,937 rows, 1,260 failures). Write the chance rate, the label test, the blank
   records and the class shares into `curation_comments`. The checks covered the nulls, the label baseline, the order,
   the drop at 140, the bands, `aa_000`, the cuts and the blank records. The null shuffles each
   counter on its own, so it breaks columns that hold one value within a row (`bb_000`, `bu_000`, `bv_000` and
   `cq_000` are equal in 99.7% of the training file's rows), where one shared rare value counts several times; the
   label and `aa_000` tests do not depend on that.

   [^1e]: **LEAK-42** (Must; draft PR #62): repeats of a unit the data does not record get one of four verdicts:
     natural, entity fix, temporal fix or not recoverable; an entity fix takes copies of one record down to one row
     per unit, and every drop gives the label shares before and after and asks whether the target still stands.
     **LEAK-43** (Should; draft PR #62): three tests set the verdict: a link far above a chance rate that keeps the
     data's structure, a label that travels with the link beyond what the shared features predict, and an order.
   [^1f]: **SPLIT-24** (Must; draft PR #62): a calibrated link takes its match rule from how the data were recorded
     (the same counters read again), never from the score, and a chance rate shows that most of its links are real;
     whether it holds is the curator's call. **LEAK-18** (Should): a match on all but one or two of many values is a
     calibrated link, and the evidence that may drop such a row may also group it.

   **Andrej (2026-11-10, discuss):** Wait, I don't get it, isn't the actual issue that there should be a temporal
   component that is not considered. Try to reconstruct it before dropping any columns.

   **Answer (AI, 2026-11-10):** No time order can be rebuilt: the copies are one read-out repeated with a counter
   nudged, not one truck read at different times. No option drops columns; c and d drop rows.

   * Rechecked directly: `aa_000` differs in 69 of 13,409 pairs at 140 counters (0.5%) and in 446 of 17,375 at 60
     (2.6%); where it differs at 140, the two values are thousands of times apart, not an increment of operating time.
   * A pair differs in 1 cell at the median (17 at the 90th percentile), mostly `bx_000`, which moves by under 0.1% at
     the median (1.7% at the 90th percentile). A later read-out would raise every cumulative counter and histogram bin.
   * Chains: 656 of 1,067 clusters of 3 or more rows can be ordered so that no counter falls, mostly because a single
     counter differs; that order agrees with file order in 6,652 of 13,383 pairs, chance.
   * The failure does not come at the newest read-out: every copy carries the same label (100%), so the label belongs to
     the truck's failure, not to a moment.
   * Beyond the copies: 16% of 5,000 sampled rows have a partner higher in every counter, with `aa_000` up to 20% higher,
     but the 307 such pairs with fewer than 60 equal counters share the label in 93.5% of cases, against 96.5% for random
     pairs: bigger trucks, not later read-outs.
   * Splits, untuned LightGBM, challenge cost at its threshold (Slurm jobs 1377079 and 1377122):

     | Split | Mean cost per truck | ROC AUC | Failures with a copy missed |
     |---|---|---|---|
     | Random, 3 folds (implemented) | 0.932 | 0.9896 | 4.6% |
     | Per truck (clusters at 60 counters held out together) | 1.109 | 0.9880 | 12.4% |
     | Ordered along the chains (newest copy tested, older copies trained) | 0.590 | 0.9913 | 0.0% |

     A split along the chains puts each tested truck's own copies in training, so it leaks the most.

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep all rows (implemented) | 76,000 rows, random split | the rows as published | 21% of test rows find their truck's copy in training |
     | t | Split along the chains | test the newest copy of each truck | none found | not a time order (`aa_000` constant); every tested truck has its copy in training |
     | c | One row per cluster at 140 counters | 63,937 rows | closest copies only | 5.1% of test rows keep a looser copy |
     | d | One row per cluster at 60 counters | 61,524 rows, 1,181 failures | 0.05% of test rows keep a copy | 19.0% of rows go |

   * **Recommendation:** d, unchanged: no time component is hidden in the copies; the time question is issue 2 (no
     dates, forced tag). **Decision:** d, c, or keep a?

   **Andrej (2026-11-11, discuss):** Instead of dropping, why don't we make it a grouped split?

   **Answer (AI, 2026-11-11):** Grouping works, but no exact key reaches far enough. The exact keys cover under
   half of the copies, so a grouped split has to use the same near-copy clusters as d. On those clusters it scores
   like d.

   * Exact keys: "all counters but `bx_000`" gives 7,400 groups. Equal in all but any one counter gives 7,437. Both
     hold only 48% of the links at 60 counters or more, and 12% of the test rows keep a copy in training.
   * Group on the clusters at 60 counters: 0.05% of the test rows have a copy in training, the same as d. Cost per
     truck is 1.558 when each truck counts once and 1.557 for d, so the task is equally hard.
   * Grouped and unweighted, a truck with up to 6 copies counts up to 6 times in the test score: 1.491 against 1.557.
   * Rules: grouping on these clusters needs the calibrated link of draft PR #62. The current group-id rule bars
     similarity clusters. d uses the same clusters, so both depend on that link. The draft keeps copies of one record
     as one row and groups separate observations that each carry their own label. Here the copies differ in about one
     counter and always share the label.
   * Untuned LightGBM, 3 folds, 2 seeds, the challenge cost at its threshold (Slurm job 1378343):

     | Split | Rows | Test rows with a copy in training | Cost per truck | Cost, each truck once | ROC AUC |
     |---|---|---|---|---|---|
     | Random (implemented) | 76,000 | 25.2% | 1.145 | 1.338 | 0.9910 |
     | Grouped, exact key "all but `bx_000`" | 76,000 | 12.3% | 1.295 | 1.458 | 0.9898 |
     | Grouped, clusters at 140 counters | 76,000 | 5.2% | 1.418 | 1.541 | 0.9890 |
     | Grouped, clusters at 60 counters | 76,000 | 0.05% | 1.491 | 1.558 | 0.9885 |
     | d: one row per cluster at 60 counters | 61,524 | 0.05% | 1.557 | 1.557 | 0.9892 |

   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep all rows (implemented) | random split | the rows as published | 25% of test rows find a copy |
     | ge | Group on the exact key | groups of rows equal in all counters but `bx_000` | allowed by the current rules | 12% of test rows keep a copy |
     | g | Group on the clusters at 60 counters | all 76,000 rows, cluster id as the group | rows as published, no arbitrary pick of one copy | copied trucks count several times in the score; needs draft PR #62 |
     | d | One row per cluster at 60 counters | 61,524 rows | each truck counts once | 19% of rows go; needs draft PR #62 |

   * **Recommendation:** d. The copies are one record read again, so one row per truck matches the use case and
     weights each truck once. Choose g if keeping the published rows matters more. g and d differ only in that
     weighting. **Decision:** d, g, ge, or keep a?

   **Answer (AI, 2026-11-12):** How sure are we that the copies are the same truck, and can the one changing counter
   give the time order? Only the close copies are one record. The looser links are probably the same truck read again,
   and the changing counter is no clock.

   * **Certainty by band.** Counting only informative matches (equal, non-zero, not missing) and comparing with the
     best match a random row finds among the rows not linked to it (600 rows):

     | Counters equal | Pairs | Informative equal cells, median (bottom 10%) | Cells with two different values, median | Mixed labels |
     |---|---|---|---|---|
     | 140 to 170 | 13,409 | 106 (84) | 1 | 0 |
     | 100 to 139 | 2,769 | 59 (33) | 47 | 0 |
     | 60 to 99 | 1,197 | 32 (14) | 81 | 0 |
     | below 60 (not joined) | 86 | 18 (10) | 87 | 1 |
     | best unlinked match of a random row | 600 rows | 5 (99th percentile 19, max 76) | | |

     - 140 counters or more: one record copied. 106 real values match (102 in columns with over 1,000 distinct values)
       and one differs, where an unlinked row almost never matches more than 19. Zeros and blanks do not make the
       match.
     - 100 to 139: very likely the same truck. Even the bottom tenth (33) is above chance, but 47 cells differ, so the
       rows are not copies of one read-out.
     - 60 to 99: probably the same truck, not established. The bottom tenth (14) is inside the chance range and 81
       cells differ. The case rests on the label (64 of 64 failure pairs are two failures) and on `aa_000` (equal in
       84%). The answer of 2026-11-06 ("one read-out copied with a few counters changed") holds for the 140 band only.
     - One random row's best unlinked match agrees on 76 informative cells, a copy the pair finder missed: the 0.05%
       left after d is a lower bound.
   * **The changing counter is no clock.** Pairs that differ in exactly one cell:

     | Check | Result | If the copies were read at two times |
     |---|---|---|
     | Which counter changes | `bx_000` in 8,289 of 8,326 pairs | |
     | Size of the change | median 0.012%, 90th percentile 0.6% | |
     | Absolute change against the truck's `bx_000` level | Spearman −0.13 (the same size for small and large trucks) | grows with the truck's usage rate |
     | Copy in the challenge's test file larger | 1,419 against 1,344 of 2,763 pairs (chance) | mostly larger if the test file is later |
     | Labels | 0 of 8,289 pairs mixed (49 failure pairs) | could change near a failure |

     - Across trucks `bx_000` follows `aa_000` (Spearman 0.91), and the other counters predict it with R² 0.98: a
       cumulative usage counter, so its level dates a truck's age, not a calendar day.
     - The change is a small step of about fixed size in either direction: noise on one counter, or two read-outs
       moments apart. At best it orders the copies of one truck. That is the split along the chains of 2026-11-10, the
       one that leaks the most (cost 0.590 against 0.932), and a split on usage level is a covariate shift, not time.
       Issue 2 stands as decided.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep all rows (implemented) | random split | the rows as published | 25% of test rows find a copy |
     | c | One row per cluster at 140 counters | 63,937 rows; looser copies stay apart | rests only on near-certain copies | 5.1% of test rows keep a looser copy in training |
     | cg | c, then group on the clusters at 60 counters | 63,937 rows, the cluster id as the group | the drop rests on near-certain copies; the probable re-readings are grouped, the treatment the draft gives separate observations of one unit | not measured yet; needs draft PR #62 |
     | d | One row per cluster at 60 counters | 61,524 rows | each truck counts once | 2,413 of its 14,476 dropped rows rest on the label pattern more than on the values |
     | g | Group on the clusters at 60 counters | all 76,000 rows | the rows as published | copies count several times in the score |

   * **Recommendation:** cg, changed from d: drop only what is one record copied, and group what is probably the same
     truck read again. **Decision:** cg, c, d, g, or keep a?

   **Notes for the AI:** on cg, apply c's notes, then build the clusters at 60 counters on the kept rows (the 11-06
   notes on d) and split grouped on the cluster id; run the split table of 2026-11-11 for cg.

   **Andrej (2026-11-12, discuss):** Reply (cg): c, then group on the clusters at 60 counters

   **Resolved (2026-11-12, Andrej):** cg. One row per copied read-out (at least 140 counters equal, the first in file
   order), then a split by truck: 63,937 rows, 1,260 failures, 61,466 trucks (2,200 with 2 to 5 rows, none with two
   labels), `Grouping(on="truck", labels="per_group")`, stratified grouped 3 × 3 folds. The trucks are the clusters of
   the links at 60 counters found on the kept rows, as the notes say, and on all rows, so a link through a dropped copy
   still joins. A grouped split needs `ForcedGroupedFromTemporal` in place of issue 2's `ForcedIIDFromTemporal`; the
   `Time basis:` line, the task summary, `splits_comment` and curation notes are rewritten; record `Grouped (NON-IID)`,
   `Non-IID (Grouped)`, a CC line. `dataset check`: 0 errors, the two known warnings (constant `cd_000`, blanks that
   mark the negative class) and a new info `groups_not_clustered` (most trucks have one row); not rebuilt. The split
   table of 2026-11-11 with cg (untuned LightGBM, 3 folds, 2 seeds; Slurm jobs 1379970 and 1379994):

   | Split | Rows | Test rows with a copy in training | Cost per row | Cost, each truck once | ROC AUC |
   |---|---|---|---|---|---|
   | a: random, all rows (shipped before) | 76,000 | 25.2% | 1.145 | 1.338 | 0.9910 |
   | c: one row per cluster at 140, random | 63,937 | 5.1% | 1.530 | 1.517 | 0.9888 |
   | cg as applied | 63,937 | 0.05% | 1.625 | 1.539 | 0.9887 |
   | cg, trucks from the links on all rows only | 63,937 | 0.05% | 1.579 | 1.530 | 0.9893 |
   | cg, trucks from the links on the kept rows only | 63,937 | 0.05% | 1.673 | 1.586 | 0.9891 |
   | d: one row per cluster at 60, random | 61,524 | 0.05% | 1.557 | 1.557 | 0.9892 |
   | g: grouped on the clusters at 60, all rows | 76,000 | 0.05% | 1.491 | 1.558 | 0.9885 |

   - The two seeds of one split differ by up to 0.15 in cost, so cg, d and g are equally hard.
   - The links on all rows alone miss 94 links at 60 counters found on the kept rows, where a value several copies held
     becomes rare: with those trucks 0.18% of the test rows keep such a link in training, with the applied ones 0.05%.

2. **Time basis: keep the forced tag, now with its `Time basis:` line?**

   * **Problem:**
     - Trucks failed over a period Scania never states, and the release keeps no time: no date, and the challenge's
       two files are not two periods as far as the data shows (near copies across them go either way, 2,237 against
       2,220).
     - The record's collection facts fit what was found (`Samples: Over Time`, `Time: Lost`, no target tag, as the
       failed component is known at the workshop), and the definition carries `ForcedIIDFromTemporal`, but without a
       line, and its `fit_reason` still says the challenge's test rows "may be later readings".
     - Keep the forced tag with a line, or read the task as a stationary relation, a diagnosis from the counters?
   * **Background:** the questions that tell the time bases apart[^2a]:
     - Can time affect the target? Among failed trucks, which component failed can move with the season, the age of
       the fleet and workshop practice.
     - Does the use case predict for a time after its data? Yes: the workshop decides on the next failed truck.
     - One shared prediction moment? No: each truck at its own failure.
     - Does arrival over time move the target? Argued from the source, as nothing dated can measure it: the
       challenge's test file has a higher share of air pressure failures (2.34% against 1.67%) for a reason it does not
       state; with the time lost that is the forced case[^2b].
     - A stationary relation would read the failed component as a present state read from the counters; nothing
       dated can show that relation flat.
   * **Experiments:** today's checks on UCI's two files, model-free: within each file the air pressure share per
     tenth stays flat (training file 1.4% to 2.0%, test file 1.8% to 2.6%), and so does the median `aa_000` (29,000
     to 34,000 in every tenth); the copies are issue 1's answer of today. The leak test across the forced split finds one
     leak, the copies of issue 1; period and order leaks have nothing to act through.
   * **Unknown:** when the counters were read relative to the failure (before it, as a warning, or after it); the
     newer Scania release `scania_component_x`, screened in its own record, has dated read-outs.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Forced from temporal (implemented), with its line | `ForcedIIDFromTemporal` stays; a `Time basis:` line names the unstated period and the undated files; `fit_reason` drops "may be later readings" | says what the random score stands for; what the data shows about the two files | none found |
     | B | Stationary relation | the tag `StationaryRelation` and a line arguing that a failed truck's counters read the same whenever it failed | none found | the test file's higher share of air pressure failures is unexplained; no dated data to measure the relation on |

   * **Recommendation:** A: a forward use case whose time is lost is what the forced tag names; the line replaces a
     guess about the files with what they show. **Decision:** forced with its line (A) or stationary relation (B)?

   **Notes for the AI:** once PR #50 is in, on A: `data_tags` stay `("ForcedIIDFromTemporal", "Anonymized")`; add
   the curation bullet "- Time basis: ForcedIIDFromTemporal: failed trucks read out over a period Scania does not
   state; the release has no date, and the challenge's two files are not shown to be two periods (near copies across
   them have the larger counters in the test file in 2,237 pairs, the smaller in 2,220), while which component fails
   can move with season and fleet, so random trucks stand in for the trucks to come. A dated release (as
   `scania_component_x`) would allow a split by date."; in `fit_reason`, replace "The challenge's test rows may be
   later readings; with no dates to check, a random split stands in for a split by time" with "Failures are undated,
   so a random split stands in for a split by time"; in `split`, replace "which may be later in time; the file has no
   dates to check" with "which are not later readings of the same trucks; the files have no dates". No
   `splits_comment` (default split).

   [^2a]: **SPLIT-32** (Should): how and when samples, features and the target arrive is information for the split;
     the record keeps the source's collection facts, and a definition can name the use-case prototype it follows
     (`Timeless`, `Snapshot`, `DelayedTarget`, `StationaryRelation`) with a `Time basis:` line stating the fact behind
     it; a forward task whose time is lost or too short is forced.
   [^2b]: **SPLIT-8** (Must): a task temporal by its use case whose release cannot give the windows ships in the
     closest regime that keeps the rows, tagged as forced from temporal, after a leak test across the split; it says
     what a dated release would change.

   **Resolved (2026-11-10, Andrej):** A (ok): `ForcedIIDFromTemporal` stays in `data_tags`, now with its `Time basis:`
   line in `curation_comments` as drafted; `fit_reason` reads "Failures are undated, so a random split stands in for a
   split by time", and the split summary says the challenge's last 16,000 rows are not shown to be later in time, the
   files having no dates; CC line in the record.

3. **`CrossSectional` instead of `ForcedGroupedFromTemporal`?**

   * **Problem:**
     - The definition is tagged `ForcedGroupedFromTemporal`, a forward use case whose time was lost[^fo-3].
     - The target is a present state measured with the features: which component failed, read from the truck's counters at the failure, and the use case reads it for new units at their own present[^cs-3].
     - The tag alone changes: the split stays grouped by truck.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Stay `ForcedGroupedFromTemporal` (implemented) | the tag and its line stay | the decision stands | the tag claims a forecast the use case does not make |
     | B | `CrossSectional` | the tag and a `Time basis:` line naming the present state, the untested drift for later units and what a dated release would show | names the use case; no claim of a lost forward split | a new prototype on a decided tag |

   * **Recommendation:** B. **Decision:** A or B?

   **Notes for the AI:** on B, swap the tag, write the line, add a CC line; the split does not change.

   [^cs-3]: **SPLIT-32** (Should, 2026-11-13): a target measured together with the features, which the use case reads for new units at their own present, is `CrossSectional`, whether the dates survive or not; its line says whether the drift of the relation was measured or is untested. A label that only arrives later is no present state.
   [^fo-3]: **SPLIT-8** (Must): a forward use case without usable time ships in the closest regime, tagged forced from temporal, with a `Time basis:` line naming the reason.

   **Andrej (2026-11-13, ok):** As implemented.

   **Resolved (2026-11-13, Andrej):** withdrawn: `CrossSectional` was dropped the same day (it named no split the existing prototypes do not give: a present state used later is forced or a measured `StationaryRelation`, used within the covered time `Retrospective`). The tag stays.

## Reference

10.24432/C5V60Q
