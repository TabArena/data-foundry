---
unique_name: concrete_compressive_strength
name: concrete_compressive_strength
checked_by:
- Lennart
- Andrej
data_foundry_status:
- 'DF: Yes'
- TabArena (v0.1)
- BeyondArena
suggestion: 'Yes'
tags:
- 'Samples: No Time Dimension'
original_source: UCI
year: '2007'
required_split:
- Grouped (NON-IID)
source_links:
- https://www.openml.org/search?type=data&id=44959
- https://doi.org/10.24432/C5PK67
notebook_path: datasets/beyond_iid/old_iid/concrete_compressive_strength/concrete_compressive_strength.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/concrete_compressive_strength/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Tabular.

Data from a lab, likely a real problem?

Potential issue: unclear domain task

Lennart: Likely yes as no objects beside maybe outdated / lab setup that is not a real predictive task

Andrej: Seems fine

**Assessment (AI, 2026-10-14):** Hidden groups. The 1,030 tests are 428 concrete mixes (identical amounts of all seven ingredients); 182 mixes are tested at several ages (up to 20 tests), so 76% of the rows share their mix with another row, and the mixes carry 65% of the strength variance. On the shipped random splits (10 x 3), 73% of the test rows had their mix in training at another age. R^2, random against grouped by mix: LightGBM 0.925 / 0.874, extra trees 0.912 / 0.881, random forest 0.901 / 0.856, MLP 0.916 / 0.838, kNN 0.882 / 0.826, ridge 0.816 / 0.804; the ranking of the models changes. The use case, designing a new mix (the UCI page lists Yeh 1999, "Design of High Performance Concrete Mixture Using Neural Networks"), predicts for a mix not tested before. The hidden-group probe missed it because it only tests single columns (the ingredient amounts are fractional, so none is a candidate, and Age has 14 values) and its near copies need at least 10 informative columns (the table has 8). Since 2026-10-14 it also checks keys of all columns but one, and `(all but Age)` is a hit (76.1% of the rows, 0.0% with independent columns; untuned LightGBM R^2 0.923 random against 0.857 grouped). The definition now groups by `mix`, built from the seven ingredient columns and not a feature: 10 x 3 grouped splits, 142-143 test mixes per fold; group_probes.py: LightGBM 0.924 IID against 0.874 grouped, and across mixes ridge 0.596, random forest 0.859, LightGBM 0.876, kNN 0.703. This changes the split shipped in TabArena v0.1 and BeyondArena.

CC (2026-10-14, Lennart): Grouped by mix: a new prediction is for a mix not tested before.

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback rmse — Yeh 1998 (closed access) is cited for R^2 of predicted vs measured strength (about 0.91-0.92 for the ANN) by secondary sources; not read, and R^2 ranks models as RMSE does within a fold. rmse is the regression fallback.

**Assessment (AI, 2026-10-31):** better data: the data-scouting run of 2026-10-30/31 found better data for the same task: `blended_cement_concrete_strength` (TBD -> Yes, priority 3). Each is screened in its own record; this record's verdict stays the curator's.

CC (2026-11-11, Andrej): review marks applied (Review issue 3; issue 1 stays open). Text and tag only, the data is unchanged.

- Issue 3 (B, "Option B: Correct it."): the data is a compilation, not one laboratory's tests. Yeh 1998 took the rows from 17 published studies (its reference list names 8 Taiwanese master's theses, 1991 to 1998, and 8 journal papers, 7 of them in ACI Materials Journal). `fit_reason` now reads "narrow (high-performance mixes compiled by Yeh 1998 from 17 published studies, mostly Taiwanese theses and ACI papers) but real", and the row text says "compiled by I-Cheng Yeh in 1998 from 17 published studies".
- The `Timeless` time basis of issue 2, accepted on 2026-11-06, is carried out here: `data_tags = ("Timeless",)` and the `Time basis:` bullet in the definition's notes, which clears the missing-time-basis check note.
- Issue 1 (grouping the re-entered mixes) stays open: the source answer of 2026-11-11 recommends c, dropping the 92 rows of the block that repeats rows 721 to 935.
- `dataset check`: 0 errors; the known warning on the 25 exact duplicates (issue 1) remains.

## Review

**Outcome:** added. Laboratory tests of high-performance concrete compiled by I-Cheng Yeh from 17 published studies (UCI, donated 2007,
https://doi.org/10.24432/C5PK67; Yeh 1998, Cement and Concrete Research 28(12):1797-1808): the compressive strength of
1,030 tests of 428 mixes, from the amounts of seven ingredients and the age at the test; RMSE fallback, and since
2026-10-14 split by mix (Lennart), so a test mix is a design not yet tested. The AI recommends shipping it after one
change to the groups (issue 1). Reviewed on 2026-11-04 without a panel, from the gathered evidence (the record, the
CHANGELOG, model runs on the shipped data and on TabArena v0.1's copy) and one check on the v0.2 frame.
Validity: a real engineering question (strength of a new mix before casting) on measured strengths; the inputs are
what the engineer chooses. But the same test was often entered twice with the amounts rounded differently (146.5
against 147 kg), so it lands in another mix group, and 17% of the test rows of the shipped splits have such a copy in
training (issue 1). Value: across mixes, LightGBM R^2 0.874 against ridge 0.596 (record, 2026-10-14); on the shipped
data (random splits) the 40 benchmark methods spread from RMSE 3.76 (Kumo) to 8.15 MPa (linear models; one diverged run
aside), median 4.16. Quality: 25 exact copies stay in their mix's fold (noted in the definition). Weighed: a real
design task on measured strengths +, wide separation of methods +, re-entered records that cross the split -, a narrow family of
mixes compiled from 17 studies -.

**Main points:** The copies of issue 1 are one source entered twice (rows 936 to 1029 repeat rows 721 to 935):
drop them (c), merge them (b) or keep the exact groups (a)? A split by source study (issue 4): the rows fall into 11
blocks, not cleanly into the 17 sources, and the scores collapse; keep the mix split? The definition now says "compiled
from 17 published studies" (issue 3, resolved 2026-11-11). The mix split is named `Timeless` (issue 2, resolved
2026-11-06).

**Record judgment:** valid. The record carries Lennart's grouping by mix (CC 2026-10-14). `fit_reason` describes the
data as high-performance mixes compiled by Yeh 1998 from 17 published studies, mostly Taiwanese theses and ACI papers
(issue 3, 2026-11-11).

**Issues for Andrej:**

1. **Group each mix with its re-entered copies, whose amounts differ only by rounding?**

   * **Problem:**
     - The groups join rows whose seven ingredient amounts are identical, but 114 pairs of rows at the same age agree
       within 0.5 kg on all seven amounts and differ only in rounding, and 77% of them carry the same strength to
       0.01 MPa, against 0.12% of random pairs at the same age, so they are one test entered twice.
     - Such a pair falls into two groups, and 17.0% of the test rows of the shipped splits (11.6% to 24.5% per split)
       have a training row of their mix at the same age within 1 kg; 11.8% have one with the identical strength.
     - Merge the copies into their mix's group, drop them, or keep the groups as they are?
   * **Background:** Lennart grouped by mix because a new prediction is for a mix not yet tested (73% of the test
     rows had their mix in training under the random split)[^1a]. A rounded copy is the same mix, so it should leave
     with it. A simple model on the shipped data pulled each prediction toward a near-copy's label in
     training and flagged that step as a leak. Within one mix, 54 pairs of tests at the same age repeat as well (80%
     with the same strength, the 25 exact copies); they already share a fold.
   * **Effect on the task:** a test row whose re-entered copy is in training is answered by look-up, not by
     predicting a new design, so scores and the ranking lean toward methods that memorise near-identical rows.
   * **Experiments:** on the v0.2 frame and its 30 shipped splits, untuned LightGBM (one configuration):

     | Groups | Groups (mixes) | R^2 (mean over 30 splits) |
     |---|---|---|
     | identical amounts (shipped) | 428 | 0.864 |
     | shipped, scored without the test rows that have a same-strength copy in training | 428 | 0.854 |
     | mixes merged when all seven amounts agree within 1 kg | 315 | 0.839 |

     - With a 1 kg tolerance 140 pairs qualify (66% with the same strength), with 2 kg 158 (58%): the strength match
       falls as the tolerance widens, so 0.5 to 1 kg is the recording's rounding.
   * **Consistency:** follows the grouping by mix (concrete, 2026-10-14) and airfoil_self_noise's grouping by setup
     (2026-10-20). Groups must be exact, never a similarity cluster[^1b]: here the tolerance stands for the rounding of
     the recorded amounts, and the identical strengths show the same record, not a similar mix.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Identical amounts (implemented) | 428 groups; rounded copies can sit on both sides | as decided on 2026-10-14; groups exact to the digit | 17% of test rows have a copy of their mix in training |
     | B | Merge rounded copies | mixes whose seven amounts all agree within 1 kg form one group (315 groups); all rows kept | holds out each mix with its re-entries, as the grouping intends; no row lost | a tolerance, not an exact key; may also join two batches that differ by a few grams of an admixture |
     | C | Drop the re-entries | rows with a same-age copy within 1 kg and the same strength to 0.01 MPa keep one row; groups as now | removes the copies the strength proves | drops rows; copies of one mix with another strength still cross the split |

   * **Recommendation:** B: the copies are the same mix, so they belong to its group, and no row is lost; R^2 falls
     from 0.864 to 0.839. **Decision:** keep the exact groups (A), merge the rounded copies (B), or drop the
     re-entries (C)?

   **Notes for the AI:** on B, build `mix` in `_clean` as the connected components of mixes (identical-amount groups)
   whose seven amounts all differ by at most 1 kg (union-find over the 428 mixes; 315 groups), keep it out of the
   features, state the 114/140 pairs, the 77% strength match and the R^2 figures in `curation_comments`, update the
   grouping definition and `changes`; `dataset check`; CHANGELOG; record CC. The check is the review's script of
   2026-11-04 (batch H_chem_bio).

   [^1a]: **SPLIT-29** (Must): an IID split is wrong when many rows share an entity that new data would not have and
     the entity carries the label.
   [^1b]: **SPLIT-24** (Must): group on a true group id or on one constructed exactly from the data (identical values
     in the columns that define the entity), never on a similarity-threshold cluster.

   **Answer (AI, 2026-11-06):** the time framing does not change this question. The only time in a row is the test
   age, a designed feature; a mix's early results come in before its late ones, but every option keeps a mix's ages
   together, and none moves a later result in front of an earlier one in calendar time, which the source does not
   record. The re-entered copies are a question of one entity entered twice, as above. Under every option the split
   is `Timeless` (issue 2).

   **Andrej (2026-11-10, note):** Measure how big the change would actually be, then we rediscuss. Also, how are the
   current group keys found vs. how would they be found with your change?

   **Answer (AI, 2026-11-10):** the change is moderate. It merges 222 of the 428 mixes into 109 groups, it moves 18% of
   each test fold, and tree models lose 0.025 to 0.027 R^2.

   | What changes | Count |
   |---|---|
   | Mix pairs whose seven amounts all agree within 1 kg | 117 (115 of them tested at a shared age) |
   | Groups | 428 to 315 (105 pairs, 4 triples) |
   | Rows in merged groups | 280 of 1,030 (27%) |
   | Test rows (shipped splits) whose merged group is partly in training | 18.4% (13.3% to 26.0%), 63 of 343 per fold |
   | Shared (pair, age) tests with the same strength to 0.01 MPa | 92 of 135 (68%; random pairs 0.12%) |

   | Model (10 x 3 grouped splits) | Exact amounts (shipped) | Merged within 1 kg |
   |---|---|---|
   | LightGBM, untuned | R^2 0.864 (RMSE 6.11) | 0.839 (6.63) |
   | Random forest | 0.855 (6.33) | 0.828 (6.86) |
   | Ridge, log age | 0.803 (7.36) | 0.802 (7.36) |

   * **Current key:** rows whose seven amounts are identical to the last digit form one mix (`groupby` on the seven
     columns).
     A mix entered twice with one amount rounded differently (146.5 against 147 kg) becomes two groups.
   * **With the change:** start from those mixes, and join two mixes when every one of the seven amounts differs by at
     most 1 kg/m^3.
     Joins chain (a union-find), but here the chains stay short: the largest group holds 3 mixes, and the median
     difference in a linked pair is 0.5 kg.
   * The ranking stays the same. The gap between trees and the linear model shrinks from 0.061 to 0.037 R^2, because the
     merge removes look-ups that only flexible models exploit.
   * Script `~/claude_jobs/marks_1110/concrete_compressive_strength/size.py`.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | a | Exact amounts (implemented) | 428 groups | exact key | 18% of test rows meet their re-entered mix in training |
   | b | Merge within 1 kg | 315 groups, all rows kept | each mix leaves with its re-entries | a tolerance, not a digit-exact key |

   * **Recommendation:** b. The 68% identical strengths show that the joined mixes are one test entered twice.
     **Decision:** a or b (or C of the issue, drop the re-entries)?

   **Andrej (2026-11-11, discuss):** Before finally deciding, look at the source again and what they say about the
   experimental design and repetitions.

   **Answer (AI, 2026-11-11):** the copies are one source entered twice. Rows 936 to 1029 are a block of the UCI file,
   and 87 of its 94 rows repeat a row of rows 721 to 935: same age, amounts to 0.1 kg instead of whole kg, strength
   within 0.01 MPa (median difference 0.003 MPa).

   * **Source:** the data is a literature compilation, not one laboratory. Yeh 1998 checks its model on "experimental
     data from 17 different sources" (full-text snippet); its reference list (Crossref) names 16 data sources: 8
     Taiwanese master's theses (1991 to 1998, three universities) and 8 journal papers (7 in ACI Materials Journal,
     1989 to 1993). Yeh 1999 says 16 sources. The full text was not read (closed access).
   * **Row:** neither the UCI readme nor what we could reach of the papers says whether a row is one specimen or a
     mean. The strengths are the sources' published numbers converted to MPa: 71% are whole psi (100% in rows 100 to
     499).
   * **Ages:** each source tested its mixes at its own schedule; the age sets repeat by source, e.g. 3/14/28/56/100
     days (52 mixes) or 7/28 (40 mixes). 246 mixes have one test.
   * **Repeats:** 19 (mix, age) cells hold two rows (10 with the same strength, 9 with another).
   * **Near-identical mixes:** two kinds.

     | Mix pairs within 1 kg on all seven amounts | Pairs | Where |
     |---|---|---|
     | same strength at every shared age | 91 | 87 in the block 936-1029 against 721-935 |
     | another strength at every shared age | 24 | scattered (e.g. rows 471/472: superplasticizer 11.61 against 11.64, 57 against 44 MPa) |
     | no shared age | 2 | |

   * The first kind is a source entered twice (likely one study taken from two documents), so it is a duplicate, not a
     second test. The second kind is two tests of two mixes and passes the exact key.
   * Dropping the later entry of each same-strength copy removes 92 rows (87 in the block): 938 rows, 338 mixes; 25
     mix pairs within 1 kg remain, all with other strengths.

   | | Option | What it does | Pro | Con |
   |---|---|---|---|---|
   | a | Exact amounts (shipped) | 1,030 rows, 428 groups | no change | 18% of test rows meet their own record in training |
   | b | Merge within 1 kg | 315 groups, all rows kept | no leak | a tolerance key; duplicates count twice; joins the 24 pairs of different tests |
   | c | Drop the re-entries | keep the first entry of each same-strength copy; 938 rows, 338 exact groups | the duplicate goes, the exact key stays | drops 92 rows |

   * **Recommendation:** c. The source shows the copies are one record entered twice, so they are duplicates to drop,
     and the remaining near pairs are separate tests that the exact key may split. The R^2 of c is measured with the
     `dataset check` after the decision.
   * Script `~/claude_jobs/marks_1111/concrete/source.py` (and `source2.py` to `source4.py`).

   **Decision:** a, b or c?

2. **Time basis: name the mix split `Timeless`, as laboratory tests of designed mixes?**

   * **Problem:**
     - A mix's seven amounts are chosen before casting and its strength is measured at the stated age (1 to 365 days,
       a feature), in laboratory tests compiled by Yeh (1998) with no calendar date, so the only time in a row is the
       designed test age.
     - The record carries `Samples: No Time Dimension` and no time or target fact; the split holds out whole mixes
       (Lennart, 2026-10-14) and has no time-basis tag yet.
     - The strength of a mix at a given age is a property of the mix, the material's strength that the `Timeless`
       prototype names[^2a].
   * **Background:** the strength arrives after the casting, by as many days as the age column says, so the target
     comes after the features in the lab; but the age is part of the question asked (strength at 28 days), every
     result was in before the 1998 compilation, and none is revised. The record therefore needs no target fact: a
     delay that is itself a designed feature informs nothing about the split. The decimals of the amounts may mark
     several source laboratories (record judgment); a source is no period, and its dates are unknown.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Mix split, no time-basis tag (implemented) | as now | nothing to change | the definition does not say why a split that is not temporal is safe in time |
     | B | Mix split, `Timeless` | as now (or with issue 1's groups); the tag and a `Time basis:` line naming the designed mixes and the test age | states the fact the split rests on; matches the study and the airfoil precedent | none found |

   * **Recommendation:** B: the target is a material's strength at a chosen age, and no calendar time is in the
     source. **Decision:** A or B?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Timeless",)` (the class adds `Non-IID`,
   `Grouped`), a curation bullet `- Time basis: Timeless: laboratory tests of designed mixes (Yeh 1998); the amounts
   are chosen before casting and the strength is measured at the stated age, a feature; no test date is recorded.`,
   `splits_comment` unchanged; `dataset check`.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     source's collection facts, and a definition can name the use-case prototype it follows with a `Time basis:`
     line. `Timeless`: the target is a fixed property of the item, the same whenever it is measured (a material's
     strength, a molecule's activity, a species, the outcome of a designed run); the split is random or grouped by
     item family.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the routine `Timeless` time
   issues with one mark?" The `Time basis: Timeless:` bullet is in `curation_comments`, ending with what the split
   cannot test (mixes of a laboratory outside the compilation); the split and `data_tags` are unchanged. The tag
   `Timeless` enters `data_tags` once PR #50 is in the working copy.

   **Resolved (2026-11-11, Andrej):** carried out here: `data_tags = ("Timeless",)`, as this working copy has the
   time-basis tags; the `Time basis: Timeless:` bullet is in `curation_comments`. `dataset check`: 0 errors, the known
   warning on the 25 exact duplicates (issue 1).

3. **Describe the data as a compilation of published studies, not one laboratory's tests?**

   * **Problem:** `fit_reason` says "one laboratory's family of high-performance mixes"; Yeh 1998 compiled the rows
     from 17 sources (8 Taiwanese master's theses, 8 journal papers in its reference list; issue 1, answer of
     2026-11-11).
   * **Options:**

     | | Option | What it does |
     |---|---|---|
     | A | Keep the text (implemented) | as now |
     | B | Correct it | `fit_reason`: "narrow (high-performance mixes compiled by Yeh 1998 from 17 published studies, mostly Taiwanese theses and ACI papers) but real"; the record's judgment line the same |

   * **Recommendation:** B, a factual fix with no effect on the data. **Decision:** A or B?

   **Notes for the AI:** on B, edit `fit_reason` in dataset.py, regenerate README.md, CHANGELOG line, record CC. No
   check needed (text only).

   **Andrej (2026-11-11, change):** Option B: Correct it.

   **Resolved (2026-11-11, Andrej):** B: `fit_reason` now reads "narrow (high-performance mixes compiled by Yeh 1998
   from 17 published studies, mostly Taiwanese theses and ACI papers) but real", and the row text says "compiled by
   I-Cheng Yeh in 1998 from 17 published studies" instead of "published by"; README.md regenerated (only these two
   lines changed), the record judgment line above updated, record CC. Text only; `dataset check` ran clean (0 errors,
   the known warning on 25 exact duplicates).

4. **Split by source study instead of by mix?**

   * **Problem:**
     - The UCI file is ordered by source: decimals, strength units, admixture pattern and age schedule change together
       at 12 row boundaries, which give 11 source blocks after merging blocks that re-enter each other's mixes.
     - The blocks are not the 17 sources of Yeh 1998: one block holds 27 single mixes of several papers, another 14 age
       schedules, and which block is which reference is a guess (the paper was not read).
     - Grouped by block, every model loses 0.13 to 0.30 R^2 and LightGBM falls below ridge.
   * **Background:** Andrej asked on the page (2026-11-11, dataset note): "Could a split by source make sense?" The mix
     split asks for a new mix design from the same pool of studies (the use case: an engineer with past results). A
     source split asks for a new laboratory's materials, aggregates and curing, which the seven amounts do not
     describe, on a key reconstructed from the file order[^4a].
   * **Assignment:** e.g. row 184 starts the fly-ash mixes with two decimals and ages 3/14/28/56/100. Rows 0 to 69 are
     shuffled from two series; rows 721 to 828 re-enter 7 mixes of rows 552 to 597 and 2 of rows 0 to 69 (rounded,
     same strengths), so those are one group. Groups hold 21 to 201 rows; 9 groups if two pairs of blocks with the same
     schedule and units are one source each. No exact mix sits in two groups.
   * **Experiments:** grouped 3-fold x 10 on the 1,030 rows (TabPFN v3.5, untuned LightGBM, ridge on log age):

     | Groups | Ridge R^2 | LightGBM R^2 | TabPFN R^2 | TabPFN RMSE |
     |---|---|---|---|---|
     | by mix (as shipped; issue 1 copies still cross) | 0.803 | 0.862 | 0.911 | 4.90 |
     | by source, 11 blocks | 0.672 | 0.558 (sd 0.25) | 0.701 | 8.48 |
     | by source, 9 blocks | 0.643 | 0.476 (sd 0.38) | 0.658 | 9.04 |

     - Leaving one block out, the 28-day three-admixture block (rows 829 to 1029) gives LightGBM R^2 -1.30 (ridge
       0.46), and the slag series of rows 0 to 69 is below zero for every model: these blocks lie outside the others'
       mixes.
     - With 11 groups each fold holds 3 to 4 sources, so a score swings by 0.1 to 0.4 R^2 between repeats.
     - Scripts in `~/claude_jobs/marks_1111/concrete_compressive_strength/srcsplit/` (`blocks.py`, `groups.py`,
       `run.py`).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep the mix split (implemented) | as now, plus a note in `curation_comments` that the rows come in about 11 source blocks and the split does not test a new laboratory | matches the use case; exact key | a study's mixes sit on both sides |
     | b | Split by source block | `source` as the group column (11 groups) | tests transfer to a new laboratory | a reconstructed, partly guessed key; very noisy scores; a different task, in which ridge beats LightGBM |

   * **Recommendation:** a: the blocks cannot be tied to the sources cleanly, and the use case is a new mix, not a new
     laboratory. **Decision:** a or b?

   **Notes for the AI:** on a, add to `curation_comments`: "- The UCI file is ordered by source study: decimals,
   units and age schedules mark about 11 blocks (the 17 sources of Yeh 1998 cannot be told apart cleanly). The mix
   split does not test a new laboratory: grouped by block, TabPFN R^2 0.70 against 0.91 by mix." Regenerate README,
   CHANGELOG, record CC. On b, build `source` in `_clean` from the row ranges of `groups.py` (merges included), group
   on it, keep it out of the features, and rerun `dataset check`.

   [^4a]: **SPLIT-24** (Must): group on a true group id or on one constructed exactly from the data (identical values
     in the columns that define the entity), never on a similarity-threshold cluster.

## Reference

Yeh, I-C. "Modeling of strength of high-performance concrete using artificial neural networks." Cement and Concrete research 28.12 (1998): 1797-1808.
