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
suggestion: 'Yes'
decision_markers:
- Anonymized
tags:
- 'Samples: Over Time'
- 'Time: Lost'
original_source: Other
year: '2016'
required_split:
- Random (IID)
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

CC (2026-11-11, Andrej): review marks of today; issue 2 applied to the definition, issue 1 answered and still open.

- Issue 2 (ok): `data_tags` stay `("ForcedIIDFromTemporal", "Anonymized")`, now with the `Time basis:` bullet they were missing here: failed trucks read out over a period Scania does not state, no date in the release, and the challenge's two files not shown to be two periods, while which component fails can move with season and fleet, so random trucks stand in for the trucks to come (SPLIT-8, SPLIT-32). `fit_reason` now reads "Failures are undated, so a random split stands in for a split by time", and the split summary says the challenge's last 16,000 rows are not shown to be later in time.
- Issue 1 (no mark; "Wait, I don"t get it, isn"t the acvtual issue that there should be a temporal component that is mot considered. Try to reconstruct it before dropping any columns"): reconstructed over the whole release, not only the near copies (Slurm job 1378335). A model cannot tell the challenge's training file from its test file (ROC AUC 0.501 over 5 folds), the file order carries no drift (first 80% to last 20%: AUC 0.994, cost 1.04 against 0.991 and 1.31 for random splits of that size), the challenge's own split scores like a random one (0.996 / 1.54 against 0.990 / 1.18), and `aa_000`, the counter that could stand in for operating time, is close to the label at its top end (failure rate 17.0% in its top decile against 0.01% to 0.57% below), so a split along it is a split on the target, not on time. No option in the issue drops a column; c and d drop rows. The issue stays open for the row decision (d, c or keep a).
- `dataset check`: 0 errors, 2 warnings, both older than this change (`cd_000` constant; eight missing-value bins that hold the majority class). Not rebuilt. The review moved from the folder's `REVIEW.md` into this record's `## Review` section.

## Review

**Outcome:** added. The IDA 2016 Industrial Challenge (Scania, via UCI): 76,000 heavy trucks with a component failure,
170 anonymised operating counters and histogram bins each, and whether the failure is in one component of the air
pressure system (1,375 trucks, 1.8%), scored by the challenge's cost (10 per needless check, 500 per missed failure).
The AI recommends shipping it after one change (issue 1). Reviewed on 2026-11-04 without a review panel, from the
gathered evidence (the record, model runs on the TabArena v0.1 task of the same 76,000 rows) and two checks of
today on the UCI files. Validity: a workshop's call whether to check the air pressure system, an approximate fit (no
dates; when the counters were read relative to the failure is not stated); the challenge's split is replaced by a forced
random one. Our experiments found that the same truck appears more than once, and today's checks confirm it on the v0.2
rows: 30% of the rows have a near copy that agrees on 140 to 169 of the 170 counters and always carries the same label,
and a random split puts such a copy on the training side for 21% of the test rows (issue 1). Value: the `one_feature`
flag is settled (the best single counter, ROC AUC 0.970, stays below every tuned method; Lennart, 2026-10-06); on the
shipped splits the benchmark methods spread from 1 - AUC 0.0048 to 0.0085 at the median and 0.010 to 0.013 for linear
models. Quality: nothing open beyond issue 1. Weighed: an industrial challenge with a stated cost +, methods that
separate +, repeated trucks across the split -, anonymised counters and no dates -; a newer Scania release
(`scania_component_x`) is screened in its own record.

**Main points:** Keep one row per truck, so no truck's own copy sits on the other side of the split (issue 1)? New on
2026-11-06: the cut at 140 counters misses looser copies of the same read-outs, and one row per truck down to 60
counters leaves 0.05% of test rows with a copy in training instead of 5.1% (issue 1, answer)? On
2026-11-10: no time order hides in the copies (`aa_000` equal in 97% of pairs, the label the same in all), so one row
per truck stands (issue 1, answer)? Record `domain` set (2026-11-11). The forced tag stays, now with its `Time basis:` line: the failures are undated, and
the challenge's two files are not two periods (issue 2, resolved 2026-11-10).

**Record judgment:** valid task, damaged split. The description file in UCI's zip carries a GNU GPL v3 notice from
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
   records and the class shares into `curation_comments`. Scripts and logs in `~/claude_jobs/entity_review/aps_failure/`:
   `entity_check.py` (job 1366347: nulls, label baseline, order, the drop at 140), `cut_options2.py` (job 1366370:
   bands, `aa_000`, the cuts), `unlinked_lookalikes.py` (job 1366366: the blank records). The null shuffles each
   counter on its own, so it breaks columns that hold one value within a row (`bb_000`, `bu_000`, `bv_000` and
   `cq_000` are equal in 99.7% of the training file's rows), where one shared rare value counts several times; the
   label and `aa_000` tests do not depend on that.

   [^1e]: **LEAK-41** (Must; draft PR #62): repeats of a unit the data does not record get one of four verdicts:
     natural, entity fix, temporal fix or not recoverable; an entity fix takes copies of one record down to one row
     per unit, and every drop gives the label shares before and after and asks whether the target still stands.
     **LEAK-42** (Should; draft PR #62): three tests set the verdict: a link far above a chance rate that keeps the
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

   **Andrej (2026-11-11):** Wait, I don"t get it, isn"t the acvtual issue that there should be a temporal component
   that is mot considered. Try to reconstruct it before dropping any columns

   **Answer (AI, 2026-11-11):** reconstructed once more, this time over the whole release and not only the copies:
   no temporal component can be recovered, and no option drops a column. **Decision:** d, c, or keep a?

   * **Problem:**
     - A time order would have to come from one of three places: the two challenge files as two periods, the file
       order, or a counter that grows with a truck's life; all three were tested today and none carries one.
     - The one counter that could stand in for time, `aa_000`, is itself close to the label at its top end, so a
       split along it is a split on the target, not on time.
     - So the question the issue puts is unchanged: the near copies are one read-out repeated, and they stay or go
       as rows; no option touches a column.
   * **Experiments:** UCI 421's two files as published (76,000 trucks, 1,375 failures, 170 counters), untuned
     LightGBM, the challenge cost (10 per false alarm, 500 per missed failure) at the least-expected-cost threshold
     (Slurm job 1378335, `~/claude_jobs/marks_b1/aps_time.py`):

     | Reconstruction tried | ROC AUC | Cost per truck | Reads as |
     |---|---|---|---|
     | Can a model tell the training file from the test file (5 folds) | 0.501 (0.496 to 0.511) | | the two files are one population, not two periods |
     | Train on the low 80% of `aa_000`, test on the high 20% | 0.852 | 26.72 | not a time split: the failures sit in the top decile |
     | Train on the high 80% of `aa_000`, test on the low 20% | 0.810 | 0.26 | the same effect the other way round |
     | Random splits of the same size (5 draws) | 0.992 | 1.10 | the reference |
     | Train on the first 80% of the training file, test on its last 20% | 0.994 | 1.04 | the file order carries no drift |
     | Random splits of that size (5 draws) | 0.991 | 1.31 | the reference |
     | The challenge's own split (training file to test file) | 0.996 | 1.54 | as a random split of the same sizes |
     | Random splits of 16,000 (5 draws) | 0.990 | 1.18 | the reference |

   * **Background:** the failure rate by decile of `aa_000` runs 0.04%, 0.04%, 0.01%, 0.05%, 0.04%, 0.11%, 0.08%,
     0.12%, 0.57%, 17.04%, so holding out the top decile holds out almost every failure; that is why the cost rises
     to 26.72 there and falls to 0.26 the other way. `aa_000` has the same median in both files (30,776 and 30,982)
     and no relation to the row position (rank correlation -0.004), so it orders trucks by use, not by date.
   * **Consistency:** this repeats on the whole release what the answer of 2026-11-10 found inside the copies
     (`aa_000` equal in 13,340 of 13,409 pairs, chains that agree with the file order at chance, every copy carrying
     the same label).
   * **Unknown:** the calendar dates themselves. Only Scania could add them; the newer release
     `scania_component_x`, screened in its own record, has dated read-outs.

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
   `splits_comment` (default split). Evidence: `~/claude_jobs/time_review/aps_failure/` (`scripts/copies_order.py`,
   `copies_order.txt`).

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

   **Resolved (2026-11-11, Andrej):** A again on today's mark (ok, no note), and now carried by this branch, which had
   the old text: `data_tags` stay `("ForcedIIDFromTemporal", "Anonymized")`, the drafted `Time basis:
   ForcedIIDFromTemporal:` bullet is in `curation_comments` (the unstated period, the two challenge files that are not
   shown to be two periods, what a dated release as `scania_component_x` would allow), `fit_reason` reads "Failures are
   undated, so a random split stands in for a split by time" and the split summary says the challenge's last 16,000
   rows are not shown to be later in time. `dataset check`: 0 errors, 2 warnings, both of them older than this change
   (`cd_000` constant, and the missing-value bins that hold the majority class).

## Reference

10.24432/C5V60Q
