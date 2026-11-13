---
unique_name: splice
name: dna / splice
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
- 'Time: Dated'
- Expanding Science Catalogue
original_source: UCI
year: '1992'
domain: biology & life sciences
required_split:
- Grouped (NON-IID)
problem_type: Multiclass Classification
source_links:
- https://www.openml.org/search?type=data&id=40670
- https://doi.org/10.24432/C5M888
notebook_path: datasets/beyond_iid/old_iid/splice/splice.ipynb
v2_path: datasets/_dev/tabarena-v0pt2/splice/dataset.py
type_adapter_id: curation-record-v1
---

## Comments

Clean canonical entry bootstrapped from the TabArena curation workbook ('Tabular' row). Shipped in TabArena (v0.1) / BeyondArena.

TabArena curation verdict: Duplicate.

Many Binary features, which originally were 4 class categoricals. Description says "Hint: Much better performance is generally observed if attributes closest to the junction are used. In the StatLog version, this means using attributes A61 to A120 only." Is a processedversion of the splice dataset

Potential issue: duplicate

Lennart: preprocssed duplicate

Andrej: Duplicate

**Assessment (AI, 2026-10-21):** Metric declared under MET-1..13: fallback log_loss — Towell, Shavlik & Noordewier report test error rates without costs between the site types; error rate rejected.

**Assessment (AI, 2026-11-04):** reviewed for the BeyondArena v0.2 review page, without a panel, from the gathered evidence (this record, earlier experiments, model runs on the shipped data); the open questions are in the record's Review. Ship after dropping the duplicate windows: 125 windows repeat (310 rows, mostly the same gene in overlapping GenBank entries), 7.7% of test rows find their twin in training and one window is labelled both IE and N; methods separate widely. Priority 3: gap 1, use case 0, source 1, shape 1, risk -1.

CC (2026-11-06, Andrej): time basis `Timeless` accepted on the BeyondArena v0.2 review page (issue 2, B, through the cross-dataset item on routine `Timeless` issues): a splice junction is a property of the sequence, cut from GenBank 64.1 in 1992 undated. The `Time basis:` line is in the definition's notes, ending with what the split cannot test; the tag enters `data_tags` once PR #50 is in the working copy.

CC (2026-11-11, Andrej): record field set from the definition (review page field mark): `domain` biology & life sciences.

CC (2026-11-12, Andrej): collection facts `Samples: Over Time` and `Time: Dated` in place of `Samples: No Time Dimension` (BeyondArena v0.2 review page, issue 4, B): the earliest reference year of each window's GenBank entry, looked up at NCBI by locus name or through the record that holds the entry's windows at the named position, dates 1,388 of 1,475 entries (94.1%; 2,879 of 3,017 windows once issue 1's option D drops the copies), 1974 to 1990. Junction share and difficulty show no trend with the year, and a split by year leaves as many close training relatives as a random one. The facts describe the source and do not change with the split, which stays as it is (issue 3 open).

CC (2026-11-12, Andrej): split by GenBank entry component (BeyondArena v0.2 review page, issue 3, reply b, after the dating of issue 4; SPLIT-24, SPLIT-34): the entry is the instance name before the site type, and entries that share an identical 60-base window are joined, one gene in overlapping entries: 1,440 components over the 3,190 windows (the largest 82), grouped 10 x 3. No exact copy crosses the split (7.4% of the test windows at random), and 1.6% of the test windows keep a training window within 3 of 60 bases (10.2% at random). A split by entry year leaves as many close relatives as a random draw (4.1% against 4.0% within 3 bases), so the family key stands and the time basis stays `Timeless`, its line rewritten for the grouped split; the tag enters `data_tags` once PR #50 is in the working copy. `required_split` Grouped (NON-IID). The duplicate windows (issue 1) are still open.

CC (2026-11-12, Andrej): the copies of one record dropped (BeyondArena v0.2 review page, issue 1, D, agreeing with the answer of 2026-11-10; LEAK-19, LEAK-20): 125 windows of 60 bases repeat (310 rows), most the same gene in overlapping GenBank entries. One row per window and label stays, both rows of `HUMCYPIIE`'s window labelled a junction and no junction go, and the 13 windows that one entry holds at two places (duplicated genes) keep one row per place: 173 rows go, 3,017 remain (exon-to-intron 685, intron-to-exon 679, neither 1,653). The entry-component groups are joined on the whole file before the drop: 1,440 over the 3,017 windows (the largest 65). On the shipped 10 x 3 folds no test window has an identical window in training and 1.6% have one within 3 of 60 bases (0.6% and 3.7% under random folds of the same rows). The marker `Duplicate` goes, as the issue's notes say: it described OpenML's StatLog copy `dna` (each base coded as binary columns), not UCI's file, which this definition reads.

## Review

**Outcome:** added. The primate splice-junction windows of Towell, Noordewier and Shavlik (UCI, 1992,
https://doi.org/10.24432/C5M888): 3,190 windows of 60 DNA bases from GenBank 64.1, each labelled as an
exon-to-intron junction (767), an intron-to-exon junction (768) or neither (1,655); the 60 positions ship as categorical
features, random splits, log loss fallback, fit approximate (a curated set in which half the windows are junctions).
Since 2026-11-12: 3,017 windows once the copies of one record go (issue 1, D), split by GenBank entry component
(issue 3, b).
The AI recommends shipping it after dropping the duplicate windows (issue 1). Reviewed on 2026-11-04 without a panel,
from the gathered evidence (the record, the CHANGELOG, model runs on the shipped data and on TabArena v0.1's
copy) and one check on the v0.2 frame. Validity: the junction label comes from GenBank's annotation of the genes, the
inputs are the sequence alone, and no leak column exists; but 125 windows occur more than once (310 rows), mostly the
same gene in several GenBank entries, so 7.7% of the test rows find their exact window in training, and one window is
labelled both junction and non-junction (issue 1). Value: on the shipped data (the same rows and splits) the 40
benchmark
methods spread in log loss from 0.086 (Kumo) to 0.168 (default logistic regression) and 0.403 (default extra trees),
median 0.110, so the methods separate. Quality: 15 windows carry ambiguity codes (N, D, R, S), kept as categories.
Weighed: a classic sequence task where tabular methods spread widely +, a documented source +, duplicate windows
across the split -, a selected class mix rather than a genome scan -.

**Main points:** Nothing open. Settled 2026-11-12: the copies of one record dropped, the duplicated genes kept,
3,017 windows (issue 1, D); split by GenBank entry component, `Timeless` kept with the dating in its line (issue 3,
b); the entries dated, 94% of them, 1974 to 1990; collection facts `Samples: Over Time`, `Time: Dated` (issue 4).
Time basis `Timeless` (issue 2, 2026-11-06).

**Record judgment:** valid, with a record inconsistency: the `Duplicate` marker and the TabArena workbook notes ("a
processed version of the splice dataset", "preprocessed duplicate") describe OpenML's StatLog copy `dna` (each base
coded as binary columns), not UCI's original file, which this definition reads; with the suggestion `Yes`, the marker
contradicts the verdict and can go at hand-over (removed on 2026-11-12 with issue 1). UCI's `splice.names` calls the intron-to-exon sites "donors" in one
place and "acceptors" in another; the definition avoids both words.

**Issues for Andrej:**

1. **Drop the duplicate windows and the window labelled both junction and non-junction?**

   * **Problem:**
     - 125 windows of 60 bases occur more than once, 310 rows in all (185 extra copies, nearly all junctions), and
       the definition keeps them without a decision, so under the random split 7.7% of the test rows (6.4% to 9.0% per
       split) have their exact window in training.
     - One window is labelled an intron-to-exon junction under `HUMCYPIIE-ACCEPTOR-12121` and no junction under
       `HUMCYPIIE-NEG-12121`: the same GenBank entry and position with two labels.
     - Drop the copies and the contradictory pair, group the copies, or keep everything?
   * **Background:**
     - The instance names give the GenBank entry, the site type and the position. Most copies are the same gene in
       overlapping entries (`HUMIL2`, `HUMIL2A`, `HUMIL2B`; `HUMERP`, `HUMERPA`); some are one record listed twice
       (`HUMALBGC-ACCEPTOR-18496`, `HUMMYLCA-DONOR-644`); a few are duplicated genes whose junctions are identical (the
       two alpha-globin genes of `HUMHBA4`, the CYP21 gene and its pseudogene). 18 of the 125 groups lie within one
       entry, 107 span two to four.
     - The source took "every split-gene for primates in Genbank 64.1" (`splice.names`), so redundant entries came in
       with it. A copy adds nothing a model can learn beyond the first row, but it answers its twin in the test fold.
   * **Effect on the task:** a test window whose twin is in training is answered by look-up, so scores are optimistic
     and favour methods that trust exact matches; the contradictory pair puts a near-certain wrong answer in every
     fold that splits it (we measured about 7% of a split's summed log loss on that one pair).
   * **Experiments:** v0.2 frame, the first 9 shipped splits, untuned LightGBM: log loss 0.112 as shipped against
     0.119 with the copies dropped (3,004 rows: one row per window and label, the contradictory pair removed).
   * **Consistency:** follows wine_quality (1,177 exact copies dropped, 2026-09-30), the rule's case for dropping
     copies rather than grouping them[^1a], and jm1 for features with two labels[^1b].
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Keep all (implemented) | 3,190 rows, copies on both sides of the split | the file as published | 7.7% of test rows answered by look-up; a contradictory pair; no recorded decision |
     | B | Drop the copies | one row per window and label; both rows of the contradictory window go; 3,004 rows | test windows are new to the model; as wine_quality | 186 rows fewer; second copies of truly duplicated genes go too |
     | C | Group the copies | identical windows share a fold; all rows kept | no look-up across the split; rows kept | the copies still weigh double in training; the contradictory pair stays |

   * **Recommendation:** B: the copies are mostly redundant database entries, a copy teaches nothing beyond its first
     row, and the contradictory pair is a labelling error. **Decision:** keep (A), drop the copies (B) or group them
     (C)?

   **Notes for the AI:** on B, in `_clean`, before dropping the instance id: drop rows whose 60-base window and label
   repeat an earlier row, and drop every row of a window that carries two labels; a curation note with the 125 groups,
   the 185 copies and the `HUMCYPIIE` pair; `changes` and `split` in the task summary; `dataset check` (the
   `dataset_duplicate_rows` warning goes); CHANGELOG; record CC. On B or C, the record's `Duplicate` marker goes as
   well (it is OpenML's `dna` copy's).

   [^1a]: **LEAK-19** (Should): exact copies with the same label: drop them rather than group on the duplicate key
     (wine_quality, 1,177 rows). **LEAK-16** (Must): duplicate rows need a decision every time.
   [^1b]: **LEAK-20** (Should): feature vectors that occur with both labels: drop every copy, unless they are genuine
     label ambiguity the task has (jm1, 176 rows).

   **Answer (AI, 2026-11-06):** Under the new entity-leakage rules the copies still go; should the windows of
   duplicated genes, distinct places in the genome, stay?

   * **Problem:**
     - Under the new rules a repeat the data does not record gets one verdict, and these repeats are copies of one record (the same gene in overlapping GenBank entries, or one name listed twice), which go down to one row per window, as option B does.
     - 13 of the 125 groups also hold their window at two positions of one GenBank entry: two copies of a duplicated gene, such as the two alpha-globin genes of `HUMHBA4`, the gibbon's two gamma-globin genes (`GIBHBGGL`) and the growth hormone cluster (`HUMGHCSA`), whose junctions read the same.
     - The rule on copies keeps distinct units that the features cannot tell apart, with a note, while B drops these 13 with the rest.
   * **Verdict: entity fix on an exact key.** The 60-base window is the key, and the instance names that the
     definition drops say what each repeat is[^1e].
     - Is the link real? 262 pairs of rows share all 60 bases; with each position's bases shuffled within the class,
       about 5 x 10^-27 such pairs are expected.
     - Does the label travel with the link? The label agrees in 124 of 125 groups. With identical windows the
       features explain that, so this test cannot tell a copy from a look-alike, and the names settle it: 107 groups
       span 2 to 4 overlapping entries of the same gene, and 12 list one name twice.
     - Is there an order? No: the windows were cut from one GenBank release, with no date.
   * **What the drop does to the classes:** B removes 186 rows (5.8%): 88 exon-to-intron junctions (11.5% of them),
     96 intron-to-exon junctions (12.5%) and 2 non-junctions (0.1%).
     - Before and after: exon-to-intron 24.0% to 22.6%, intron-to-exon 24.1% to 22.4%, neither 51.9% to 55.0%.
     - The copies are junctions because overlapping entries repeat the same annotated junction, while the
       non-junction windows were drawn at positions within each entry and rarely coincide.
     - Does the target still stand for the use case? The AI reads yes: the label means the same, and the source's
       curated mix of about half junctions moves to 45%.
   * **The duplicated genes:** keeping one row per position within an entry brings back 13 rows: 3,017 in all
     (exon-to-intron 22.7%, intron-to-exon 22.5%, neither 54.8%). Under random 3-fold splits 0.6% of the test rows then
     find the identical window of a sister gene in training, against 7.6% as shipped; for these the verdict is
     natural, distinct look-alikes, and the notes report the overlap.
     - The names prove distinct places only within one entry. Two genes of one family in two entries read like one
       gene in two entries (the CYP21 gene and its pseudogene may be such a case, in `HUMCP21OH`, `HUMCP21OHC`,
       `HUMMHCP42` and `HUMMHCP52`), so such pairs stay merged.
     - Of the 18 groups within one entry, 12 list one name twice, 5 are duplicated genes, and 1 is the window labelled
       both ways (`HUMCYPIIE`, one position), which goes under b and d.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Keep all (implemented) | 3,190 rows | the file as published | 7.6% of test rows answered by a copy; the window labelled both ways stays |
     | b | Drop the copies | one row per window and label; both rows of the two-label window go; 3,004 rows | no window on both sides of the split | the 13 windows of duplicated genes go too |
     | c | Group the copies | identical windows share a fold; all rows kept | no look-up across the split | copies of one record weigh double in training; the two-label pair stays |
     | d | Drop the copies of one record, keep the duplicated genes | as b, then one row per position within an entry: 3,017 rows | follows the rule on copies; distinct places in the genome stay | 0.6% of test rows meet a sister gene's identical window in training |

   * **Recommendation:** d: the copies of one record go as in b, and the 13 windows of duplicated genes are distinct
     units that the window cannot tell apart, which the rule on copies keeps with a note[^1f]; the 0.6% overlap they
     leave is a gene family an annotation tool also meets. **Decision:** d, b, c, or keep a?

   **Notes for the AI:** on d, in `_clean` before dropping the instance id: apply b, then for each window whose one
   GenBank entry (the name before the site type) holds it at 2 or more positions, keep the first row per position of
   that entry; 13 rows come back, 3,017 rows (EI 685, IE 679, N 1,653). The curation note names the 125 groups, the
   184 copies of one record and the `HUMCYPIIE` pair dropped, and the 13 duplicated-gene windows kept with the 0.6%
   overlap.

   [^1e]: **LEAK-41** (Must; draft PR #62): repeats of a unit the data does not record get one of four verdicts:
     natural, entity fix, temporal fix or not recoverable; an entity fix takes copies of one record down to one row
     per unit, and every drop gives the label shares before and after and asks whether the target still stands.
     **LEAK-42** (Should; draft PR #62): three tests set the verdict: a link far above a chance rate that keeps the
     data's structure, a label that travels with the link beyond what the shared features predict, and an order.
   [^1f]: **LEAK-19** (Should): exact copies with the same label are dropped rather than grouped; copies of one
     compound go, while distinct compounds the descriptors cannot tell apart stay with the reason in the notes
     (hiva_agnostic, qsar_tid_11). **SPLIT-24** (Must; draft PR #62): a key built from the data exactly, here the
     window and the instance name.

   **Andrej (2026-11-10, discuss):** I generally tend towards D, but shouldn't this be a grouped split then?

   **Answer (AI, 2026-11-10):** a grouped split is possible and costs nothing in score. On D's 3,017 windows it removes
   the exact overlap and part of the near relatives. It is a decision of its own, so it is issue 3.

   | Split of D's rows (10 x 3) | Groups | Identical window in training | Within 3 of 60 bases | Within 5 | LightGBM log loss | Logistic regression |
   |---|---|---|---|---|---|---|
   | Random | 3,017 rows | 0.55% | 3.8% | 5.4% | 0.120 | 0.160 |
   | By GenBank entry | 1,471 | 0% | 2.8% | 4.3% | 0.119 | 0.159 |
   | By entry component (entries sharing an identical window) | 1,440 | 0% | 1.3% | 2.3% | 0.118 | 0.160 |

   * **Entries can be recovered:** the instance name starts with the GenBank entry (`HUMHBA4-DONOR-7090`). 1,234 of the
     1,471 entries hold a single window.
   * **Genes cannot be recovered fully:** one gene in several entries (`HUMIL2`, `HUMIL2A`) can be joined only through a
     window they share exactly, which gives the components.
     Orthologs and sister genes in other entries share no identical window, and joining them by similarity is barred.
   * **Effect on issue 2's near-copies:** grouping by component lowers the near relatives within 3 bases from 3.8% to
     1.3% of the test windows. The rest are orthologs and gene families in entries that no exact key links.
   * D's 13 duplicated-gene windows sit within one entry, so under either grouping they always share a fold; their 0.55%
     identical overlap goes to 0.
   * The score does not move (differences of 0.002 or less, SD 0.011 to 0.019), so the near relatives do not inflate it.
   * **Recommendation:** D here, and the split in issue 3. **Decision:** D, B, C or keep A?

   **Andrej (2026-11-12, discuss):** Agree.

   **Resolved (2026-11-12, Andrej):** D (the answer of 2026-11-10), fitted to issue 3's split: in `_clean` the entry
   components are joined on the whole file first, then `_one_row_per_record` keeps one row per window and label, drops
   both rows of `HUMCYPIIE`'s window labelled two ways, and keeps one row per place for the 13 windows one entry holds
   at two or more places (duplicated genes). Task summary `row`, `predicted`, `changes`; a curation note; the split
   note and `splits_comment` re-measured. Record CC line; the marker `Duplicate` removed (OpenML's `dna` copy's, as the
   notes say for B, which D applies first). Verdict ship; split and metric `ok`.

   | Shipped 10 x 3 grouped folds | Before (3,190 windows) | Now (3,017 windows) | Random 10 x 3, rows now |
   |---|---|---|---|
   | Exon-to-intron / intron-to-exon / neither | 767 / 768 / 1,655 | 685 / 679 / 1,653 | |
   | Entry components | 1,440 (largest 82) | 1,440 (1,226 single; largest 65, 2.2%) | |
   | Test windows per fold | 925 to 1,219 | 877 to 1,121 | 1,005 to 1,006 |
   | Identical window in training | 0% | 0% | 0.6% |
   | Within 3 of 60 bases | 1.6% | 1.6% (0.7% to 2.5% per fold) | 3.7% |
   | Within 10 of 60 bases | 5.1% | 5.0% | 7.9% |

   * The within-3 share stays 1.6%: every copy sat in one component already, so the drop changes look-ups only for a
     random split (7.4% identical before, 0.6% now).
   * `dataset check` (Slurm 1380083): 0 errors, 0 warnings, 1 info (`dataset_duplicate_rows`, 13 rows: the duplicated
     genes' second places, each pair in one group); the 184-row warning and the two-label info are gone. README
     regenerated; not rebuilt.

2. **Time basis: name the random split `Timeless`?**

   * **Problem:**
     - Each row is a 60-base window cut in 1992 from primate genes in GenBank release 64.1, labelled by the annotation
       of the same sequence; the instance names give the entry, the site type and the position, no date, and the
       window and its label exist together.
     - The record carries `Samples: No Time Dimension` and no time or target fact, which fits a reference collection
       of sequences; the split is random and names no time basis yet.
     - Whether a position is a splice junction, and of which kind, is a fixed property of the sequence, the case the
       `Timeless` prototype names, with a random split or one grouped by item family[^2a].
   * **Background:** the entries were deposited over years before release 64.1, but when a gene was sequenced does not
     change where its exons end. The family of an item here is the gene: issue 1 settles the exact copies of one gene
     in several entries. Beyond them, after issue 1's B, 3.4% of the test windows have a training window within 3
     of 60 bases (4.9% within 5), always of the same label, and in 91% of those cases the nearest window sits in
     another entry: mostly the same gene in another primate or a sister gene (the globins, the CYP21 pair). A tool
     annotating a new primate genome has such relatives in its training data, and grouping by sequence similarity is
     barred, so the random split stays.
   * **Experiments:** UCI's `splice.data`, issue 1's B applied (3,004 windows), 3 x 3 random folds, the Hamming
     distance of each test window to its nearest training window (model-free).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random split, no time basis (implemented) | as now | nothing to change | the definition does not say why a random split is safe in time |
     | B | Random split, `Timeless` | as now (with issue 1's decision); the tag and a `Time basis:` line naming the sequence property and the 1992 cut | states the fact the split rests on; the near relatives measured | none found |

   * **Recommendation:** B: the junction is a property of the sequence, and the relatives left after issue 1 are ones
     an annotation tool also has. **Decision:** A or B?

   **Notes for the AI:** on B, once PR #50 is in: `data_tags = ("Timeless",)` (the class adds `IID`), a curation
   bullet `- Time basis: Timeless: a splice junction is a property of the sequence; the windows were cut in 1992 from
   GenBank 64.1 and labelled by its annotation, with no date. After the copies leave, 3.4% of the test windows have a
   training window within 3 of 60 bases, nearly all the same gene in another primate or a sister gene.` (the share
   as measured after issue 1's decision), no `splits_comment` change; `dataset check`.

   [^2a]: **SPLIT-32** (Should): how the data was collected is information for the split; the record carries the
     source's collection facts, and a definition can name the use-case prototype it follows with a `Time basis:`
     line. `Timeless`: the target is a fixed property of the item, the same whenever it is measured; the split is
     random or grouped by item family. **SPLIT-24** (Must): group on a true group id or one constructed exactly from
     the data, never on a similarity-threshold cluster. **SPLIT-31** (Should): over related entities, IID can match how
     a task is framed even when it is optimistic.

   **Resolved (2026-11-06, Andrej):** B, accepted through the cross-dataset item "Accept the routine `Timeless` time
   issues with one mark?" The `Time basis: Timeless:` bullet is in `curation_comments`, ending with what the split
   cannot test (a gene with no relative among the training windows); the split and `data_tags` are unchanged. The 3.4%
   of near relatives was measured without the exact copies (issue 1's B), so the line says "exact copies of a window
   aside" and holds whatever issue 1 decides. The tag `Timeless` enters `data_tags` once PR #50 is in the working copy.

3. **Split by GenBank entry component instead of at random?**

   * **Problem:**
     - Andrej asked whether option D of issue 1 should go with a grouped split (2026-11-10).
     - The instance names give the GenBank entry, and entries that share an identical window are one gene in several entries, so groups can be built on an exact key: 1,440 entry components over D's 3,017 windows.
     - Keep the random split, or group by entry component?
   * **Background:** the definition drops the instance name, so the key has to be built in `_clean` before the name
     is dropped. Orthologs and sister genes in other entries share no identical window, and no exact key links them;
     grouping them by sequence similarity is barred[^3a]. Issue 2's `Timeless` line allows a random split or one grouped
     by item family.
   * **Effect on the task:** the test windows then come from genes whose entries are all unseen. This is closer to
     annotating a new gene, while orthologs in other primates can still sit in training.
   * **Experiments:** D's 3,017 windows, 10 x 3 folds:

     | Split | Identical window in training | Within 3 of 60 bases | LightGBM log loss | Logistic regression |
     |---|---|---|---|---|
     | Random | 0.55% | 3.8% | 0.120 | 0.160 |
     | By entry | 0% | 2.8% | 0.119 | 0.159 |
     | By entry component | 0% | 1.3% | 0.118 | 0.160 |

     - The largest component holds 65 windows (2.2%); 84 pairs of windows of one entry lie less than 60 bases apart
       and overlap in sequence, and both groupings keep them together.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Random (implemented) | as now | nothing to build | 0.55% identical and 3.8% near windows across the split; overlapping windows of one entry split |
     | B | By entry component | `gene_group` from the entries joined through identical windows; grouped 10 x 3 | no window and no entry on both sides; exact key; same score | orthologs in other entries still cross |
     | C | By entry | `entry` from the instance name | simplest key | one gene in two entries can cross (2.8% near) |

   * **Recommendation:** B. It is exact, it costs nothing in score, and it holds out each gene's entries together.
     **Decision:** random (A), by entry component (B) or by entry (C)?

   **Notes for the AI:** on B, in `_clean` before dropping the instance id: entry = the name before the site type
   (`rsplit("-", 2)[0]`), union-find over entries that share an identical 60-base window in the raw file, the root as
   `gene_group` (anonymised); `Grouping(on="gene_group", labels="per_sample", prediction_unit="row", context="none")`,
   `split` and `splits_comment`, a curation note with the counts above; record `required_split` Grouped; `dataset
   check`. Apply after issue 1 (the counts are for D).

   [^3a]: **SPLIT-24** (Must): group on a true group id or on one built exactly from the data, never on a
     similarity-threshold cluster.

   **Andrej (2026-11-11, discuss):** What is the split that comes closest to what practitioners in reality would face?

   **Answer (AI, 2026-11-11):** a practitioner annotates genes the model has never seen, with no close relative in
   training; the closest split is grouping by sequence similarity, which the rules bar, and the closest allowed one is
   the entry component (B). The gap between them is small (+0.006 log loss).

   * **Who uses it:** a splice-site predictor marks exon-intron borders in a newly sequenced gene or genome, mostly
     human, sometimes another species. Modern tools test on held-out chromosomes and drop paralogs from the test set,
     so test genes have no close relative in training.
   * **What the data allows:** the instance name gives the GenBank entry, so entries and entry components are exact
     keys. 95% of the windows are human (2,879); the 138 windows of 12 other primates are too few for an organism
     split. Orthologs and sister genes in other entries are linked only by similarity.
   * **The similarity groups:** joining entry components whose windows lie within 10 of 60 bases gives 1,417 groups
     (largest 2.8%) and leaves no test window with a relative within 10 bases.

   | Split of D's rows | Groups | Identical window in training | Within 3 of 60 | Within 10 | LightGBM log loss | Logistic regression |
   |---|---|---|---|---|---|---|
   | Random (10 x 3) | 3,017 | 0.55% | 3.8% | 8.0% | 0.120 (SD 0.011) | 0.160 |
   | Entry component (10 x 3) | 1,440 | 0% | 1.3% | 4.6% | 0.118 (0.012) | 0.160 |
   | Similarity within 5 (10 x 3) | 1,425 | 0% | 0% | 0.7% | 0.127 (0.017) | 0.170 |
   | Similarity within 10 (10 x 3) | 1,417 | 0% | 0% | 0% | 0.124 (0.015) | 0.169 |
   | Train human, test the 138 other primates (1 split) | | 0% | 9.4% | 15.2% | 0.106 | 0.122 |

   * Holding out relatives costs 0.004 to 0.009 for LightGBM and 0.010 for logistic regression, within one SD; the
     gap between the two models stays.
   * The other primates are easier, not harder: their genes are orthologs of the human ones in training.
   * **Options:**

     | | Option | Pro | Con |
     |---|---|---|---|
     | A | Random (implemented) | nothing to build | 0.55% identical and 3.8% near windows cross |
     | B | Entry component (recommended above) | exact key; no window or entry on both sides | 1.3% near relatives in other entries cross |
     | C | Similarity groups within 10 bases | closest to a new gene with no relative in training | a threshold cluster, barred as a group key[^3a]; needs an exception |
     | D | By organism | a new species | 95% human, 138 test windows; easier, not harder |

   * **Recommendation:** B. It is the closest split built on an exact key, and C would change the score by less
     than one SD. **Decision:** A, B, C or D?

   **Answer (AI, 2026-11-12):** splice is a cut of GenBank, a database that keeps growing, so the split rule for growing
   catalogues applies to it[^3b]; it was left out of that review by mistake. On that rule's steps the recommendation
   stays B, with one step not measured yet, which issue 4 asks about.

   | Step | Splice | Status |
   |---|---|---|
   | Item | the duplicate windows and the window labelled both junction and non-junction | issue 1, open (you lean to D) |
   | Family | the GenBank entry component: entries joined through an identical window | this issue's B |
   | Source | built "to help evaluate a 'hybrid' learning algorithm (KBANN)", scored by ten-fold cross-validation on 1,000 random windows; a habitual random split says nothing about scope, and the source names no limit | goes on to the date |
   | Entry date | each window's GenBank entry is known by name, but no entry date has been looked up | issue 4 |

   * The family key is the rule's default: B stands unless the dating of issue 4 shows that a split by entry date leaves
     test windows clearly fewer close training relatives than a random draw does.
   * Issue 2's `Timeless` was decided for the random split; under B it carries over only if the dating finds no wave.

   [^3b]: **SPLIT-34** (Should): a dataset drawn from a database that keeps growing can be split by the item, its family
     or the date it entered; the family key is the default, the source's stated aim and scope decide which items the
     test set stands for, and the date replaces the family key only where it carries waves.

   **Answer (AI, 2026-11-12):** the entries are dated (issue 4), and the date carries no wave: split by entry
   component (b), by entry year (c), or keep random (a)?

   * **Problem:**
     - Predicting each later year from the earlier ones, which is how a practitioner meets newly sequenced genes, leaves
       the test windows as many close training relatives as a random draw of the same size.
     - Holding out the test windows' entry components leaves the fewest, at the same score.
     - So the date does not replace the family key, and B stays the closest split on an exact key[^3c].
   * **Background:** three expanding windows by entry year (test 1988, 1989 and 1990; training 55%, 72% and 95% of the
     dated windows); the same test windows trained on every earlier window, on a random draw of the same size, or on
     that draw kept out of the test windows' entry components. Untuned LightGBM and one-hot logistic regression, 10
     draws or seeds, means over the three windows (Slurm 1379990):

     | Training side | Within 3 of 60 bases | Within 10 | LightGBM log loss | Logistic regression |
     |---|---|---|---|---|
     | Forward by year | 4.1% | 9.3% | 0.093 | 0.143 |
     | Random draw, same size | 4.0% | 8.4% | 0.091 | 0.139 |
     | Random draw outside the test entry components | 2.3% | 5.4% | 0.094 | 0.141 |

     - No identical window crosses under any of them. In the 1990 window the forward side is every other dated window,
       so forward and random coincide there.
     - On the 1,221 entries dated by name or at the named position only, the picture holds: 4.4%, 4.2% and 2.5% within
       3 bases; LightGBM 0.092, 0.090 and 0.092 (Slurm 1380014).
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | a | Random (implemented) | as now | nothing to build | 0.55% identical and 3.8% near windows cross |
     | b | By entry component, `Timeless` kept | issue 3's B; the `Time basis:` line names the dating and its flat result | the fewest close relatives on an exact key; the date measured, not assumed | orthologs in other entries still cross (1.3% within 3 bases) |
     | c | By entry year | three expanding windows on a year table from NCBI shipped with the definition | the order in which genes arrive | as many close relatives as random; 138 windows undated; a reference year, not the day of entry |

   * **Recommendation:** b: the forward split holds out nothing that a random draw does not, and the entry component
     is the one exact key that does. **Decision:** a, b or c?

   **Notes for the AI:** on b, issue 3's notes for B, and the `Time basis: Timeless:` bullet rewritten for the grouped
   split: the junction is a property of the sequence; the windows' GenBank entries, dated by their earliest reference
   (94% of entries, 1974 to 1990), show no wave, and a split by entry year leaves as many close relatives as a random
   one; grouped by entry component, 1.3% of the test windows keep a training window within 3 of 60 bases (under
   issue 1's D; re-measure under another option); not tested: a gene with no relative among the training windows. Once PR #50 is in,
   `data_tags = ("Timeless",)`. On c, `entry_year` joined in `_clean` from an entry-year table
   copied into the folder, `Temporal(..., feature=False)` with windows 1988, 1989, 1990, the undated windows in
   training; `dataset check`.

   [^3c]: **SPLIT-34** (Should): within the source's scope the entry date replaces the family key only when it carries
     waves, or a forward split leaves the test items clearly fewer close training neighbours than a random draw;
     otherwise the family key stands and the time basis says why. Here the forward split leaves 4.1% within 3 bases
     against 4.0% for a random draw.

   **Andrej (2026-11-12, discuss):** Reply (b): By entry component, Timeless kept

   **Resolved (2026-11-12, Andrej):** b: split by GenBank entry component. In `_clean`, before the instance name goes,
   the entry is the name before the site type, entries that share an identical 60-base window are joined, and the
   component's number is `gene_group`; `Grouping(on="gene_group", labels="per_sample", prediction_unit="row",
   context="none")`, 10 x 3. Task summary `split` and `changes`, `splits_comment`, a curation note on the split, and
   the `Time basis: Timeless:` bullet rewritten for the grouped split (the dating, no wave, forward 4.1% against
   random 4.0%), ending with what the split cannot test (a gene with no relative among the training windows).
   Measured on the 3,190 windows shipped while issue 1 is open:

   | Measure | Entry component (shipped) | Random 10 x 3, same rows |
   |---|---|---|
   | Groups | 1,440 (1,225 single windows; largest 82, 2.6%) | 3,190 |
   | Test windows per fold | 925 to 1,219 | 1,063 to 1,064 |
   | Identical window in training | 0% | 7.4% |
   | Within 3 of 60 bases | 1.6% (0.6% to 3.2% per fold) | 10.2% |
   | Within 10 of 60 bases | 5.1% | 14.1% |

   * Every repeated window lies in one component, so no copy crosses whatever issue 1 decides; on D's 3,017 rows the
     share within 3 bases was 1.3%.
   * `dataset check` (Slurm 1380066): 0 errors, 1 warning (`dataset_duplicate_rows`, 184 rows, issue 1), 1 info (the
     window labelled two ways), the same findings as before; README regenerated; not rebuilt. The split and group
     probes were not run.
   * Record `required_split` Grouped (NON-IID), CC line. The tag `Timeless` enters `data_tags` once PR #50 is in the
     working copy.

4. **Date the GenBank entries before settling the split?**

   * **Problem:**
     - Splice's windows are cut from GenBank entries, and GenBank keeps growing, so the split rule for growing
       catalogues asks whether the date an entry entered GenBank carries waves before the family key settles[^4a].
     - Nobody has looked that date up: the release keeps only the entry name of each window.
     - Date the entries first, or settle the split without the date?
   * **Background:**
     - The instance names give each window's GenBank entry (1,440 entry components over D's 3,017 windows, issue 3). UCI
       dates the donation 1991-12-31, so every entry predates 1992.
     - The source was built to evaluate a learning algorithm (KBANN) and scored ten-fold cross-validation on 1,000
       random windows, so it neither limits the use case nor dates anything.
     - For the regulatory toxicity sets you chose to date the chemicals first (qsar_oral_toxicity,
       qsar_bioconcentration, qsar_fish_toxicity, qsar_aquatic_toxicity); their dates showed no wave, and the scaffold
       split stayed. For qsar_tid_11 the date did show one, and it is split by year.
   * **What dating would take:** each entry's first submission date from NCBI by its entry name (entries renamed or
     merged since then may not resolve); the share dated and the range; then, if the span gives at least three
     windows[^4b], expanding windows by entry date against a random draw of the same size on the same test windows, with
     the share of test windows that have a relative within 3 and within 10 of 60 bases, as issue 3 measured.
   * **Options:**

     | | Option | What it does | Pro | Con |
     |---|---|---|---|---|
     | A | Settle without dating | issue 3 decides; the `Time basis:` line says the entry order is unmeasured | no lookup | the date question rests on an assumption |
     | B | Date the entries first | the lookup and the measurement above; issue 3 waits for the result | decides on a measurement, as for the toxicity sets | entries from before 1992 may span too few years for three windows; renamed entries may not resolve |

   * **Recommendation:** B, as you chose for the toxicity sets: the key is in the release, so the question can be
     settled by measurement. **Decision:** A or B?

   **Notes for the AI:** on B, a script: NCBI E-utilities (`esearch` on nuccore by
   entry name, then the earliest date in the record; a generic client name, rate-limited), coverage and range first; if
   three windows fit, the forward-against-random measurement on D's rows as a Slurm CPU job; then an answer in this
   issue and in issue 3. If the entries are dated, the record's facts become `Samples: Over Time` and `Time: Dated`
   whichever split wins. On A, issue 3's decision stands alone.

   [^4a]: **SPLIT-34** (Should): the family key is the default; the source's stated aim and scope decide which items the
     test set stands for; within that scope the entry date replaces the family key when the use case predicts for items
     the catalogue does not hold yet, the date is when the item entered, the labels are final, and a forward split
     leaves the test items clearly fewer close training neighbours than a random draw.
   [^4b]: **SPLIT-14** (Must): a temporal task has at least 3 windows; the newest window and at least one other train on
     at least 50% of the data.

   **Andrej (2026-11-12, change):** Option B: Date the entries first.

   **Resolved (2026-11-12, Andrej):** B: dated. 1,388 of 1,475 GenBank entries (94.1%) and 2,879 of D's 3,017 windows
   (95.4%), 1974 to 1990, median 1987; the date carries no wave.

   | Measure | Result |
   |---|---|
   | Dated by locus name at NCBI | 795 entries |
   | Dated by the record that holds the entry's windows at the named position | 593 entries |
   | Check of that match on the 803 entries NCBI knows by name | same record 99.4%, same year 99% |
   | Not dated | 87 entries, 138 windows (66% non-junctions) |
   | Junction share by entry year (7 periods) | 36% to 56%, no trend (Spearman 0.09) |
   | LightGBM log loss by entry year, out of fold | 0.05 to 0.15, no trend |
   | Test windows with a training window within 3 bases: forward by year / random draw | 4.1% / 4.0% (issue 3) |

   * The date is the earliest reference year of the entry (the paper, or a direct submission); NCBI's own create date
     cannot serve, since many old entries carry the 27-APR-1993 database conversion. The records are all in the
     primate division (PRI) but 2 viral (VRL) and 1 STS.
   * Record facts `Samples: Over Time` and `Time: Dated` in place of `Samples: No Time Dimension`, with a CC line and
     `Andrej` in `checked_by`. Definition and split unchanged; issue 3 decides the split, with an answer that uses the
     dates.

## Reference

10.24432/C5M888; Originally from the StatLog project.; https://www.rdocumentation.org/packages/mlbench/versions/2.1-1/topics/DNA
